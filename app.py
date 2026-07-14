"""Streamlit UI — Marketing Agent Team demo."""

from __future__ import annotations

import asyncio
import html
import json

import streamlit as st

from marketing_team.config import get_model_name, init_observability
from marketing_team.models import CampaignPackage, ContentChannel, ReviewDecision
from marketing_team.orchestration import run_campaign

st.set_page_config(
    page_title="Marketing Agent Team",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

DEFAULT_BRIEF = (
    "Launch a campaign for Algen Academy Course 3: Designing Multi-Agent AI Systems. "
    "Audience: senior engineers in India. Goal: waitlist signups for the next cohort. "
    "Tone: credible, practical, hands-on — not hypey."
)

PIPELINE = ["Planner", "Copywriter", "Editor", "SEO", "Review"]

CHANNEL_COLORS = {
    ContentChannel.BLOG: ("Blog", "#5B5EF7"),
    ContentChannel.SOCIAL: ("Social", "#0EA5E9"),
    ContentChannel.SEO: ("SEO", "#10B981"),
}


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        #MainMenu, footer, header { visibility: hidden; }
        .block-container {
            padding: 1.25rem 2rem 2.5rem 2rem;
            max-width: 1280px;
        }
        .topbar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
            margin-bottom: 1.5rem;
            flex-wrap: wrap;
        }
        .topbar-title {
            font-size: 1.55rem;
            font-weight: 700;
            color: #111827;
            margin: 0;
        }
        .topbar-sub {
            color: #6B7280;
            font-size: 0.92rem;
            margin: 0.15rem 0 0 0;
        }
        .pipeline {
            display: flex;
            align-items: center;
            gap: 0.35rem;
            flex-wrap: wrap;
        }
        .step {
            background: #fff;
            border: 1px solid #E5E7EB;
            color: #374151;
            font-size: 0.78rem;
            font-weight: 600;
            padding: 0.35rem 0.7rem;
            border-radius: 8px;
        }
        .arrow { color: #9CA3AF; font-size: 0.8rem; }
        .panel {
            background: #fff;
            border: 1px solid #E5E7EB;
            border-radius: 16px;
            padding: 1.25rem 1.35rem;
            margin-bottom: 1rem;
            box-shadow: 0 1px 2px rgba(17, 24, 39, 0.04);
        }
        .panel-title {
            font-size: 0.95rem;
            font-weight: 700;
            color: #111827;
            margin: 0 0 0.85rem 0;
        }
        .info-grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 0.75rem;
            margin-bottom: 1rem;
        }
        @media (min-width: 900px) {
            .info-grid { grid-template-columns: repeat(4, minmax(0, 1fr)); }
        }
        .info-item {
            background: #F9FAFB;
            border: 1px solid #E5E7EB;
            border-radius: 12px;
            padding: 0.85rem 0.95rem;
            min-height: 88px;
        }
        .info-label {
            font-size: 0.72rem;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            color: #6B7280;
            font-weight: 600;
            margin-bottom: 0.35rem;
        }
        .info-value {
            font-size: 0.92rem;
            color: #111827;
            line-height: 1.45;
            word-break: break-word;
        }
        .content-card {
            background: #fff;
            border: 1px solid #E5E7EB;
            border-radius: 14px;
            padding: 1.1rem 1.2rem;
            margin-bottom: 0.85rem;
        }
        .badge {
            display: inline-block;
            font-size: 0.68rem;
            font-weight: 700;
            letter-spacing: 0.03em;
            text-transform: uppercase;
            color: #fff;
            padding: 0.2rem 0.55rem;
            border-radius: 6px;
            margin-bottom: 0.45rem;
        }
        .card-title {
            font-size: 1rem;
            font-weight: 700;
            color: #111827;
            margin: 0 0 0.55rem 0;
        }
        .card-body {
            color: #374151;
            font-size: 0.92rem;
            line-height: 1.65;
            white-space: pre-wrap;
        }
        .card-meta {
            margin-top: 0.75rem;
            padding-top: 0.75rem;
            border-top: 1px solid #F3F4F6;
            color: #4B5563;
            font-size: 0.86rem;
            line-height: 1.5;
        }
        .status-wait {
            background: #FFFBEB;
            border: 1px solid #FDE68A;
            border-radius: 12px;
            padding: 1rem 1.1rem;
            color: #92400E;
        }
        .status-done {
            background: #ECFDF5;
            border: 1px solid #A7F3D0;
            border-radius: 12px;
            padding: 1rem 1.1rem;
            color: #065F46;
        }
        .empty {
            text-align: center;
            padding: 3rem 1.5rem;
            color: #6B7280;
        }
        .empty h3 {
            color: #111827;
            margin-bottom: 0.35rem;
        }
        div[data-testid="stSidebar"] {
            background: #1F2937;
        }
        div[data-testid="stSidebar"] h3, div[data-testid="stSidebar"] p, div[data-testid="stSidebar"] label {
            color: #F3F4F6 !important;
        }
        div[data-testid="stSidebar"] .stCaption, div[data-testid="stSidebar"] code {
            color: #D1D5DB !important;
        }
        div[data-testid="stSidebar"] hr {
            border-color: #374151 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_resource
def _boot_observability() -> bool:
    init_observability(console=True)
    return True


def esc(text: str) -> str:
    return html.escape(text)


def render_header() -> None:
    steps = ""
    for i, name in enumerate(PIPELINE):
        if i:
            steps += '<span class="arrow">›</span>'
        steps += f'<span class="step">{name}</span>'

    st.markdown(
        f"""
        <div class="topbar">
            <div>
                <p class="topbar-title">Marketing Agent Team</p>
                <p class="topbar-sub">Algen Academy · Course 3 demo</p>
            </div>
            <div class="pipeline">{steps}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_info_grid(package: CampaignPackage) -> None:
    plan = package.plan
    items = [
        ("Audience", plan.audience),
        ("Goal", plan.goal),
        ("Tone", plan.tone),
        ("Pieces", str(len(package.drafts))),
    ]
    cells = "".join(
        f"""
        <div class="info-item">
            <div class="info-label">{esc(label)}</div>
            <div class="info-value">{esc(value)}</div>
        </div>
        """
        for label, value in items
    )
    st.markdown(f'<div class="info-grid">{cells}</div>', unsafe_allow_html=True)


def render_piece(title: str, channel: ContentChannel, body: str, meta: str = "") -> None:
    label, color = CHANNEL_COLORS[channel]
    meta_html = f'<div class="card-meta">{meta}</div>' if meta else ""
    st.markdown(
        f"""
        <div class="content-card">
            <span class="badge" style="background:{color};">{label}</span>
            <div class="card-title">{esc(title)}</div>
            <div class="card-body">{esc(body)}</div>
            {meta_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_empty() -> None:
    st.markdown(
        """
        <div class="panel empty">
            <h3>No campaign yet</h3>
            <p>Write a brief below and hit Run campaign.<br>
            The planner and specialist agents will fill this section with results.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_review(package: CampaignPackage, require_approval: bool) -> None:
    if require_approval and not package.published:
        st.markdown(
            '<div class="status-wait"><strong>Awaiting your approval</strong><br>'
            "Agents are done. Review the content, then approve or send back.</div>",
            unsafe_allow_html=True,
        )
        c1, c2 = st.columns(2)
        if c1.button("Approve & publish", type="primary", use_container_width=True):
            package.published = True
            package.review = ReviewDecision(approved=True, feedback="")
            st.session_state.package = package
            st.rerun()
        with c2:
            feedback = st.text_input("Feedback", placeholder="What should change?", label_visibility="collapsed")
            if st.button("Request revisions", use_container_width=True) and feedback:
                package.review = ReviewDecision(approved=False, feedback=feedback)
                package.published = False
                st.session_state.package = package
                st.warning(feedback)
    elif package.published:
        st.markdown(
            '<div class="status-done"><strong>Approved for publish</strong><br>'
            "Campaign package is ready.</div>",
            unsafe_allow_html=True,
        )
    elif package.review:
        st.json(package.review.model_dump(mode="json"))


def main() -> None:
    _boot_observability()
    inject_styles()

    if "package" not in st.session_state:
        st.session_state.package = None
        st.session_state.metrics = None

    with st.sidebar:
        st.markdown("### Settings")
        mode = st.radio("Run mode", ["parallel", "sequential"], index=0)
        require_approval = st.checkbox("Human review", value=True)
        st.divider()
        st.caption("Model")
        st.code(get_model_name())
        st.caption("Traces go to console via Traccia")

    render_header()

    st.markdown('<div class="panel"><p class="panel-title">Campaign brief</p>', unsafe_allow_html=True)
    brief = st.text_area(
        "Brief",
        value=DEFAULT_BRIEF,
        height=130,
        label_visibility="collapsed",
    )
    st.markdown("</div>", unsafe_allow_html=True)

    run = st.button("Run campaign", type="primary", use_container_width=False)

    if run:
        if not brief.strip():
            st.error("Add a campaign brief first.")
        else:
            with st.spinner(f"Running {mode} pipeline — Planner → Copywriter → Editor → SEO…"):
                package, metrics = asyncio.run(
                    run_campaign(brief.strip(), mode=mode, require_approval=False)
                )
            st.session_state.package = package
            st.session_state.metrics = metrics

    package = st.session_state.package
    metrics = st.session_state.metrics

    st.markdown("---")

    if not package:
        render_empty()
        return

    st.markdown(f"### {package.plan.campaign_name}")
    render_info_grid(package)

    with st.expander("View campaign plan"):
        for task in package.plan.subtasks:
            label, _ = CHANNEL_COLORS[task.channel]
            st.markdown(f"**{task.title}** · {label}")
            st.caption(task.brief)

    tabs = st.tabs(["Drafts", "Edited", "SEO", "Review", "Export"])

    with tabs[0]:
        for d in package.drafts:
            render_piece(d.title, d.channel, d.body)

    with tabs[1]:
        for e in package.edited:
            meta = ""
            if e.changes_made:
                meta = "<strong>Edits:</strong> " + esc(", ".join(e.changes_made))
            render_piece(e.title, e.channel, e.body, meta)

    with tabs[2]:
        for s in package.seo:
            kw = ", ".join(s.secondary_keywords) if s.secondary_keywords else "—"
            meta = (
                f"<strong>Keyword:</strong> {esc(s.primary_keyword)}<br>"
                f"<strong>Also:</strong> {esc(kw)}<br>"
                f"<strong>Meta:</strong> {esc(s.meta_description)}"
            )
            render_piece(s.title, s.channel, s.body, meta)

    with tabs[3]:
        render_review(package, require_approval)

    with tabs[4]:
        if metrics:
            st.code(metrics.summary())
        st.download_button(
            "Download JSON",
            data=json.dumps(package.model_dump(mode="json"), indent=2),
            file_name="campaign_package.json",
            mime="application/json",
        )


if __name__ == "__main__":
    main()
