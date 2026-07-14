"""Marketing Agent Team — Planner + Copywriter + Editor + SEO specialist.

Uses the OpenAI Agents SDK with Groq (OpenAI-compatible endpoint).
Structured outputs are parsed from JSON text (Groq json_schema mode is flaky).
"""

from __future__ import annotations

from agents import Agent

from marketing_team.config import get_model

JSON_RULE = "Return ONLY a raw JSON object. No markdown fences, no extra text."

PLANNER_INSTRUCTIONS = f"""
You are the Campaign Planner for a marketing agent team.

Given a campaign brief, produce a structured plan with:
- campaign_name, audience, goal, tone
- exactly 3 subtasks: one blog, one social, one seo

Each subtask needs: id, channel, title, brief, priority.
channel must be exactly one of: blog, social, seo
priority must be one of: high, medium, low

{JSON_RULE}
""".strip()

COPYWRITER_INSTRUCTIONS = f"""
You are a marketing Copywriter.

Write compelling, on-brand content for the assigned channel.
Return JSON with: channel, title, body, notes.
channel must be: blog, social, or seo.
Blog: 250-400 words. Social: 1-3 short posts.

{JSON_RULE}
""".strip()

EDITOR_INSTRUCTIONS = f"""
You are a sharp marketing Editor.

Improve clarity, tone, and structure of the draft.
Return JSON with: channel, title, body, changes_made (list of strings).
Do not invent new product claims that were not in the draft.

{JSON_RULE}
""".strip()

SEO_INSTRUCTIONS = f"""
You are an SEO specialist.

Optimize content for search without killing readability.
Return JSON with: channel, title, body, primary_keyword,
secondary_keywords (list of 3-5 strings), meta_description (max 155 chars).

{JSON_RULE}
""".strip()


def build_planner() -> Agent:
    return Agent(
        name="Planner",
        instructions=PLANNER_INSTRUCTIONS,
        model=get_model(),
    )


def build_copywriter() -> Agent:
    return Agent(
        name="Copywriter",
        instructions=COPYWRITER_INSTRUCTIONS,
        model=get_model(),
    )


def build_editor() -> Agent:
    return Agent(
        name="Editor",
        instructions=EDITOR_INSTRUCTIONS,
        model=get_model(),
    )


def build_seo() -> Agent:
    return Agent(
        name="SEO Specialist",
        instructions=SEO_INSTRUCTIONS,
        model=get_model(),
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
