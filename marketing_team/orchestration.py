"""Orchestration strategies: sequential, parallel, and human-in-the-loop."""

from __future__ import annotations

import asyncio
import time
from collections.abc import Callable
from dataclasses import dataclass, field

from marketing_team.structured import run_structured

from marketing_team.agents import (
    build_copywriter,
    build_editor,
    build_planner,
    build_seo,
)
from marketing_team.models import (
    CampaignPackage,
    CampaignPlan,
    ContentChannel,
    DraftPiece,
    EditedPiece,
    ReviewDecision,
    SeoOptimizedPiece,
    Subtask,
)


@dataclass
class RunMetrics:
    """Simple cost/latency counters for the scaling chapter."""

    steps: list[dict] = field(default_factory=list)

    def record(self, name: str, seconds: float) -> None:
        self.steps.append({"name": name, "seconds": round(seconds, 3)})

    @property
    def total_seconds(self) -> float:
        return round(sum(s["seconds"] for s in self.steps), 3)

    def summary(self) -> str:
        lines = [f"  - {s['name']}: {s['seconds']}s" for s in self.steps]
        lines.append(f"  TOTAL: {self.total_seconds}s")
        return "\n".join(lines)


async def plan_campaign(brief: str) -> CampaignPlan:
    planner = build_planner()
    return await run_structured(planner, brief, CampaignPlan)


async def draft_for_subtask(subtask: Subtask, plan: CampaignPlan) -> DraftPiece:
    copywriter = build_copywriter()
    prompt = (
        f"Campaign: {plan.campaign_name}\n"
        f"Audience: {plan.audience}\n"
        f"Goal: {plan.goal}\n"
        f"Tone: {plan.tone}\n"
        f"Channel: {subtask.channel.value}\n"
        f"Title hint: {subtask.title}\n"
        f"Brief: {subtask.brief}\n"
    )
    return await run_structured(copywriter, prompt, DraftPiece)


async def edit_draft(draft: DraftPiece, plan: CampaignPlan) -> EditedPiece:
    editor = build_editor()
    prompt = (
        f"Campaign tone: {plan.tone}\n"
        f"Audience: {plan.audience}\n"
        f"Draft channel: {draft.channel.value}\n"
        f"Title: {draft.title}\n"
        f"Body:\n{draft.body}\n"
        f"Author notes: {draft.notes}\n"
    )
    return await run_structured(editor, prompt, EditedPiece)


async def optimize_seo(edited: EditedPiece, plan: CampaignPlan) -> SeoOptimizedPiece:
    seo = build_seo()
    prompt = (
        f"Campaign: {plan.campaign_name}\n"
        f"Goal: {plan.goal}\n"
        f"Channel: {edited.channel.value}\n"
        f"Title: {edited.title}\n"
        f"Body:\n{edited.body}\n"
    )
    return await run_structured(seo, prompt, SeoOptimizedPiece)


async def run_sequential(brief: str, metrics: RunMetrics | None = None) -> CampaignPackage:
    """Planner → (blog + social + seo drafts one-by-one) → edit each → SEO each."""
    metrics = metrics or RunMetrics()

    t0 = time.perf_counter()
    plan = await plan_campaign(brief)
    metrics.record("planner", time.perf_counter() - t0)

    drafts: list[DraftPiece] = []
    edited: list[EditedPiece] = []
    seo_pieces: list[SeoOptimizedPiece] = []

    for subtask in plan.subtasks:
        t0 = time.perf_counter()
        draft = await draft_for_subtask(subtask, plan)
        drafts.append(draft)
        metrics.record(f"copywriter:{subtask.channel.value}", time.perf_counter() - t0)

        t0 = time.perf_counter()
        edited_piece = await edit_draft(draft, plan)
        edited.append(edited_piece)
        metrics.record(f"editor:{subtask.channel.value}", time.perf_counter() - t0)

        if subtask.channel in (ContentChannel.BLOG, ContentChannel.SEO):
            t0 = time.perf_counter()
            optimized = await optimize_seo(edited_piece, plan)
            seo_pieces.append(optimized)
            metrics.record(f"seo:{subtask.channel.value}", time.perf_counter() - t0)

    return CampaignPackage(plan=plan, drafts=drafts, edited=edited, seo=seo_pieces)


async def run_parallel(brief: str, metrics: RunMetrics | None = None) -> CampaignPackage:
    """Planner, then draft all channels in parallel, then edit+SEO in parallel."""
    metrics = metrics or RunMetrics()

    t0 = time.perf_counter()
    plan = await plan_campaign(brief)
    metrics.record("planner", time.perf_counter() - t0)

    t0 = time.perf_counter()
    drafts = list(
        await asyncio.gather(*(draft_for_subtask(s, plan) for s in plan.subtasks))
    )
    metrics.record("copywriter:parallel", time.perf_counter() - t0)

    t0 = time.perf_counter()
    edited = list(await asyncio.gather(*(edit_draft(d, plan) for d in drafts)))
    metrics.record("editor:parallel", time.perf_counter() - t0)

    seo_targets = [e for e in edited if e.channel in (ContentChannel.BLOG, ContentChannel.SEO)]
    t0 = time.perf_counter()
    seo_pieces = list(await asyncio.gather(*(optimize_seo(e, plan) for e in seo_targets)))
    metrics.record("seo:parallel", time.perf_counter() - t0)

    return CampaignPackage(plan=plan, drafts=drafts, edited=edited, seo=seo_pieces)


def human_review(
    package: CampaignPackage,
    ask: Callable[[str], str] | None = None,
) -> CampaignPackage:
    """Pause for human approval before anything is 'published'.

    `ask` defaults to input() for CLI; Streamlit passes its own callback.
    """
    ask = ask or input
    print("\n=== HUMAN REVIEW ===")
    print(f"Campaign: {package.plan.campaign_name}")
    print(f"Goal: {package.plan.goal}")
    for piece in package.edited:
        print(f"\n[{piece.channel.value.upper()}] {piece.title}")
        preview = piece.body[:400] + ("…" if len(piece.body) > 400 else "")
        print(preview)

    decision = ask("\nApprove for publish? [y/N]: ").strip().lower()
    approved = decision in {"y", "yes"}
    feedback = ""
    if not approved:
        feedback = ask("What should change? ").strip()

    package.review = ReviewDecision(approved=approved, feedback=feedback)
    package.published = approved
    return package


async def run_campaign(
    brief: str,
    *,
    mode: str = "parallel",
    require_approval: bool = True,
    ask: Callable[[str], str] | None = None,
) -> tuple[CampaignPackage, RunMetrics]:
    metrics = RunMetrics()
    if mode == "sequential":
        package = await run_sequential(brief, metrics)
    else:
        package = await run_parallel(brief, metrics)

    if require_approval:
        package = human_review(package, ask=ask)
    return package, metrics
