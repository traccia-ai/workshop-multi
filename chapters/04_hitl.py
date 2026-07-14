"""Chapter 04 — Human-in-the-Loop Review.

Run: python chapters/04_hitl.py
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from marketing_team.config import init_observability
from marketing_team.orchestration import run_campaign

SAMPLE_BRIEF = """
Campaign for Algen Academy Course 3 (multi-agent systems).
Audience: senior engineers. Goal: waitlist signups. Tone: practical.
Produce blog, social, and SEO pieces — then pause for human approval.
""".strip()


async def main() -> None:
    init_observability()
    print("Running parallel pipeline, then pausing for your approval...\n")
    package, metrics = await run_campaign(
        SAMPLE_BRIEF,
        mode="parallel",
        require_approval=True,
    )
    print("\n=== REVIEW RESULT ===")
    print(package.review)
    print(f"Published: {package.published}")
    print("\nTiming:")
    print(metrics.summary())


if __name__ == "__main__":
    asyncio.run(main())
