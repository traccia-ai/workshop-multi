"""Algen Multi Agent Marketing System — product UI."""

from __future__ import annotations

import asyncio
import json

import streamlit as st

from marketing_team.config import get_model_name, init_observability
from marketing_team.models import ContentChannel, ReviewDecision
from marketing_team.pipeline import AGENT_STEPS, PipelineState, run_autopilot, run_pipeline_step

st.set_page_config(
    page_title="Algen Multi Agent Marketing System",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

DEFAULT_BRIEF = (
    "Launch a thought-leadership campaign for Algen Academy's advanced multi-agent systems program. "
    "Audience: senior engineers and AI architects in India. "
    "Goal: drive qualified waitlist signups. "
    "Tone: credible, practical, outcome-focused."
)


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        #MainMenu, footer, header { visibility: hidden; }
        .block-container { padding-top: 1.5rem; padding-bottom: 2rem; max-width: 1180px; }

        div[data-testid="stSidebar"] {
            background: #0B1220;
        }
        div[data-testid="stSidebar"] * { color: #E5E7EB !important; }
        div[data-testid="stSidebar"] .stCaption { color: #94A3B8 !important; }

        .agent-box {
            border: 1px solid #D8DEE9;
            border-radius: 12px;
            padding: 14px 14px 14px 16px;
            background: #FFFFFF;
            min-height: 138px;
            box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
            border-left: 4px solid #CBD5E1;
        }
        .agent-box-active {
            border-color: #C7D2FE;
            border-left: 4px solid #1E1B4B;
            background: #FFFFFF;
            box-shadow: 0 8px 20px rgba(30, 27, 75, 0.10);
        }
        .agent-box-done {
            border-color: #D1D5DB;
            border-left: 4px solid #0F172A;
            background: #FFFFFF;
        }
        .agent-box-pending {
            border-color: #E5E7EB;
            border-left: 4px solid #E5E7EB;
            background: #FAFBFC;
            box-shadow: none;
        }
        .agent-box-pending .agent-title,
        .agent-box-pending .agent-desc {
            color: #94A3B8 !important;
        }
        .agent-label {
            display: inline-block;
            font-size: 10px;
            font-weight: 700;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            margin-top: 10px;
            padding: 3px 8px;
            border-radius: 999px;
        }
        .label-pending { color: #64748B; background: #F1F5F9; }
        .label-active { color: #FFFFFF; background: #1E1B4B; }
        .label-done { color: #FFFFFF; background: #0F172A; }
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_resource
def _boot_observability() -> bool:
    init_observability(console=True)
    return True


def init_session() -> None:
    if "pipeline" not in st.session_state:
        st.session_state.pipeline = None
    if "autopilot" not in st.session_state:
        st.session_state.autopilot = False


def reset_pipeline(brief: str) -> None:
    st.session_state.pipeline = PipelineState(brief=brief.strip(), step_index=0)


def render_agent_rail(state: PipelineState) -> None:
    cols = st.columns(len(AGENT_STEPS))
    for i, (col, step) in enumerate(zip(cols, AGENT_STEPS)):
        status = state.step_status(i)
        css = {
            "pending": "agent-box agent-box-pending",
            "active": "agent-box agent-box-active",
            "done": "agent-box agent-box-done",
        }[status]
        label_css = f"label-{status}"
        with col:
            st.markdown(
                f"""
                <div class="{css}">
                    <div style="font-size:18px;line-height:1;">{step.icon}</div>
                    <div class="agent-title" style="font-weight:700;font-size:13px;margin-top:8px;color:#0F172A;">{step.name}</div>
                    <div class="agent-desc" style="font-size:12px;color:#64748B;margin-top:4px;line-height:1.4;">{step.tagline}</div>
                    <div class="agent-label {label_css}">{status}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def channel_label(channel: ContentChannel) -> str:
    return {
        ContentChannel.BLOG: "Blog",
        ContentChannel.SOCIAL: "Social",
        ContentChannel.SEO: "Landing page",
    }[channel]


def render_outputs(state: PipelineState) -> None:
    if state.plan and state.step_index >= 1:
        with st.container(border=True):
            st.markdown(f"### {AGENT_STEPS[0].icon} {AGENT_STEPS[0].name}")
            st.caption(AGENT_STEPS[0].tagline)
            st.write(f"**Campaign:** {state.plan.campaign_name}")
            st.write(f"**Audience:** {state.plan.audience}")
            st.write(f"**Goal:** {state.plan.goal}")
            st.write(f"**Tone:** {state.plan.tone}")
            st.markdown("**Tasks**")
            for task in state.plan.subtasks:
                st.markdown(f"- **{channel_label(task.channel)}** — {task.title}: _{task.brief}_")

    if state.drafts and state.step_index >= 2:
        with st.container(border=True):
            st.markdown(f"### {AGENT_STEPS[1].icon} {AGENT_STEPS[1].name}")
            st.caption(AGENT_STEPS[1].tagline)
            for d in state.drafts:
                st.markdown(f"**{channel_label(d.channel)} · {d.title}**")
                st.write(d.body)
                st.divider()

    if state.edited and state.step_index >= 3:
        with st.container(border=True):
            st.markdown(f"### {AGENT_STEPS[2].icon} {AGENT_STEPS[2].name}")
            st.caption(AGENT_STEPS[2].tagline)
            for e in state.edited:
                st.markdown(f"**{channel_label(e.channel)} · {e.title}**")
                st.write(e.body)
                if e.changes_made:
                    st.caption("Edits: " + ", ".join(e.changes_made))

                if e.channel == ContentChannel.SOCIAL:
                    st.markdown("**Publish social**")
                    c1, c2 = st.columns(2)
                    with c1:
                        st.text_area(
                            "LinkedIn post",
                            e.body,
                            height=110,
                            key=f"li-{e.title}",
                        )
                        if st.button("Post to LinkedIn", key=f"btn-li-{e.title}", use_container_width=True):
                            st.toast("Queued for LinkedIn (demo)")
                    with c2:
                        x_body = e.body[:277] + ("…" if len(e.body) > 277 else "")
                        st.text_area("X post", x_body, height=110, key=f"x-{e.title}")
                        if st.button("Post on X", key=f"btn-x-{e.title}", use_container_width=True):
                            st.toast("Queued for X (demo)")
                st.divider()

    if state.seo and state.step_index >= 4:
        with st.container(border=True):
            st.markdown(f"### {AGENT_STEPS[3].icon} {AGENT_STEPS[3].name}")
            st.caption(AGENT_STEPS[3].tagline)
            for s in state.seo:
                st.markdown(f"**{channel_label(s.channel)} · {s.title}**")
                st.write(s.body)
                st.caption(
                    f"Keyword: {s.primary_keyword} · Meta: {s.meta_description}"
                )
                if st.button("Publish landing page", key=f"pub-{s.title}", use_container_width=True):
                    st.toast("Landing page published (demo)")
                st.divider()


def main() -> None:
    _boot_observability()
    inject_styles()
    init_session()

    with st.sidebar:
        st.markdown("### Algenbot")
        st.caption("Multi-agent marketing system")
        st.divider()
        st.session_state.autopilot = st.toggle(
            "Autopilot",
            value=st.session_state.autopilot,
            help="On = run all agents at once. Off = press Next for each agent.",
        )
        st.divider()
        st.caption("Model")
        st.code(get_model_name())
        st.caption("Tracing via Traccia")

    st.title("Algen Multi Agent Marketing System")
    st.caption("Powered by Algenbot — Planner, Copywriter, Editor & SEO agents as one team")

    state: PipelineState | None = st.session_state.pipeline

    if state is None:
        with st.container(border=True):
            st.subheader("New campaign")
            brief = st.text_area("Campaign brief", value=DEFAULT_BRIEF, height=130)
            if st.button("Start campaign", type="primary"):
                if not brief.strip():
                    st.error("Add a brief first.")
                else:
                    reset_pipeline(brief)
                    st.rerun()

        st.markdown("#### How it works")
        c1, c2, c3 = st.columns(3)
        c1.info("**Step by step**\n\nEach agent runs alone so you can see who did what.")
        c2.info("**Autopilot**\n\nTurn it on in the sidebar to run the full team without clicking Next.")
        c3.info("**Publish**\n\nApprove at the end, then use LinkedIn / X / landing buttons.")
        return

    # Active campaign
    render_agent_rail(state)

    top_l, top_r = st.columns([4, 1])
    with top_l:
        st.text_area(
            "Campaign brief",
            value=state.brief,
            height=90,
            disabled=True,
        )
    with top_r:
        st.write("")
        st.write("")
        if st.button("Reset", use_container_width=True):
            st.session_state.pipeline = None
            st.rerun()

    render_outputs(state)

    finished = state.step_index >= len(AGENT_STEPS)
    at_review = state.step_index == len(AGENT_STEPS) - 1

    if state.step_index < len(AGENT_STEPS) - 1:
        next_step = AGENT_STEPS[state.step_index]
        with st.container(border=True):
            st.markdown(f"**Up next:** {next_step.icon} {next_step.name}")
            st.caption(next_step.tagline)

            if st.session_state.autopilot:
                if st.button("Run all remaining agents", type="primary"):
                    with st.spinner("Algenbot is running the pipeline…"):
                        state = asyncio.run(run_autopilot(state))
                    st.session_state.pipeline = state
                    st.rerun()
            else:
                if st.button(f"Run {next_step.name} →", type="primary"):
                    with st.spinner(f"{next_step.name} is working…"):
                        state = asyncio.run(run_pipeline_step(state))
                    st.session_state.pipeline = state
                    st.rerun()

    if at_review or finished:
        with st.container(border=True):
            st.markdown(f"### {AGENT_STEPS[4].icon} {AGENT_STEPS[4].name}")
            st.caption(AGENT_STEPS[4].tagline)

            if not state.published:
                a, b = st.columns(2)
                if a.button("Approve campaign", type="primary", use_container_width=True):
                    state.published = True
                    state.step_index = len(AGENT_STEPS)
                    st.session_state.pipeline = state
                    st.rerun()
                note = b.text_input("Or request revisions")
                if b.button("Send back", use_container_width=True) and note:
                    st.warning(f"Held: {note}")
            else:
                st.success("Campaign approved. Use the publish buttons above, or export the package.")
                st.download_button(
                    "Export campaign JSON",
                    data=json.dumps(state.to_package().model_dump(mode="json"), indent=2),
                    file_name="algen_campaign.json",
                    mime="application/json",
                )
                if state.metrics.steps:
                    with st.expander("Timing"):
                        st.code(state.metrics.summary())


if __name__ == "__main__":
    main()
