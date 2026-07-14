"""Step-by-step pipeline for the Streamlit product UI."""

from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass, field

from marketing_team.models import (
    CampaignPackage,
    CampaignPlan,
    ContentChannel,
    DraftPiece,
    EditedPiece,
    SeoOptimizedPiece,
)
from marketing_team.orchestration import (
    RunMetrics,
    draft_for_subtask,
    edit_draft,
    optimize_seo,
    plan_campaign,
)


@dataclass
class AgentStep:
    id: str
    name: str
    tagline: str
    icon: str


AGENT_STEPS: list[AgentStep] = [
    AgentStep(
        id="planner",
        name="Algen Planner",
        tagline="Turns your campaign brief into channel-specific tasks",
        icon="🧭",
    ),
    AgentStep(
        id="copywriter",
        name="Algen Copywriter",
        tagline="Drafts blog posts, social copy, and landing content",
        icon="✍️",
    ),
    AgentStep(
        id="editor",
        name="Algen Editor",
        tagline="Sharpens tone, structure, and calls to action",
        icon="📝",
    ),
    AgentStep(
        id="seo",
        name="Algen SEO Agent",
        tagline="Optimizes keywords, meta copy, and search readiness",
        icon="🔍",
    ),
    AgentStep(
        id="review",
        name="Publish Gate",
        tagline="Human approval before anything goes live",
        icon="✅",
    ),
]


@dataclass
class PipelineState:
    brief: str = ""
    plan: CampaignPlan | None = None
    drafts: list[DraftPiece] = field(default_factory=list)
    edited: list[EditedPiece] = field(default_factory=list)
    seo: list[SeoOptimizedPiece] = field(default_factory=list)
    published: bool = False
    step_index: int = 0  # next step to run (0 = planner)
    metrics: RunMetrics = field(default_factory=RunMetrics)

    def to_package(self) -> CampaignPackage:
        return CampaignPackage(
            plan=self.plan or CampaignPlan(
                campaign_name="Untitled",
                audience="",
                goal="",
                tone="",
                subtasks=[],
            ),
            drafts=self.drafts,
            edited=self.edited,
            seo=self.seo,
            published=self.published,
        )

    def step_status(self, index: int) -> str:
        if index < self.step_index:
            return "done"
        if index == self.step_index:
            return "active"
        return "pending"


async def run_pipeline_step(state: PipelineState) -> PipelineState:
    """Run exactly one agent step, then advance step_index."""
    if state.step_index >= len(AGENT_STEPS):
        return state

    step = AGENT_STEPS[state.step_index]
    t0 = time.perf_counter()

    if step.id == "planner":
        state.plan = await plan_campaign(state.brief)
        state.metrics.record("Algen Planner", time.perf_counter() - t0)

    elif step.id == "copywriter":
        if not state.plan:
            raise RuntimeError("Planner must run first")
        state.drafts = []
        for subtask in state.plan.subtasks:
            t1 = time.perf_counter()
            draft = await draft_for_subtask(subtask, state.plan)
            state.drafts.append(draft)
            state.metrics.record(
                f"Algen Copywriter · {subtask.channel.value}",
                time.perf_counter() - t1,
            )

    elif step.id == "editor":
        if not state.drafts:
            raise RuntimeError("Copywriter must run first")
        state.edited = []
        for draft in state.drafts:
            t1 = time.perf_counter()
            edited = await edit_draft(draft, state.plan)  # type: ignore[arg-type]
            state.edited.append(edited)
            state.metrics.record(
                f"Algen Editor · {draft.channel.value}",
                time.perf_counter() - t1,
            )

    elif step.id == "seo":
        if not state.edited:
            raise RuntimeError("Editor must run first")
        state.seo = []
        targets = [
            e for e in state.edited
            if e.channel in (ContentChannel.BLOG, ContentChannel.SEO)
        ]
        for piece in targets:
            t1 = time.perf_counter()
            optimized = await optimize_seo(piece, state.plan)  # type: ignore[arg-type]
            state.seo.append(optimized)
            state.metrics.record(
                f"Algen SEO · {piece.channel.value}",
                time.perf_counter() - t1,
            )

    elif step.id == "review":
        state.metrics.record("Publish Gate", time.perf_counter() - t0)

    state.step_index += 1
    return state


async def run_autopilot(state: PipelineState) -> PipelineState:
    """Run all remaining agent steps without pausing."""
    while state.step_index < len(AGENT_STEPS) - 1:  # stop before review gate
        state = await run_pipeline_step(state)
    return state
