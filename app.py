"""Streamlit UI — single interface for the Marketing Agent Team.

Run locally:
  streamlit run app.py

Deploy: push to GitHub → Streamlit Community Cloud → select app.py
"""

from __future__ import annotations

import asyncio
import json

import streamlit as st

from marketing_team.config import init_observability, get_model_name
from marketing_team.orchestration import run_campaign

st.set_page_config(
    page_title="Marketing Agent Team | Algen Academy",
    page_icon="✦",
    layout="wide",
)

DEFAULT_BRIEF = (
    "Launch a campaign for Algen Academy Course 3: Designing Multi-Agent AI Systems. "
    "Audience: senior engineers in India. Goal: waitlist signups for the next cohort. "
    "Tone: credible, practical, hands-on — not hypey."
)


@st.cache_resource
def _boot_observability() -> bool:
    init_observability(console=True)
    return True


def main() -> None:
    _boot_observability()

    st.title("Marketing Agent Team")
    st.caption(
        f"Course 3 demo · Planner → Copywriter → Editor → SEO · model: `{get_model_name()}`"
    )

    with st.sidebar:
        st.header("Controls")
        mode = st.radio("Orchestration", ["parallel", "sequential"], index=0)
        require_approval = st.checkbox("Human review before publish", value=True)
        st.markdown("---")
        st.markdown(
            "Agents: **Planner**, **Copywriter**, **Editor**, **SEO**.\n\n"
            "Traces: Traccia (console / OTLP)."
        )

    brief = st.text_area("Campaign brief", value=DEFAULT_BRIEF, height=140)
    run = st.button("Run campaign", type="primary", use_container_width=True)

    if "package" not in st.session_state:
        st.session_state.package = None
        st.session_state.metrics = None

    if run:
        if not brief.strip():
            st.error("Enter a campaign brief.")
            return
        with st.spinner(f"Running {mode} pipeline…"):
            package, metrics = asyncio.run(
                run_campaign(
                    brief.strip(),
                    mode=mode,
                    require_approval=False,  # Streamlit handles approval in UI
                )
            )
        st.session_state.package = package
        st.session_state.metrics = metrics

    package = st.session_state.package
    metrics = st.session_state.metrics
    if not package:
        st.info("Paste a brief and run the campaign to see the team work.")
        return

    st.subheader(package.plan.campaign_name)
    c1, c2, c3 = st.columns(3)
    c1.metric("Audience", package.plan.audience[:40] + ("…" if len(package.plan.audience) > 40 else ""))
    c2.metric("Subtasks", len(package.plan.subtasks))
    c3.metric("Wall time", f"{metrics.total_seconds}s" if metrics else "—")

    with st.expander("Plan (JSON)", expanded=False):
        st.json(package.plan.model_dump(mode="json"))

    tabs = st.tabs(["Drafts", "Edited", "SEO", "Review"])
    with tabs[0]:
        for d in package.drafts:
            st.markdown(f"### {d.title}")
            st.caption(d.channel.value)
            st.write(d.body)
    with tabs[1]:
        for e in package.edited:
            st.markdown(f"### {e.title}")
            st.caption(e.channel.value)
            st.write(e.body)
            if e.changes_made:
                st.write("Changes:", ", ".join(e.changes_made))
    with tabs[2]:
        for s in package.seo:
            st.markdown(f"### {s.title}")
            st.caption(f"{s.channel.value} · keyword: `{s.primary_keyword}`")
            st.write(s.body)
            st.write("Meta:", s.meta_description)
    with tabs[3]:
        if require_approval and not package.published:
            st.warning("Awaiting human approval before publish.")
            col_a, col_b = st.columns(2)
            if col_a.button("Approve & publish", type="primary"):
                package.published = True
                from marketing_team.models import ReviewDecision

                package.review = ReviewDecision(approved=True, feedback="")
                st.session_state.package = package
                st.success("Published (demo).")
                st.rerun()
            feedback = col_b.text_input("Or request changes")
            if col_b.button("Request revisions") and feedback:
                from marketing_team.models import ReviewDecision

                package.review = ReviewDecision(approved=False, feedback=feedback)
                package.published = False
                st.session_state.package = package
                st.info(f"Held: {feedback}")
        elif package.published:
            st.success("Approved for publish.")
        else:
            st.write(package.review)

    if metrics:
        st.markdown("#### Timing")
        st.code(metrics.summary())

    st.download_button(
        "Download package JSON",
        data=json.dumps(package.model_dump(mode="json"), indent=2),
        file_name="campaign_package.json",
        mime="application/json",
    )


if __name__ == "__main__":
    main()
