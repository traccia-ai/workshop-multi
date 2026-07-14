"""Chapter 06 — Observability for Multi-Agents (Traccia).

Run: python chapters/06_observability.py

Narrative for instructors:
  1. Run WITHOUT traccia first (comment init) — hard to see which agent failed.
  2. Enable init_observability() — every agent/LLM call is traced.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from marketing_team.config import init_observability
from marketing_team.orchestration import plan_campaign

SAMPLE_BRIEF = """
Plan a tiny campaign for Algen Academy Course 3 multi-agent workshop.
Audience: senior engineers. Goal: waitlist. Tone: practical.
""".strip()


async def main() -> None:
    # One line — Traccia auto-instruments OpenAI Agents SDK.
    init_observability(console=True)

    print("Watch the console traces: planner → LLM spans → tokens/latency.\n")
    plan = await plan_campaign(SAMPLE_BRIEF)
    print(f"\nPlan ready: {plan.campaign_name} ({len(plan.subtasks)} subtasks)")
    print(
        "\nIn production you would export the same spans to Traccia Cloud / "
        "Grafana Tempo / Jaeger via OTLP — concepts stay the same."
    )


if __name__ == "__main__":
    asyncio.run(main())
