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
    st.markdown(
        """
        <style>
        .block-container {padding-top: 1.5rem;}
        .mission-card {border: 1px solid #d9e2ec; border-radius: 14px; padding: 1rem; margin-bottom: 1rem; background: #ffffff;}
        .mission-complete {border-left: 7px solid #2e7d32;}
        .mission-incomplete {border-left: 7px solid #7b8794;}
        .mission-bonus {border-left: 7px solid #6f42c1; background: #fbf9ff;}
        .status-pill, .skill-chip {display: inline-block; border-radius: 999px; padding: 0.18rem 0.55rem; margin: 0.12rem; font-size: 0.85rem;}
        .status-complete {background: #e8f5e9; color: #1b5e20;}
        .status-incomplete {background: #eef2f7; color: #394b59;}
        .status-bonus {background: #f0e7ff; color: #4b2380;}
        .skill-chip {border: 1px solid; }
        .skill-earned {background: #e7f6ec; border-color: #94d3a2; color: #14532d;}
        .skill-pending {background: #f6f8fa; border-color: #d0d7de; color: #57606a;}
        .summary-skill-strip {
            background: #f6f8fa;
            border: 1px solid #d0d7de;
            border-radius: 8px;
            color: #394b59;
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
            border: 1px solid #d0d7de;
            border-left: 6px solid #8c959f;
            border-radius: 8px;
            background: #ffffff;
            min-height: 8.4rem;
            padding: 0.75rem;
        }
        .path-node-complete {border-left-color: #2e7d32;}
        .path-node-pending {background: #f6f8fa;}
        .path-source {
            color: #57606a;
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 0.04em;
            text-transform: uppercase;
        }
        .path-label {
            color: #24292f;
            font-size: 1rem;
            font-weight: 700;
            margin-top: 0.2rem;
        }
        .path-value {
            color: #394b59;
            font-size: 0.9rem;
            line-height: 1.3;
            margin-top: 0.45rem;
            overflow-wrap: anywhere;
        }
        .path-status {
            color: #57606a;
            font-size: 0.75rem;
            margin-top: 0.6rem;
        }
        .focus-panel {
            background: #fff8e6;
            border: 1px solid #f0c36d;
            border-radius: 8px;
            display: grid;
            gap: 0.65rem;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            margin: 0.5rem 0 1.25rem 0;
            padding: 0.85rem;
        }
        .focus-item {
            background: rgba(255, 255, 255, 0.72);
            border: 1px solid rgba(184, 134, 11, 0.22);
            border-radius: 6px;
            padding: 0.65rem;
        }
        .focus-label {
            color: #6b4e16;
            font-size: 0.78rem;
            font-weight: 700;
            text-transform: uppercase;
        }
        .focus-value {
            color: #24292f;
            font-size: 0.92rem;
            margin-top: 0.25rem;
            overflow-wrap: anywhere;
        }
        .small-note {color: #52606d; font-size: 0.92rem;}
        </style>
        """,
        unsafe_allow_html=True,
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
    st.markdown(
        " ".join(
            f"<span class='skill-chip skill-earned'>{award_icon} {skill}</span>"
            for skill in skill_names
        ),
        unsafe_allow_html=True,
    )


def render_activity_skills(mission, award_icon, mission_skills, skill_complete):
    st.markdown(
        " ".join(
            f"<span class='skill-chip {'skill-earned' if skill_complete(mission, skill) else 'skill-pending'}'>{award_icon} {skill['skill']}</span>"
            for skill in mission_skills(mission)
        ),
        unsafe_allow_html=True,
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
        summary, "advp", ["AD association status", "One association or evidence detail"]
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
    functional_signal = first_answer(
        summary,
        "functional",
        [
            "Dataset, track, or result name",
            "Evidence type",
            "Functional annotation note",
        ],
    )
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
    snapshot_cols[1].metric("Team label", summary["team_label"] or "Not set")
    snapshot_cols[2].metric("Score", f"{summary['score']} pts")
    snapshot_cols[3].metric("Required progress", progress_text)
    st.markdown(
        f"<div class='summary-skill-strip'>{display_value(skills_text)}</div>",
        unsafe_allow_html=True,
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
    st.markdown(
        f"<div class='path-grid'>{''.join(nodes)}</div>", unsafe_allow_html=True
    )

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
                "functional",
                ["Dataset, track, or result name", "Evidence type"],
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
    st.markdown(f"<div class='focus-panel'>{focus_html}</div>", unsafe_allow_html=True)


def render_sidebar(
    score,
    progress,
    completed_required,
    required_count,
    completed_skills,
    genes,
    award_icon,
    random_team_label,
):
    with st.sidebar:
        st.header("Workshop Progress")
        st.text_input("Table or group number", key="team_name", placeholder="e.g., Table 4")
        st.text_input(
            "Team leader email (optional)",
            key="leader_email",
            placeholder="name@example.org",
        )
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Generate team label", use_container_width=True):
                st.session_state.team_label = random_team_label()
        with col_b:
            if st.button("Assign gene", use_container_width=True):
                st.session_state.assigned_gene = random.choice(genes)
        st.text_input("Team label", key="team_label", placeholder="Generate or type one")
        st.selectbox("Manual gene override", genes, key="assigned_gene")

        if st.session_state.timer_started_at is None:
            if st.button("Start 20-minute timer", type="primary", use_container_width=True):
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
        st.link_button("🏆 View leaderboard", "?view=leaderboard", use_container_width=True)


def render_page_header(completed_required, required_count, score, completed_skills, award_icon):
    st.title("NIAGADS Open Access Workshop Challenge")
    st.subheader("Build a gene evidence summary")
    st.markdown(
        f"Your team is reviewing **{st.session_state.assigned_gene}**. Complete the required activities in about 20 minutes; the API activity is optional bonus credit."
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

        st.markdown(f"<div class='mission-card {status_class}'>", unsafe_allow_html=True)
        header_cols = st.columns([3, 1])
        with header_cols[0]:
            st.markdown(f"### {mission['title']}")
            st.markdown(
                f"<span class='status-pill {pill_class}'>{status_text}</span>",
                unsafe_allow_html=True,
            )
            render_activity_skills(mission, award_icon, mission_skills, skill_complete)
        with header_cols[1]:
            label = (
                f"+{mission['points']} bonus pts"
                if mission["bonus"]
                else f"{mission['points']} pts"
            )
            st.metric("Value", label)

        st.write(mission["task"])
        if mission["id"] == "varixam":
            st.info(
                "VarIXam is used here for ADSP variant inventory within a gene footprint, not variant interpretation.",
                icon="ℹ️",
            )

        if mission["resources"]:
            link_cols = st.columns(max(len(mission["resources"]), 1))
            for idx, resource in enumerate(mission["resources"]):
                link_cols[idx].link_button(
                    f"Open {resource}", resource_url(resource), use_container_width=True
                )

        if st.button("Show hint (-1 point once)", key=f"hint_{mission['id']}"):
            st.session_state.hints_used.add(mission["id"])
        if mission["id"] in st.session_state.hints_used:
            st.warning(f"Hint: {mission['hint']}")

        render_mission_fields(mission)

        st.markdown("</div>", unsafe_allow_html=True)


def render_mission_fields(mission):
    mission_answers = st.session_state.answers.setdefault(mission["id"], {})
    for field in mission["fields"]:
        if field["type"] == "section":
            st.markdown(f"#### {field['label']}")
            continue
        key = f"answer_{mission['id']}_{field['key']}"
        current = mission_answers.get(field["key"], "")
        widget_label = field["label"]
        label_visibility = "visible"
        if "hint" in field:
            st.markdown(f"**{field['label']}**")
            hint_key = f"{mission['id']}::{field['key']}"
            if st.button(
                "Show bonus hint", key=f"field_hint_{mission['id']}_{field['key']}"
            ):
                st.session_state.field_hints_used.add(hint_key)
            if hint_key in st.session_state.field_hints_used:
                st.warning(f"Hint: {field['hint']}")
            widget_label = field["label"]
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
