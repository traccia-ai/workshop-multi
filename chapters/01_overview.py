"""Chapter 01 — Multi-Agent System Overview (no API calls).

Run: python chapters/01_overview.py
"""

from __future__ import annotations

ARCHITECTURE = """
MARKETING AGENT TEAM — Architecture

                    ┌─────────────────┐
   Campaign Brief → │     PLANNER     │  breaks work into subtasks
                    └────────┬────────┘
                             │ delegates
           ┌─────────────────┼─────────────────┐
           ▼                 ▼                 ▼
    ┌────────────┐    ┌────────────┐    ┌────────────┐
    │ COPYWRITER │    │   EDITOR   │    │    SEO     │
    └────────────┘    └────────────┘    └────────────┘
           │                 │                 │
           └─────────────────┼─────────────────┘
                             ▼
                    ┌─────────────────┐
                    │  HUMAN REVIEW  │  approve / request changes
                    └────────┬────────┘
                             ▼
                         PUBLISH

Orchestration strategies you will use today:
  1. Sequential  — one agent after another (simple, slower)
  2. Parallel    — independent specialists run together (faster, more cost)
  3. Delegation  — manager agent calls specialists as tools (LLM decides)
"""

PATTERNS = {
    "planner / specialist": "One agent plans; specialists execute narrow jobs.",
    "agents as tools": "Manager keeps control; specialists are bounded tools.",
    "handoffs": "Control transfers to a specialist for the rest of the turn.",
    "human-in-the-loop": "Pause before irreversible actions (publish, spend, delete).",
}


def main() -> None:
    print(ARCHITECTURE)
    print("Key patterns:")
    for name, desc in PATTERNS.items():
        print(f"  • {name}: {desc}")
    print("\nNext: chapters/02_planner.py — build the Planner agent.")


if __name__ == "__main__":
    main()
