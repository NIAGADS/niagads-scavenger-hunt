import random
import time
from html import escape

import streamlit as st

from leaderboard_store import (
    leaderboard_configured,
    leaderboard_rows,
    load_leaderboard,
    submit_to_leaderboard,
)


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
        .block-container {padding-top: 1.25rem;}
        .app-hero {
            background: var(--niagads-navy);
            border-top: 4px solid var(--niagads-gold);
            border-radius: 0;
            box-shadow: 0 8px 20px rgba(29, 42, 54, 0.12);
            margin: -0.25rem 0 1.4rem 0;
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
        .mission-card {
            background: #ffffff;
            border: 1px solid var(--niagads-line);
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(35, 49, 63, 0.06);
            margin-bottom: 1rem;
            padding: 1rem;
        }
        .mission-complete {border-left: 7px solid var(--niagads-blue);}
        .mission-incomplete {border-left: 7px solid #8a98a8;}
        .mission-bonus {border-left: 7px solid var(--niagads-violet); background: #f9f8ff;}
        .mission-description {
            color: #3c4b58;
            line-height: 1.45;
            margin: 0.35rem 0 0.75rem 0;
            max-width: 66rem;
        }
        .mission-start {
            background: #fff5dd;
            border-left: 4px solid var(--niagads-gold-deep);
            color: var(--niagads-ink);
            margin: 0;
            padding: 0.6rem 0.75rem;
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
        .status-complete {background: #eaf3f9; color: #224f73;}
        .status-incomplete {background: #edf1f4; color: #425466;}
        .status-bonus {background: #eeeaff; color: #3e2ba4;}
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
        .summary-skill-strip {
            background: #f3f6f8;
            border: 1px solid var(--niagads-line);
            border-radius: 8px;
            color: var(--niagads-ink);
            margin: 0.5rem 0 1rem 0;
            padding: 0.65rem 0.8rem;
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
            background: var(--niagads-gold);
            border: 1px solid var(--niagads-gold-deep);
            border-radius: 4px;
            color: var(--niagads-ink) !important;
            display: inline-flex;
            font-size: 0.95rem;
            min-height: 2.5rem;
            padding: 0.45rem 0.85rem;
            text-decoration: none !important;
            white-space: nowrap;
        }
        .resource-open-button:hover {
            background: #ffd37a;
            border-color: var(--niagads-blue);
            color: var(--niagads-ink) !important;
            text-decoration: none !important;
        }
        .resource-open-button + .resource-open-button {
            margin-left: 0.45rem;
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
        .stButton > button[kind="primary"] {
            background: var(--niagads-blue);
            border-color: var(--niagads-blue);
            color: #ffffff;
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
            font-weight: 600;
            line-height: 1.35;
            margin: 0.45rem 0 0.25rem 0;
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


def render_leaderboard_view():
    st.title("Workshop Leaderboard")
    st.caption(
        "Scores are sorted by points, required activity progress, completed skills, and fewer hints used."
    )
    if st.button("Return to workshop challenge"):
        st.query_params.clear()
        st.rerun()

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
    advp_signal = first_answer(
        summary, "advp", ["Curated association count", "Example association SNP"]
    )
    gwas_signal = first_answer(
        summary, "genomicsdb", ["Selected variant", "Variant p-value"]
    )
    dataset_signal = first_answer(
        summary,
        "genomicsdb",
        ["Locus zoom variant", "Dataset top region", "Dataset top result"],
    )
    variant_signal = first_answer(
        summary,
        "genomicsdb",
        ["Variant consequence", "Variant record ID", "Variant RefSNP"],
    )
    browser_region = first_answer(
        summary, "genomicsdb", ["Region to carry forward", "Genome browser observation"]
    )
    filer_signal = first_answer(
        summary,
        "filer",
        [
            "Highest overlap genomic feature type",
            "Darkest heatmap data source",
            "Strongest heatmap tissue categories",
        ],
    )
    xqtl_signal = first_answer(
        summary,
        "xqtl",
        [
            "xQTL type with highest associations",
            "Most significant association variant",
            "Local or broader context",
        ],
    )
    functional_signal = filer_signal or xqtl_signal
    interpretation = first_answer(
        summary,
        "interpretation",
        ["One-sentence interpretation", "One limitation or unanswered question"],
    )

    progress_text = f"{summary['required_activities_completed']}/{summary['required_activities_total']}"
    skills_text = (
        ", ".join(summary["skills_completed"])
        if summary["skills_completed"]
        else "No skills completed yet"
    )

    st.header("Evidence Pathway")
    snapshot_cols = st.columns(4)
    snapshot_cols[0].metric("Gene", summary["assigned_gene"])
    snapshot_cols[1].metric("Team name", summary["team_name"] or "Not set")
    snapshot_cols[2].metric("Score", f"{summary['score']} pts")
    snapshot_cols[3].metric("Required progress", progress_text)
    st.html(
        f"<div class='summary-skill-strip'>{display_value(skills_text)}</div>",
    )

    nodes = [
        pathway_node(
            "Assigned gene",
            "Workshop setup",
            summary["assigned_gene"],
            bool(summary["assigned_gene"]),
        ),
        pathway_node("Association evidence", "ADVP", advp_signal, bool(advp_signal)),
        pathway_node("GWAS table signal", "GenomicsDB", gwas_signal, bool(gwas_signal)),
        pathway_node(
            "Dataset / locus zoom", "GenomicsDB", dataset_signal, bool(dataset_signal)
        ),
        pathway_node(
            "Variant record", "GenomicsDB", variant_signal, bool(variant_signal)
        ),
        pathway_node(
            "Browser region", "GenomicsDB", browser_region, bool(browser_region)
        ),
        pathway_node(
            "Functional annotation",
            "FILER / xQTL",
            functional_signal,
            bool(functional_signal),
        ),
        pathway_node(
            "Interpretation", "Synthesis", interpretation, bool(interpretation)
        ),
    ]
    st.html(f"<div class='path-grid'>{''.join(nodes)}</div>")

    st.subheader("Carry-Forward Focus")
    focus_items = [
        (
            "Dataset / track",
            answer_value(summary, "genomicsdb", "Dataset or track name"),
        ),
        (
            "Locus zoom variant",
            answer_value(summary, "genomicsdb", "Locus zoom variant"),
        ),
        (
            "Variant context",
            first_answer(
                summary,
                "genomicsdb",
                ["Variant consequence", "Variant alleles", "Variant RefSNP"],
            ),
        ),
        (
            "Genome browser region",
            answer_value(summary, "genomicsdb", "Region to carry forward"),
        ),
        (
            "Functional evidence",
            first_answer(
                summary,
                "filer",
                ["Highest overlap genomic feature type", "Darkest heatmap data source"],
            )
            or first_answer(
                summary,
                "xqtl",
                ["xQTL type with highest associations", "Most significant association variant"],
            ),
        ),
        (
            "Limitation / question",
            answer_value(
                summary, "interpretation", "One limitation or unanswered question"
            ),
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
        st.text_input("Team name", key="team_name")
        st.text_input(
            "Email (optional)",
            key="email",
            placeholder="name@example.org",
        )
        gene_cols = st.columns([2.35, 0.65], vertical_alignment="bottom")
        with gene_cols[0]:
            st.text_input(
                "Assigned gene",
                key="assigned_gene",
                label_visibility="collapsed",
            )
        with gene_cols[1]:
            st.button("New", on_click=assign_random_gene, use_container_width=True)

        if st.session_state.timer_started_at is None:
            if st.button(
                "Start 20-minute timer", type="primary", use_container_width=True
            ):
                st.session_state.timer_started_at = time.time()
                st.rerun()
        else:
            elapsed = int(time.time() - st.session_state.timer_started_at)
            remaining = max(20 * 60 - elapsed, 0)
            st.metric("Time remaining", f"{remaining // 60:02d}:{remaining % 60:02d}")
            st.caption(f"Elapsed: {elapsed // 60:02d}:{elapsed % 60:02d}")
            if remaining > 0:
                time.sleep(1)
                st.rerun()

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


def render_page_header(
    completed_required, required_count, score, completed_skills, award_icon
):
    st.html(
        f"""
        <div class="app-hero">
            <div class="app-kicker">NIAGADS Open Access</div>
            <div class="app-title">Workshop Challenge</div>
            <div class="app-subtitle">
                Build a gene evidence summary for <strong>{escape(st.session_state.assigned_gene)}</strong>.
                Complete the required activities in about 20 minutes; the API activity is optional bonus credit.
            </div>
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
    mission_skills,
    skill_complete,
    resource_url,
):
    st.divider()

    for mission in missions:
        complete = mission_complete(mission)
        status_class = (
            "mission-bonus"
            if mission["bonus"]
            else ("mission-complete" if complete else "mission-incomplete")
        )
        status_text = (
            "Bonus" if mission["bonus"] else ("Complete" if complete else "Incomplete")
        )
        pill_class = (
            "status-bonus"
            if mission["bonus"]
            else ("status-complete" if complete else "status-incomplete")
        )
        resource_text = ", ".join(mission["resources"])
        display_title = (
            f"{mission['title']}: {resource_text}"
            if resource_text
            else mission["title"]
        )

        st.html(f"<div class='mission-card {status_class}'>")
        header_cols = st.columns([3, 1])
        with header_cols[0]:
            st.html(
                f"<div class='mission-title-row'><div class='mission-title'>{escape(display_title)}</div><span class='status-pill {pill_class}'>{status_text}</span></div>"
            )
            render_activity_skills(mission, award_icon, mission_skills, skill_complete)
        with header_cols[1]:
            bonus_total = sum(field.get("bonus_points", 0) for field in mission["fields"])
            label = (
                f"+{mission['points']} bonus pts"
                if mission["bonus"]
                else f"{mission['points']} pts"
            )
            if bonus_total and not mission["bonus"]:
                label = f"{label} + {bonus_total} bonus"
            st.metric("Value", label)

        if mission.get("purpose"):
            st.html(
                f"<div class='mission-description'>{content_html(mission['purpose'])}</div>"
            )

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

        st.html("</div>")


def render_mission_fields(mission):
    mission_answers = st.session_state.answers.setdefault(mission["id"], {})
    for field in mission["fields"]:
        if field["type"] == "section":
            st.html(f"<div class='section-heading'>{escape(field['label'])}</div>")
            continue
        key = f"answer_{mission['id']}_{field['key']}"
        current = mission_answers.get(field["key"], "")
        bonus_points = field.get("bonus_points", 0)
        widget_label = (
            f"{field['label']} (+{bonus_points} bonus point)"
            if bonus_points == 1
            else (
                f"{field['label']} (+{bonus_points} bonus points)"
                if bonus_points
                else field["label"]
            )
        )
        label_visibility = "visible"
        rendered_label = content_html(widget_label)
        if "hint" in field:
            st.html(f"<div class='field-label'>{rendered_label}</div>")
            hint_key = f"{mission['id']}::{field['key']}"
            if st.button(
                "Show bonus hint", key=f"field_hint_{mission['id']}_{field['key']}"
            ):
                st.session_state.field_hints_used.add(hint_key)
            if hint_key in st.session_state.field_hints_used:
                st.warning(f"Hint: {field['hint']}")
            label_visibility = "collapsed"
        elif "<" in widget_label and ">" in widget_label:
            st.html(f"<div class='field-label'>{rendered_label}</div>")
            label_visibility = "collapsed"
        if field["type"] == "textarea":
            mission_answers[field["key"]] = st.text_area(
                widget_label,
                value=current,
                key=key,
                height=90,
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
                label_visibility=label_visibility,
            )
        else:
            mission_answers[field["key"]] = st.text_input(
                widget_label,
                value=current,
                key=key,
                label_visibility=label_visibility,
            )


def render_summary_and_submit(summary, score):
    st.divider()
    render_evidence_pathway(summary)
    st.divider()
    st.header("Gene Evidence Summary Preview")
    st.caption("This preview updates as your team fills in activity fields.")
    st.json(summary, expanded=False)

    st.divider()
    st.header("Submit Results")
    st.caption(
        "Submit or update your team score when you are ready. The leaderboard is shown on a separate page."
    )

    submit_cols = st.columns([1, 1])
    with submit_cols[0]:
        if leaderboard_configured():
            if st.button(
                "Submit / update leaderboard", type="primary", use_container_width=True
            ):
                submit_to_leaderboard(summary, st.session_state.leaderboard_entry_id)
                st.session_state.leaderboard_submitted = True
                st.success("Leaderboard updated.")
        else:
            st.warning("Leaderboard submission is not configured yet.")
    with submit_cols[1]:
        st.metric("Current score", f"{score} pts")

    if st.session_state.leaderboard_submitted:
        st.success(
            "This team has submitted during the current session. Submit again to update the score."
        )

    st.link_button("🏆 Open leaderboard", "?view=leaderboard")
