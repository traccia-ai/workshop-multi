"""Chapter 02 — Building the Planner Agent.

Run: python chapters/02_planner.py
"""

from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from marketing_team.agents import build_planner
from marketing_team.config import init_observability
from marketing_team.orchestration import plan_campaign

SAMPLE_BRIEF = """
Launch a 2-week campaign for Algen Academy's Course 3:
"Designing Multi-Agent AI Systems" for senior engineers in India.
Goal: get waitlist signups for the next cohort.
Tone: credible, practical, not hypey.
Need: one blog outline/post, social posts, and SEO-focused landing copy.
""".strip()


async def main() -> None:
    init_observability()
    planner = build_planner()
    print(f"Agent: {planner.name}")
    print(f"Output type: {planner.output_type.__name__}")
    print("\nBrief:\n", SAMPLE_BRIEF, "\n")

    plan = await plan_campaign(SAMPLE_BRIEF)
    print("=== CAMPAIGN PLAN ===")
    print(json.dumps(plan.model_dump(mode="json"), indent=2))
    print(f"\nSubtasks planned: {len(plan.subtasks)}")


if __name__ == "__main__":
    asyncio.run(main())
