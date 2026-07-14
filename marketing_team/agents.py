"""Marketing Agent Team — Planner + Copywriter + Editor + SEO specialist.

Uses the OpenAI Agents SDK with Gemini (OpenAI-compatible endpoint).
Orchestration style: code-driven sequential / parallel + agents-as-tools.
"""

from __future__ import annotations

from agents import Agent

from marketing_team.config import get_model
from marketing_team.models import CampaignPlan, DraftPiece, EditedPiece, SeoOptimizedPiece


PLANNER_INSTRUCTIONS = """
You are the Campaign Planner for a marketing agent team.

Given a campaign brief, produce a structured plan with:
- campaign_name, audience, goal, tone
- 3 subtasks (exactly one blog, one social, one seo) with clear briefs

Keep briefs concrete and short so specialist agents can execute them.
""".strip()

COPYWRITER_INSTRUCTIONS = """
You are a marketing Copywriter.

Write compelling, on-brand content for the assigned channel.
Return structured output: channel, title, body, and optional notes.
Blog: 250–400 words. Social: 1–3 short posts. Stay faithful to the brief.
""".strip()

EDITOR_INSTRUCTIONS = """
You are a sharp marketing Editor.

Improve clarity, tone, and structure of the draft. Fix fluff and weak CTAs.
Return structured output with channel, title, body, and a short list of changes_made.
Do not invent new product claims that were not in the draft.
""".strip()

SEO_INSTRUCTIONS = """
You are an SEO specialist.

Optimize the content for search without killing readability.
Return structured output: channel, title, body, primary_keyword,
secondary_keywords (3–5), and a meta_description (<=155 chars).
""".strip()


def build_planner() -> Agent:
    return Agent(
        name="Planner",
        instructions=PLANNER_INSTRUCTIONS,
        model=get_model(),
        output_type=CampaignPlan,
    )


def build_copywriter() -> Agent:
    return Agent(
        name="Copywriter",
        instructions=COPYWRITER_INSTRUCTIONS,
        model=get_model(),
        output_type=DraftPiece,
    )


def build_editor() -> Agent:
    return Agent(
        name="Editor",
        instructions=EDITOR_INSTRUCTIONS,
        model=get_model(),
        output_type=EditedPiece,
    )


def build_seo() -> Agent:
    return Agent(
        name="SEO Specialist",
        instructions=SEO_INSTRUCTIONS,
        model=get_model(),
        output_type=SeoOptimizedPiece,
    )


def build_manager_with_tools() -> Agent:
    """LLM-orchestrated manager that calls specialists as tools (delegation pattern)."""
    copywriter = build_copywriter()
    editor = build_editor()
    seo = build_seo()

    return Agent(
        name="Marketing Manager",
        instructions=(
            "You manage a marketing content team. For a campaign brief:\n"
            "1) Call Copywriter to draft blog or social content.\n"
            "2) Call Editor to polish the draft.\n"
            "3) Call SEO Specialist when the piece needs search optimization.\n"
            "Synthesize a final package the human can review. Be concise."
        ),
        model=get_model(),
        tools=[
            copywriter.as_tool(
                tool_name="run_copywriter",
                tool_description="Draft marketing content for a channel brief.",
            ),
            editor.as_tool(
                tool_name="run_editor",
                tool_description="Edit and improve a content draft.",
            ),
            seo.as_tool(
                tool_name="run_seo",
                tool_description="Optimize content for SEO and keywords.",
            ),
        ],
    )
