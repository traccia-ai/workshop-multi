"""Chapter 07 — Final Integration (end-to-end campaign).

Run: python chapters/07_integration.py
"""

from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from marketing_team.config import init_observability
from marketing_team.orchestration import run_campaign

OUTPUT_DIR = Path(__file__).resolve().parents[1] / "outputs"

SAMPLE_BRIEF = """
Full campaign for Algen Academy Course 3: Designing Multi-Agent AI Systems.
Audience: senior engineers and AI architects in India.
Goal: cohort waitlist signups for the next Saturday demo / workshop.
Tone: credible, hands-on, outcome-focused — no hype.
Deliver blog, social, and SEO landing copy. Require human approval before publish.
""".strip()


async def main() -> None:
    init_observability()
    OUTPUT_DIR.mkdir(exist_ok=True)

    package, metrics = await run_campaign(
        SAMPLE_BRIEF,
        mode="parallel",
        require_approval=True,
    )

    out = OUTPUT_DIR / "campaign_package.json"
    out.write_text(json.dumps(package.model_dump(mode="json"), indent=2))
    print(f"\nSaved package → {out}")
    print("Timing:")
    print(metrics.summary())
    if package.published:
        print("\n✅ Approved — ready to show as the end-product trailer.")
    else:
        print("\n⏸ Held for revisions — feedback:", package.review)


if __name__ == "__main__":
    asyncio.run(main())
