"""Chapter 03 — Specialist Agents and Handoffs (agents-as-tools).

Run: python chapters/03_specialists.py
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agents import Runner

from marketing_team.agents import build_manager_with_tools
from marketing_team.config import init_observability

SAMPLE = """
Write a short LinkedIn post + a blog intro paragraph for Algen Academy
Course 3 (multi-agent systems). Audience: senior engineers. Tone: practical.
Use the copywriter, then the editor. Skip SEO for this short demo.
""".strip()


async def main() -> None:
    init_observability()
    manager = build_manager_with_tools()
    print(f"Manager: {manager.name}")
    print(f"Tools: {[t.name for t in manager.tools]}")
    print("\nRunning manager (specialists as tools)...\n")

    result = await Runner.run(manager, SAMPLE)
    print("=== FINAL OUTPUT ===")
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
