"""Chapter 05 — Scaling and Performance (sequential vs parallel).

Run: python chapters/05_parallel.py
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from marketing_team.config import init_observability
from marketing_team.orchestration import RunMetrics, run_parallel, run_sequential

SAMPLE_BRIEF = """
Short campaign for Algen Academy Course 3.
Audience: engineers. Goal: demo signups. Tone: clear and credible.
""".strip()


async def main() -> None:
    init_observability()

    seq_metrics = RunMetrics()
    print("→ Running SEQUENTIAL pipeline...")
    await run_sequential(SAMPLE_BRIEF, seq_metrics)
    print("Sequential timing:")
    print(seq_metrics.summary())

    par_metrics = RunMetrics()
    print("\n→ Running PARALLEL pipeline...")
    await run_parallel(SAMPLE_BRIEF, par_metrics)
    print("Parallel timing:")
    print(par_metrics.summary())

    if seq_metrics.total_seconds > 0:
        speedup = seq_metrics.total_seconds / max(par_metrics.total_seconds, 0.001)
        print(f"\nApprox speedup: {speedup:.2f}x")
        print(
            "Trade-off: parallel is faster wall-clock but can raise peak cost "
            "and make traces harder to read — observability matters more."
        )


if __name__ == "__main__":
    asyncio.run(main())
