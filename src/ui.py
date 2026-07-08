import base64
import random
import time
from html import escape
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from src.leaderboard_store import (
    leaderboard_configured,
    leaderboard_rows,
    load_leaderboard,
    submit_to_leaderboard,
)
from src.scoring import mission_started


@st.cache_data(show_spinner=False)
def video_data_uri(video_path):
    video_bytes = Path(video_path).read_bytes()
    encoded = base64.b64encode(video_bytes).decode("ascii")
    return f"data:video/mp4;base64,{encoded}"


def render_styles():
    st.html(
        """
        <style>
        :root {
            --niagads-navy: #23313f;
            --niagads-navy-deep: #1d2a36;
            --niagads-gold: #ffc45c;
            --niagads-gold-deep: #f3aa34;
            --niagads-blue: #5f8fb8;
            --niagads-violet: #5d4bd8;
            --niagads-ink: #24313c;
            --niagads-muted: #647384;
            --niagads-line: #d8e0e7;
            --niagads-page: #f7f8fa;
        }
        .stApp {background: var(--niagads-page);}
        input,
        textarea,
        select,
        [data-baseweb="input"],
        [data-baseweb="textarea"],
        [data-baseweb="select"] {
            background-color: #ffffff !important;
            color: var(--niagads-ink) !important;
        }
        input::placeholder,
        textarea::placeholder {
            color: var(--niagads-muted) !important;
            opacity: 1;
        }
        .stButton > button:disabled,
        .stButton > button:disabled * {
            background-color: #edf1f4 !important;
            border-color: var(--niagads-line) !important;
            color: #425466 !important;
            opacity: 1;
        }
        header[data-testid="stHeader"],
        div[data-testid="stToolbar"] {
            display: none;
        }
        #MainMenu,
        footer {
            visibility: hidden;
        }
        section[data-testid="stSidebar"] {
            background: var(--niagads-navy-deep);
            border-right: 4px solid var(--niagads-gold);
        }
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] p {
            color: #eef3f7;
        }
        h1, h2, h3 {color: var(--niagads-ink);}
        .block-container {padding-top: 0.5rem;}
        .app-hero {
            background: var(--niagads-navy);
            border-top: 4px solid var(--niagads-gold);
            border-radius: 0;
            box-shadow: 0 8px 20px rgba(29, 42, 54, 0.12);
            margin: -0.50rem 0 0 0;
            overflow: hidden;
            padding: 2rem 2.25rem;
            position: relative;
        }
        .app-kicker {
            color: var(--niagads-gold);
            font-size: 0.88rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }
        .app-title {
            color: var(--niagads-gold);
            font-size: 2.25rem;
            font-weight: 800;
            line-height: 1.1;
            margin-top: 0.25rem;
        }
        .app-subtitle {
            color: #dce4eb;
            font-size: 1.02rem;
            line-height: 1.45;
            margin-top: 0.8rem;
            max-width: 48rem;
        }
        .landing-intro {
            margin: 0.5rem 0 0.75rem 0;
        }
        .landing-eyebrow {
            color: var(--niagads-navy-deep);
            font-size: 1rem;
            font-weight: 800;
            letter-spacing: 0.12em;
            margin-bottom: 0.28rem;
            text-transform: uppercase;
        }
        .landing-title {
            color: var(--niagads-ink);
            font-size: 2rem;
            font-weight: 800;
            line-height: 1.08;
            margin-top: 0.22rem;
        }
        .landing-copy {
            color: var(--niagads-muted);
            font-size: 1rem;
            line-height: 1.4;
            margin-top: 0.45rem;
        }
        .mobile-resource-note {
            background: #fff9e8;
            border-left: 4px solid var(--niagads-gold-deep);
            color: #70501a;
            display: none;
            font-size: 0.92rem;
            line-height: 1.35;
            margin-top: 0.65rem;
            padding: 0.55rem 0.7rem;
        }
        @media (max-width: 760px) {
            .mobile-resource-note {
                display: block;
            }
        }
        .landing-video-spacer {margin-top: 0.55rem;}
        .landing-video {
            background: #000000;
            border-radius: 8px;
            display: block;
            width: 100%;
        }
        .landing-action-spacer {margin-top: 0.55rem;}
        .stButton > button[kind="primary"] {
            background: var(--niagads-gold);
            border-color: var(--niagads-gold-deep);
            color: var(--niagads-ink);
            font-weight: 800;
        }
        .stButton > button[kind="primary"]:hover {
            background: #ffd37a;
            border-color: var(--niagads-blue);
            color: var(--niagads-ink);
        }
        .stButton > button[kind="secondary"]:not(:disabled) {
            background: #eaf3fb;
            border-color: #8fb8d6;
            color: #1f4f73;
            font-weight: 800;
        }
        .stButton > button[kind="secondary"]:not(:disabled):hover {
            background: #d9ebf7;
            border-color: #5f8fb8;
            color: #1d405c;
        }
        .mission-description {
            color: #3c4b58;
            line-height: 1.45;
            margin: 0.35rem 0 0.75rem 0;
            max-width: 66rem;
        }
        .mission-start {
            background: #e7f6ec;
            border-left: 4px solid #2f8f4e;
            color: var(--niagads-ink);
            margin: 0;
            padding: 0.6rem 0.75rem;
        }
        .next-step {
            background: #e7f6ec;
            border-left: 4px solid #2f8f4e;
            color: var(--niagads-ink);
            font-size: 0.92rem;
            line-height: 1.35;
            margin: -0.1rem 0 0.55rem 0;
            padding: 0.5rem 0.7rem;
        }
        .resource-action-row {
            align-items: stretch;
            display: flex;
            gap: 0.75rem;
            margin: 0.75rem 0;
        }
        .resource-action-row > div:first-child {
            flex: 0 0 auto;
        }
        .resource-action-row > div:last-child {
            flex: 1 1 auto;
        }
        .status-pill, .skill-chip {display: inline-block; border-radius: 999px; padding: 0.18rem 0.55rem; margin: 0.12rem; font-size: 0.85rem;}
        .status-complete {background: #e7f6ec; color: #1f6b3a;}
        .status-incomplete {background: #edf1f4; color: #425466;}
        .skill-chip {border: 1px solid; }
        .skill-earned {background: #fff3d6; border-color: var(--niagads-gold-deep); color: #6d4714;}
        .skill-pending {background: #f3f6f8; border-color: var(--niagads-line); color: var(--niagads-muted);}
        .skill-label {
            color: var(--niagads-muted);
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.04em;
            text-transform: uppercase;
        }
        code {
            background: #e7eff6;
            border: 1px solid #bfd1df;
            border-radius: 999px;
            color: var(--niagads-navy-deep);
            font-family: inherit;
            font-size: 0.86em;
            font-weight: 700;
            padding: 0.12rem 0.45rem;
            white-space: nowrap;
        }
        .path-grid {
            display: grid;
            gap: 0.7rem;
            grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
            margin: 0.6rem 0 1.25rem 0;
        }
        .path-node {
            border: 1px solid var(--niagads-line);
            border-left: 6px solid #8c959f;
            border-radius: 8px;
            background: #ffffff;
            min-height: 8.4rem;
            padding: 0.75rem;
        }
        .path-node-complete {border-left-color: var(--niagads-blue);}
        .path-node-pending {background: #f3f6f8;}
        .path-source {
            color: var(--niagads-muted);
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 0.04em;
            text-transform: uppercase;
        }
        .path-label {
            color: var(--niagads-ink);
            font-size: 1rem;
            font-weight: 700;
            margin-top: 0.2rem;
        }
        .path-value {
            color: #3c4b58;
            font-size: 0.9rem;
            line-height: 1.3;
            margin-top: 0.45rem;
            overflow-wrap: anywhere;
        }
        .path-status {
            color: var(--niagads-muted);
            font-size: 0.75rem;
            margin-top: 0.6rem;
        }
        .focus-panel {
            background: #fff5dd;
            border: 1px solid var(--niagads-gold-deep);
            border-radius: 8px;
            display: grid;
            gap: 0.65rem;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            margin: 0.5rem 0 1.25rem 0;
            padding: 0.85rem;
        }
        .focus-item {
            background: rgba(255, 255, 255, 0.72);
            border: 1px solid rgba(243, 170, 52, 0.34);
            border-radius: 6px;
            padding: 0.65rem;
        }
        .focus-label {
            color: #70501a;
            font-size: 0.78rem;
            font-weight: 700;
            text-transform: uppercase;
        }
        .focus-value {
            color: var(--niagads-ink);
            font-size: 0.92rem;
            margin-top: 0.25rem;
            overflow-wrap: anywhere;
        }
        .stButton > button,
        .stLinkButton > a {
            border-color: var(--niagads-blue);
            border-radius: 4px;
            color: var(--niagads-ink);
        }
        .stLinkButton > a {
            background: var(--niagads-gold);
            border-color: var(--niagads-gold-deep);
        }
        .stLinkButton > a:hover {
            background: #ffd37a;
            border-color: var(--niagads-blue);
            color: var(--niagads-ink);
        }
        .resource-open-button {
            align-items: center;
            background: #2f8f4e;
            border: 1px solid #1f6b3a;
            border-radius: 4px;
            color: #ffffff !important;
            display: inline-flex;
            font-size: 0.95rem;
            font-weight: 800;
            min-height: 2.5rem;
            padding: 0.45rem 0.85rem;
            text-decoration: none !important;
            white-space: nowrap;
        }
        .resource-open-button:hover {
            background: #25743f;
            border-color: #144d2a;
            color: #ffffff !important;
            text-decoration: none !important;
        }
        .resource-open-button + .resource-open-button {
            margin-left: 0.45rem;
        }
        .resource-note {
            background: #eaf3fb;
            border: 1px solid #8fb8d6;
            border-left: 6px solid var(--niagads-blue);
            border-radius: 6px;
            color: var(--niagads-ink);
            font-size: 0.92rem;
            line-height: 1.35;
            margin: -0.25rem 0 0.85rem 0;
            padding: 0.62rem 0.75rem;
        }
        .resource-note-icon {
            color: var(--niagads-blue);
            font-weight: 800;
            margin-right: 0.3rem;
        }
        section[data-testid="stSidebar"] .stButton > button,
        section[data-testid="stSidebar"] .stLinkButton > a {
            background: var(--niagads-gold);
            border-color: var(--niagads-gold-deep);
            color: var(--niagads-ink);
        }
        section[data-testid="stSidebar"] .stButton > button:hover,
        section[data-testid="stSidebar"] .stLinkButton > a:hover {
            background: #ffd37a;
            border-color: var(--niagads-blue);
            color: var(--niagads-ink);
        }
        section[data-testid="stSidebar"] .stButton > button:focus,
        section[data-testid="stSidebar"] .stLinkButton > a:focus {
            box-shadow: 0 0 0 0.16rem rgba(255, 196, 92, 0.45);
            outline: none;
        }
        section[data-testid="stSidebar"] .stButton > button *,
        section[data-testid="stSidebar"] .stLinkButton > a * {
            color: var(--niagads-ink);
        }
        section[data-testid="stSidebar"] .stButton > button:hover *,
        section[data-testid="stSidebar"] .stLinkButton > a:hover * {
            color: var(--niagads-ink);
        }

        section[data-testid="stSidebar"] .stButton > button,
        section[data-testid="stSidebar"] .stLinkButton > a {
            align-items: center;
            display: flex;
            justify-content: center;
            white-space: nowrap;
        }
        section[data-testid="stSidebar"] .stButton > button p,
        section[data-testid="stSidebar"] .stLinkButton > a p {
            line-height: 1;
            margin: 0;
            padding: 0;
            white-space: nowrap;
        }
        .stProgress > div > div > div > div {
            background-color: var(--niagads-gold);
        }
        .small-note {color: var(--niagads-muted); font-size: 0.92rem;}
        .section-heading {
            color: var(--niagads-ink);
            font-size: 1.08rem;
            font-weight: 800;
            margin: 1rem 0 0.4rem 0;
        }
        .field-label {
            color: var(--niagads-ink);
            font-size: 0.95rem;
            font-weight: 400;
            line-height: 1.35;
            margin: 0.45rem 0 0.25rem 0;
        }
        .bonus-badge {
            background: #ff6b35;
            border: 1px solid #d94e1f;
            border-radius: 999px;
            color: #ffffff;
            display: inline-block;
            font-size: 0.92em;
            font-weight: 800;
            margin-right: 0.25rem;
            padding: 0.1rem 0.45rem;
        }
        .carry-forward-badge {
            background: #0c772f;
            border: 1px solid #1f6b3a;
            border-radius: 0.5rem;
            color: #ffffff;
            display: inline-block;
            font-size: 0.92em;
            font-weight: 800;
            margin-right: 0.5rem;
            padding: 0.1rem 0.45rem;
        }
        .hint-details {
            display: block;
            margin: 0;
        }
        .hint-details summary {
            color: var(--niagads-ink);
            cursor: pointer;
            display: flex;
            align-items: baseline;
            gap: 0.7rem;
            line-height: 1.35;
            user-select: none;
        }
        .hint-details summary::marker {
            content: "";
        }
        .inline-hint-button {
            background: var(--niagads-gold);
            border: 1px solid var(--niagads-gold-deep);
            border-radius: 0.5rem;
            color: var(--niagads-ink);
            display: inline-block;
            flex: 0 0 auto;
            font-size: 0.86em;
            font-weight: 700;
            line-height: 1;
            padding: 0.32rem 0.7rem;
        }
        .inline-hint-button::before {
            content: "Show hint";
        }
        .hint-details[open] .inline-hint-button::before {
            content: "Hide hint";
        }
        .hint-details summary:hover .inline-hint-button {
            background: #ffd37a;
            border-color: var(--niagads-blue);
        }
        .hint-question {
            flex: 1 1 auto;
        }
        .hint-content {
            background: #fff9e8;
            border-left: 4px solid var(--niagads-gold-deep);
            color: #70501a;
            display: block;
            margin-top: 0.45rem;
            padding: 0.55rem 0.7rem;
        }
        .mission-title-row {
            align-items: center;
            display: flex;
            gap: 0.55rem;
            margin: 0 0 0.2rem 0;
        }
        .mission-title {
            color: var(--niagads-ink);
            font-size: 1.55rem;
            font-weight: 800;
            line-height: 1.1;
        }
        </style>
        """,
    )


def render_landing_page(video_path):
    _, content_col, _ = st.columns([0.26, 0.48, 0.26])
    with content_col:
        st.html(
            """
            <div class="landing-intro">
                <div class="landing-eyebrow">NIAGADS</div>
                <div class="landing-title">Open Access Scavenger Hunt</div>
                <div class="landing-copy">
                    Watch the short introduction, then begin the hunt when you're ready.
                </div>
            </div>
            """,
        )
        st.html("<div class='landing-video-spacer'></div>")
        st.html(
            f"""
            <video class="landing-video" autoplay muted playsinline controls>
                <source src="{video_data_uri(video_path)}" type="video/mp4">
            </video>
            """,
        )
        st.html("<div class='landing-action-spacer'></div>")
        if st.button("Begin the Hunt", type="primary"):
            st.session_state.hunt_started = True
            st.rerun()


def render_leaderboard_view():
    st.title("Workshop Leaderboard")
    st.caption(
        "Rank score is points plus badges earned. Ties are sorted by required activity progress, then points."
    )

    if not leaderboard_configured():
        st.warning("Leaderboard storage is not configured yet.")
        st.stop()

    try:
        entries = load_leaderboard()
    except Exception as error:
        st.error("Could not load the leaderboard from Google Sheets.")
        st.caption(str(error))
        st.stop()

    rows = leaderboard_rows(entries)
    if rows:
        st.dataframe(rows, hide_index=True, use_container_width=True)
    else:
        st.caption("No leaderboard submissions yet.")
    st.stop()


def render_completed_skills(skill_names, award_icon):
    if not skill_names:
        st.caption("No skills completed yet.")
        return
    st.html(
        " ".join(
            f"<span class='skill-chip skill-earned'>{award_icon} {skill}</span>"
            for skill in skill_names
        ),
    )


def render_activity_skills(mission, award_icon, mission_skills, skill_complete):
    st.html(
        "<span class='skill-label'>Badges to earn:</span> "
        + " ".join(
            f"<span class='skill-chip {'skill-earned' if skill_complete(mission, skill) else 'skill-pending'}'>{award_icon} {skill['skill']}</span>"
            for skill in mission_skills(mission)
        ),
    )


def activity_answers(summary, activity_id):
    for activity in summary["activities"]:
        if activity.get("id") == activity_id:
            return activity.get("answers", {})
    return {}


def answer_value(summary, activity_id, key):
    value = activity_answers(summary, activity_id).get(key, "")
    return str(value).strip()


def first_answer(summary, activity_id, keys):
    for key in keys:
        value = answer_value(summary, activity_id, key)
        if value:
            return value
    return ""


def display_value(value, fallback="Not recorded yet"):
    return escape(str(value).strip() or fallback)


def content_html(text):
    return str(text)


def field_label_html(label, carry_forward=False):
    label = content_html(label)
    if carry_forward:
        label = f"<span class='carry-forward-badge'>Link forward</span>{label}"
    if label.startswith("Bonus: "):
        return f"<span class='bonus-badge'>Bonus</span>{label.removeprefix('Bonus: ')}"
    return label


def pathway_node(label, source, value, complete=False):
    status_class = "path-node-complete" if complete else "path-node-pending"
    status_text = "Complete" if complete else "Pending"
    return (
        f"<div class='path-node {status_class}'>"
        f"<div class='path-source'>{escape(source)}</div>"
        f"<div class='path-label'>{escape(label)}</div>"
        f"<div class='path-value'>{display_value(value)}</div>"
        f"<div class='path-status'>{status_text}</div>"
        f"</div>"
    )


def render_evidence_pathway(summary):
    prioritization = first_answer(
        summary, "topgenes", ["topgenes-2", "topgenes-3", "topgenes-4"]
    )
    variant_inventory = first_answer(
        summary, "varixam", ["varixam-1", "varixam-2", "varixam-3"]
    )
    curated_association = first_answer(summary, "advp", ["advp-3", "advp-4", "advp-5"])
    genomicsdb_record = first_answer(
        summary,
        "genomicsdb",
        [
            "genomicsdb-gene-annotations-7",
            "genomicsdb-dataset-summary-1",
            "genomicsdb-dataset-summary-5",
            "genomicsdb-variant-record-1",
        ],
    )
    browser_observation = first_answer(
        summary,
        "genomicsdb",
        [
            "genomicsdb-genome-browser-1",
            "genomicsdb-genome-browser-2",
            "genomicsdb-genome-browser-3",
        ],
    )
    filer_signal = first_answer(
        summary,
        "filer",
        [
            "filer-3",
            "filer-6",
            "filer-7",
            "filer-9",
        ],
    )
    xqtl_signal = first_answer(
        summary,
        "xqtl",
        [
            "xqtl-2",
            "xqtl-associations-tab-1",
            "xqtl-associations-tab-2",
            "xqtl-associations-tab-3",
        ],
    )
    functional_context = filer_signal or xqtl_signal
    interpretation = first_answer(
        summary,
        "interpretation",
        ["interpretation-1", "interpretation-2", "interpretation-3"],
    )
    api_integration = first_answer(
        summary,
        "api_bonus",
        ["api-1", "api-2"],
    )

    progress_text = f"{summary['required_activities_completed']}/{summary['required_activities_total']}"

    st.header("Challenge Takeaways")
    snapshot_cols = st.columns(4)
    snapshot_cols[0].metric("Gene", summary["assigned_gene"])
    snapshot_cols[1].metric("Team name", summary["team_name"] or "Not set")
    snapshot_cols[2].metric("Score", f"{summary['score']} pts")
    snapshot_cols[3].metric("Required progress", progress_text)

    nodes = [
        pathway_node(
            "Assigned gene",
            "Workshop setup",
            summary["assigned_gene"],
            bool(summary["assigned_gene"]),
        ),
        pathway_node(
            "Gene prioritization",
            "GVC Top Genes",
            prioritization,
            bool(prioritization),
        ),
        pathway_node(
            "ADSP variant inventory",
            "VariXam",
            variant_inventory,
            bool(variant_inventory),
        ),
        pathway_node(
            "Curated association",
            "ADVP",
            curated_association,
            bool(curated_association),
        ),
        pathway_node(
            "Linked GenomicsDB record",
            "GenomicsDB",
            genomicsdb_record,
            bool(genomicsdb_record),
        ),
        pathway_node(
            "Genome browser observation",
            "GenomicsDB",
            browser_observation,
            bool(browser_observation),
        ),
        pathway_node(
            "Functional context",
            "FILER / xQTL",
            functional_context,
            bool(functional_context),
        ),
        pathway_node(
            "Interpretation", "Synthesis", interpretation, bool(interpretation)
        ),
        pathway_node(
            "Programmatic integration",
            "NIAGADS API",
            api_integration,
            bool(api_integration),
        ),
    ]
    st.html(f"<div class='path-grid'>{''.join(nodes)}</div>")

    st.subheader("Carry-Forward Focus")
    focus_items = [
        (
            "Gene span",
            answer_value(summary, "genomicsdb", "genomicsdb-gene-annotations-1"),
        ),
        (
            "Dataset / track",
            answer_value(summary, "genomicsdb", "genomicsdb-gene-annotations-7"),
        ),
        (
            "Selected ADSP variant",
            answer_value(summary, "genomicsdb", "genomicsdb-dataset-summary-5"),
        ),
        (
            "Variant record / identifier",
            first_answer(
                summary,
                "genomicsdb",
                ["genomicsdb-variant-record-1", "genomicsdb-variant-record-2"],
            )
            or answer_value(summary, "varixam", "varixam-2"),
        ),
        (
            "Genome browser observation",
            first_answer(
                summary,
                "genomicsdb",
                [
                    "genomicsdb-genome-browser-1",
                    "genomicsdb-genome-browser-3",
                ],
            ),
        ),
        ("Functional context", functional_context),
        (
            "Interpretation / limitation",
            first_answer(
                summary, "interpretation", ["interpretation-1", "interpretation-3"]
            ),
        ),
        (
            "API integration idea",
            answer_value(summary, "api_bonus", "api-1"),
        ),
    ]
    focus_html = "".join(
        f"<div class='focus-item'><div class='focus-label'>{escape(label)}</div><div class='focus-value'>{display_value(value)}</div></div>"
        for label, value in focus_items
    )
    st.html(f"<div class='focus-panel'>{focus_html}</div>")


def render_sidebar(
    score,
    progress,
    completed_required,
    required_count,
    completed_skills,
    assignment_pool,
    award_icon,
):
    def assign_random_gene():
        st.session_state.assigned_gene = random.choice(assignment_pool)

    with st.sidebar:
        st.header("Challenge Status")
        st.session_state.team_name = st.text_input(
            "Team name",
            value=st.session_state.team_name,
        )
        st.text_input(
            "Email (optional)",
            key="email",
            placeholder="name@example.org",
        )
        gene_cols = st.columns([2.35, 0.65], vertical_alignment="bottom")
        with gene_cols[0]:
            st.session_state.assigned_gene = st.text_input(
                "Assigned gene",
                value=st.session_state.assigned_gene,
                label_visibility="collapsed",
            )
        with gene_cols[1]:
            st.button("New", on_click=assign_random_gene, use_container_width=True)

        if st.session_state.timer_started_at is None:
            if st.button(
                "Start 25-minute timer", type="primary", use_container_width=True
            ):
                st.session_state.timer_started_at = time.time()
                st.rerun()
        else:
            render_live_timer(st.session_state.timer_started_at)

        st.metric("Current score", f"{score} pts")
        st.progress(
            progress,
            text=f"Required progress: {completed_required}/{required_count}",
        )
        st.subheader("Skills completed")
        render_completed_skills(completed_skills, award_icon)
        st.link_button(
            "🏆 View leaderboard", "?view=leaderboard", use_container_width=True
        )


def render_live_timer(started_at):
    started_at_ms = int(started_at * 1000)
    duration_seconds = 25 * 60
    components.html(
        f"""
        <style>
            html, body {{
                background: transparent;
                color: #eef3f7;
                font-family: "Source Sans Pro", sans-serif;
                margin: 0;
                padding: 0;
            }}
            .timer-label {{
                font-size: 0.88rem;
                font-weight: 600;
                margin: 0 0 0.2rem 0;
            }}
            .timer-value {{
                font-size: 1.85rem;
                font-weight: 700;
                line-height: 1.15;
                margin: 0;
            }}
            .timer-elapsed {{
                color: #eef3f7;
                font-size: 0.88rem;
                margin-top: 0.1rem;
                opacity: 0.85;
            }}
        </style>
        <div class="timer-label">Time remaining</div>
        <div id="timer-value" class="timer-value">--:--</div>
        <div id="timer-elapsed" class="timer-elapsed">Elapsed: 00:00</div>
        <script>
            const startedAt = {started_at_ms};
            const durationSeconds = {duration_seconds};
            const valueEl = document.getElementById("timer-value");
            const elapsedEl = document.getElementById("timer-elapsed");

            function formatSeconds(totalSeconds) {{
                const minutes = Math.floor(totalSeconds / 60);
                const seconds = totalSeconds % 60;
                return `${{String(minutes).padStart(2, "0")}}:${{String(seconds).padStart(2, "0")}}`;
            }}

            function updateTimer() {{
                const elapsed = Math.max(Math.floor((Date.now() - startedAt) / 1000), 0);
                const remaining = Math.max(durationSeconds - elapsed, 0);
                valueEl.textContent = formatSeconds(remaining);
                elapsedEl.textContent = `Elapsed: ${{formatSeconds(elapsed)}}`;
            }}

            updateTimer();
            window.setInterval(updateTimer, 1000);
        </script>
        """,
        height=86,
    )


def render_page_header(
    completed_required, required_count, score, completed_skills, award_icon
):
    st.html(
        f"""
        <div class="app-hero">
            <div class="app-kicker">NIAGADS Open Access</div>
            <div class="app-title">AD Gene Challenge</div>
            <div class="app-subtitle">
                Build a gene evidence summary for <strong>{escape(st.session_state.assigned_gene)}</strong>.
                Complete the required activities in about 25 minutes; optional prompts add bonus credit.
            </div>
        </div>
        """,
    )

    st.html(
        """
        <div class="mobile-resource-note">
            This activity is designed for desktop; it requires opening multiple browser tabs. </br></br>
            On mobile, press and hold <code>Open Resource</code>
            buttons (next to the <code>Getting Started</code> directives) and select option to open link in a new tab.
        </div>
        """,
    )
    col1, col2, col3 = st.columns(3)
    col1.metric("Assigned gene", st.session_state.assigned_gene)
    col2.metric("Required activities", f"{completed_required}/{required_count}")
    col3.metric("Score", f"{score} pts")
    render_completed_skills(completed_skills, award_icon)


def render_missions(
    missions,
    award_icon,
    mission_complete,
    mission_ready,
    mission_skills,
    skill_complete,
    resource_url,
):
    st.divider()

    for mission in missions:
        complete = mission_complete(mission)
        status_text = "Complete" if complete else "Incomplete"
        pill_class = "status-complete" if complete else "status-incomplete"
        resource_text = ", ".join(mission["resources"])
        display_title = (
            f"{mission['title']}: {resource_text}"
            if resource_text
            else mission["title"]
        )

        with st.container(border=True):
            header_cols = st.columns([3, 1])
            with header_cols[0]:
                st.html(
                    f"<div class='mission-title-row'><div class='mission-title'>{escape(display_title)}</div><span class='status-pill {pill_class}'>{status_text}</span></div>"
                )
                render_activity_skills(
                    mission, award_icon, mission_skills, skill_complete
                )
            with header_cols[1]:
                bonus_total = sum(
                    field.get("bonus_points", 0) for field in mission["fields"]
                )
                label = f"{mission['points']} pts"
                if bonus_total:
                    label = (
                        f"+{bonus_total} bonus pts"
                        if mission["points"] == 0
                        else f"{label} + {bonus_total} bonus"
                    )
                st.metric("Value", label)

            if mission.get("purpose"):
                st.html(
                    f"<div class='mission-description'>{content_html(mission['purpose'])}</div>"
                )
            render_resource_notes(mission.get("resource_notes", []))
            if mission.get("reference_links"):
                for link in mission["reference_links"]:
                    st.link_button(link["label"], link["url"])

            if mission["resources"] or mission.get("getting_started"):
                buttons_html = "".join(
                    f"<a class='resource-open-button' href='{escape(resource_url(resource))}' target='_blank' rel='noopener noreferrer'>Open {escape(resource)}</a>"
                    for resource in mission["resources"]
                )
                start_html = (
                    f"<div class='mission-start'><strong>Getting started:</strong> {content_html(mission['getting_started'])}</div>"
                    if mission.get("getting_started")
                    else ""
                )
                st.html(
                    f"<div class='resource-action-row'><div>{buttons_html}</div><div>{start_html}</div></div>",
                )

            render_mission_fields(mission)
            ready = mission_ready(mission)
            started = mission_started(mission)
            complete = mission_complete(mission)
            button_label = "Section complete" if complete else "Mark section complete"
            st.button(
                button_label,
                key=f"complete_{mission['id']}",
                type="primary" if ready and not complete else "secondary",
                disabled=complete or not started,
                on_click=mark_mission_complete,
                args=(mission,),
            )


def render_resource_notes(notes):
    notes_html = "".join(
        f"<div class='resource-note'><span class='resource-note-icon'>ⓘ</span><strong>{escape(note['label'])}:</strong> {content_html(note['message'])}</div>"
        for note in notes
    )
    if notes_html:
        st.html(notes_html)


def render_mission_fields(mission):
    mission_answers = st.session_state.answers.setdefault(mission["id"], {})
    for field in mission["fields"]:
        if field["type"] == "section":
            st.html(f"<div class='section-heading'>{escape(field['label'])}</div>")
            if field.get("next_step"):
                st.html(
                    f"<div class='next-step'><strong>Next step:</strong> {content_html(field['next_step'])}</div>"
                )
            continue
        key = f"answer_{mission['id']}_{field['key']}"
        current = mission_answers.get(field["key"], "")
        bonus_points = field.get("bonus_points", 0)
        widget_label = field["label"]
        label_visibility = "visible"
        rendered_label = field_label_html(
            widget_label, carry_forward=field.get("carry_forward", False)
        )
        if "hint" in field:
            st.html(
                f"<div class='field-label'><details class='hint-details'><summary><span class='inline-hint-button'></span><span class='hint-question'>{rendered_label}</span></summary><div class='hint-content'>{content_html(field['hint'])}</div></details></div>"
            )
            label_visibility = "collapsed"
        elif ("<" in widget_label and ">" in widget_label) or field.get(
            "carry_forward"
        ):
            st.html(f"<div class='field-label'>{rendered_label}</div>")
            label_visibility = "collapsed"
        if field["type"] == "textarea":
            mission_answers[field["key"]] = st.text_area(
                widget_label,
                value=current,
                key=key,
                height=90,
                on_change=start_timer_if_needed,
                label_visibility=label_visibility,
            )
        elif field["type"] == "select":
            options = field["options"]
            index = options.index(current) if current in options else 0
            mission_answers[field["key"]] = st.selectbox(
                widget_label,
                options,
                index=index,
                key=key,
                on_change=start_timer_if_needed,
                label_visibility=label_visibility,
            )
        else:
            mission_answers[field["key"]] = st.text_input(
                widget_label,
                value=current,
                key=key,
                on_change=start_timer_if_needed,
                label_visibility=label_visibility,
            )


def start_timer_if_needed():
    if st.session_state.timer_started_at is None:
        st.session_state.timer_started_at = time.time()


def mark_mission_complete(mission):
    mission_id = mission["id"]
    st.session_state.completed_missions.add(mission_id)
    st.session_state.mission_completed_at[mission_id] = time.time()
    st.session_state.mission_base_points_awarded[mission_id] = mission["points"]


def render_summary_and_submit(summary, score):
    st.divider()
    render_evidence_pathway(summary)

    st.divider()
    st.header("Submit Results")
    st.caption(
        "Submit or update your score when you are ready. The leaderboard is shown on a separate page."
    )

    submit_cols = st.columns([1, 1])
    with submit_cols[0]:
        if leaderboard_configured():
            if st.button("Submit to Leaderboard"):
                submit_to_leaderboard(summary, st.session_state.leaderboard_entry_id)
                st.session_state.leaderboard_submitted = True
                st.success("Leaderboard updated.")
        else:
            st.warning("Leaderboard submission is not configured yet.")
    with submit_cols[1]:
        st.metric("Current score", f"{score} pts")
