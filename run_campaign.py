#!/usr/bin/env python3
"""CLI entrypoint — run a full marketing campaign from a brief.

Usage:
  python run_campaign.py
  python run_campaign.py --mode sequential
  python run_campaign.py --no-approval
  python run_campaign.py --brief "Launch X for Y"
"""

from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path

from marketing_team.config import init_observability
from marketing_team.orchestration import run_campaign

DEFAULT_BRIEF = """
Launch a campaign for Algen Academy Course 3: Designing Multi-Agent AI Systems.
Audience: senior engineers. Goal: waitlist signups. Tone: practical and credible.
""".strip()


async def _amain(args: argparse.Namespace) -> None:
    init_observability()
    package, metrics = await run_campaign(
        args.brief,
        mode=args.mode,
        require_approval=not args.no_approval,
    )

    out_dir = Path("outputs")
    out_dir.mkdir(exist_ok=True)
    path = out_dir / "last_campaign.json"
    path.write_text(json.dumps(package.model_dump(mode="json"), indent=2))

    print("\n=== PACKAGE SUMMARY ===")
    print(f"Campaign: {package.plan.campaign_name}")
    print(f"Drafts: {len(package.drafts)} | Edited: {len(package.edited)} | SEO: {len(package.seo)}")
    print(f"Published: {package.published}")
    print(f"Saved: {path}")
    print("\nTiming:")
    print(metrics.summary())


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Marketing Agent Team")
    parser.add_argument("--brief", default=DEFAULT_BRIEF, help="Campaign brief text")
    parser.add_argument(
        "--mode",
        choices=["parallel", "sequential"],
        default="parallel",
        help="Orchestration mode",
    )
    parser.add_argument(
        "--no-approval",
        action="store_true",
        help="Skip human-in-the-loop review",
    )
    args = parser.parse_args()
    asyncio.run(_amain(args))


if __name__ == "__main__":
    main()
