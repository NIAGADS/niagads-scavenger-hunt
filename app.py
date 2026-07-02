import csv
import io
import json
import random
import time
from datetime import datetime, timezone

import streamlit as st


st.set_page_config(
    page_title="NIAGADS AD Gene Workshop Challenge",
    page_icon="🧬",
    layout="wide",
)

GENES = ["APOE", "BIN1", "TREM2", "ABCA7", "CLU", "PICALM", "CR1", "SORL1", "MS4A6A", "CD33"]

RESOURCES = {
    "ADVP": "https://advp.niagads.org/",
    "GenomicsDB": "https://www.niagads.org/genomics",
    "FILER": "https://tf.lisanwanglab.org/FILER/",
    "VarIXam": "https://varixam.niagads.org/",
    "TopGenes": "https://topgenes.niagads.org/",
    "xQTL Browser": "https://xqtl.niagads.org/",
    "API": "https://api.niagads.org/",
}

AWARD_ICON = "🏆"
TEAM_LABEL_PREFIXES = ["Amyloid", "Tau", "Synapse", "Hippocampus", "Microglia", "Genome", "Variant", "Atlas"]
TEAM_LABEL_NOUNS = ["Review Group", "Working Group", "Analysis Team", "Data Team", "Study Group", "Workshop Team"]

MISSIONS = [
    {
        "id": "advp",
        "title": "Review AD association evidence",
        "skill": "Association review",
        "points": 3,
        "resources": ["ADVP"],
        "task": "Search the assigned gene in ADVP and determine whether it has Alzheimer’s disease association evidence.",
        "fields": [
            {"key": "AD association status", "label": "AD association status", "type": "text"},
            {"key": "One association or evidence detail", "label": "One association or evidence detail", "type": "textarea"},
        ],
        "fallback": "If no result is found, write what ADVP is designed to help users find.",
        "hint": "Search by gene symbol and look for curated association/evidence records.",
        "bonus": False,
    },
    {
        "id": "genomicsdb",
        "title": "Review the genomic location",
        "skill": "Genomic context",
        "points": 3,
        "resources": ["GenomicsDB"],
        "task": "Find the genomic location or region for the assigned gene.",
        "fields": [
            {"key": "Chromosome", "label": "Chromosome", "type": "text"},
            {"key": "Start coordinate", "label": "Start coordinate", "type": "text"},
            {"key": "End coordinate", "label": "End coordinate", "type": "text"},
        ],
        "fallback": "If coordinates are hard to find, record the page/result where the gene appears.",
        "hint": "Search the gene symbol and look for chromosome and coordinate range.",
        "bonus": False,
    },
    {
        "id": "varixam",
        "title": "Inventory ADSP variants",
        "skill": "Variant inventory",
        "points": 3,
        "resources": ["VarIXam"],
        "task": "Find ADSP variants overlapping the assigned gene footprint. Record one example variant or summarize the returned variant set.",
        "fields": [
            {"key": "Example variant ID or coordinate", "label": "Example variant ID or coordinate", "type": "text"},
            {"key": "Variant density", "label": "Variant density", "type": "select", "options": ["", "none", "few", "many"]},
        ],
        "fallback": "If too many variants are returned, write “many” and describe what kind of list VarIXam provides.",
        "hint": "This is an inventory task, not interpretation. Any returned ADSP variant is acceptable.",
        "bonus": False,
    },
    {
        "id": "functional",
        "title": "Review functional evidence",
        "skill": "Functional annotation",
        "points": 4,
        "resources": ["FILER", "xQTL Browser"],
        "task": "Find one regulatory, functional, or QTL-related evidence item for the assigned gene or nearby region.",
        "fields": [
            {"key": "Evidence type", "label": "Evidence type", "type": "text"},
            {"key": "Dataset, track, or result name", "label": "Dataset, track, or result name", "type": "text"},
            {"key": "Which resource was used", "label": "Which resource was used", "type": "select", "options": ["", "FILER", "xQTL Browser"]},
        ],
        "fallback": "If no evidence is found, describe what kind of evidence FILER or xQTL Browser is intended to provide.",
        "hint": "Use xQTL for QTL-style evidence. Use FILER for functional or regulatory track evidence.",
        "bonus": False,
    },
    {
        "id": "topgenes",
        "title": "Check gene prioritization",
        "skill": "Gene prioritization",
        "points": 3,
        "resources": ["TopGenes"],
        "task": "Look up the assigned gene and record its prioritization information if available.",
        "fields": [
            {"key": "Rank, score, category, or not found", "label": "Rank, score, category, or “not found”", "type": "text"},
            {"key": "Brief note on what the prioritization suggests", "label": "Brief note on what the prioritization suggests", "type": "textarea"},
        ],
        "fallback": "If no gene result is found, describe what TopGenes is designed to support.",
        "hint": "Do not over-interpret. Capture how the resource ranks or categorizes the gene.",
        "bonus": False,
    },
    {
        "id": "interpretation",
        "title": "Summarize the evidence",
        "skill": "Evidence summary",
        "points": 4,
        "resources": [],
        "task": "Write a short synthesis of what the collected evidence suggests.",
        "fields": [
            {"key": "One-sentence interpretation", "label": "One-sentence interpretation", "type": "textarea"},
            {"key": "Most useful resource", "label": "Most useful resource", "type": "text"},
            {"key": "One limitation or unanswered question", "label": "One limitation or unanswered question", "type": "textarea"},
        ],
        "fallback": "None",
        "hint": "Good answers combine association, genomic context, variant inventory, and functional/prioritization evidence.",
        "bonus": False,
    },
    {
        "id": "api_bonus",
        "title": "Plan future automation",
        "skill": "API planning",
        "points": 2,
        "resources": ["API"],
        "task": "Identify one step in the workshop challenge that should eventually be automated through the NIAGADS API.",
        "fields": [
            {"key": "Step to automate", "label": "Step to automate", "type": "text"},
            {"key": "Why automation would help", "label": "Why automation would help", "type": "textarea"},
        ],
        "fallback": "Name one lookup that would be useful to retrieve programmatically.",
        "hint": "Think repeated lookup, coordinate retrieval, variant inventory, evidence aggregation, or report generation.",
        "bonus": True,
    },
]


def initialize_state():
    defaults = {
        "team_name": "",
        "team_label": "",
        "assigned_gene": "APOE",
        "timer_started_at": None,
        "answers": {},
        "hints_used": set(),
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def mission_complete(mission):
    answers = st.session_state.answers.get(mission["id"], {})
    return all(str(answers.get(field["key"], "")).strip() for field in mission["fields"])


def earned_points(mission):
    if not mission_complete(mission):
        return 0
    return max(mission["points"] - (1 if mission["id"] in st.session_state.hints_used else 0), 0)


def build_summary():
    completed = [mission for mission in MISSIONS if mission_complete(mission)]
    required = [mission for mission in MISSIONS if not mission["bonus"]]
    return {
        "team_name": st.session_state.team_name,
        "team_label": st.session_state.team_label,
        "assigned_gene": st.session_state.assigned_gene,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "score": sum(earned_points(mission) for mission in MISSIONS),
        "required_activities_completed": sum(mission_complete(mission) for mission in required),
        "required_activities_total": len(required),
        "skills_completed": [mission["skill"] for mission in completed],
        "hints_used": sorted(st.session_state.hints_used),
        "activities": [
            {
                "title": mission["title"],
                "skill": mission["skill"],
                "bonus": mission["bonus"],
                "complete": mission_complete(mission),
                "points_awarded": earned_points(mission),
                "answers": st.session_state.answers.get(mission["id"], {}),
            }
            for mission in MISSIONS
        ],
    }


def summary_csv(summary):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["team_name", "team_label", "assigned_gene", "activity", "skill", "field", "answer", "points_awarded"])
    for mission in summary["activities"]:
        answers = mission["answers"] or {"": ""}
        for field, answer in answers.items():
            writer.writerow([
                summary["team_name"], summary["team_label"], summary["assigned_gene"],
                mission["title"], mission["skill"], field, answer, mission["points_awarded"],
            ])
    return output.getvalue()


def render_skills(completed_missions):
    if not completed_missions:
        st.caption("No skills completed yet.")
        return
    st.markdown(
        " ".join(
            f"<span class='skill-chip skill-earned'>{AWARD_ICON} {mission['skill']}</span>"
            for mission in completed_missions
        ),
        unsafe_allow_html=True,
    )


initialize_state()

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
    .small-note {color: #52606d; font-size: 0.92rem;}
    </style>
    """,
    unsafe_allow_html=True,
)

required_missions = [mission for mission in MISSIONS if not mission["bonus"]]
completed_required = sum(mission_complete(mission) for mission in required_missions)
progress = completed_required / len(required_missions)
score = sum(earned_points(mission) for mission in MISSIONS)
completed_missions = [mission for mission in MISSIONS if mission_complete(mission)]

with st.sidebar:
    st.header("Workshop Progress")
    st.text_input("Team name", key="team_name", placeholder="e.g., Table 4")
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("Generate team label", use_container_width=True):
            st.session_state.team_label = f"{random.choice(TEAM_LABEL_PREFIXES)} {random.choice(TEAM_LABEL_NOUNS)}"
    with col_b:
        if st.button("Assign gene", use_container_width=True):
            st.session_state.assigned_gene = random.choice(GENES)
    st.text_input("Team label", key="team_label", placeholder="Generate or type one")
    st.selectbox("Manual gene override", GENES, key="assigned_gene")

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
    st.progress(progress, text=f"Required progress: {completed_required}/{len(required_missions)}")
    st.subheader("Skills completed")
    render_skills(completed_missions)

st.title("NIAGADS Open Access Workshop Challenge")
st.subheader("Build a gene evidence summary")
st.markdown(
    f"Your team is reviewing **{st.session_state.assigned_gene}**. Complete the required activities in about 20 minutes; the API activity is optional bonus credit."
)

col1, col2, col3 = st.columns(3)
col1.metric("Assigned gene", st.session_state.assigned_gene)
col2.metric("Required activities", f"{completed_required}/{len(required_missions)}")
col3.metric("Score", f"{score} pts")
render_skills(completed_missions)

st.divider()

for mission in MISSIONS:
    complete = mission_complete(mission)
    status_class = "mission-bonus" if mission["bonus"] else ("mission-complete" if complete else "mission-incomplete")
    status_text = "Bonus" if mission["bonus"] else ("Complete" if complete else "Incomplete")
    pill_class = "status-bonus" if mission["bonus"] else ("status-complete" if complete else "status-incomplete")

    st.markdown(f"<div class='mission-card {status_class}'>", unsafe_allow_html=True)
    header_cols = st.columns([3, 1])
    with header_cols[0]:
        st.markdown(f"### {mission['title']}")
        skill_class = "skill-earned" if complete else "skill-pending"
        st.markdown(f"<span class='status-pill {pill_class}'>{status_text}</span> <span class='skill-chip {skill_class}'>{AWARD_ICON} {mission['skill']}</span>", unsafe_allow_html=True)
    with header_cols[1]:
        label = f"+{mission['points']} bonus pts" if mission["bonus"] else f"{mission['points']} pts"
        st.metric("Value", label)

    st.write(mission["task"])
    if mission["id"] == "varixam":
        st.info("VarIXam is used here for ADSP variant inventory within a gene footprint, not variant interpretation.", icon="ℹ️")

    if mission["resources"]:
        link_cols = st.columns(max(len(mission["resources"]), 1))
        for idx, resource in enumerate(mission["resources"]):
            link_cols[idx].link_button(f"Open {resource}", RESOURCES[resource], use_container_width=True)

    with st.expander("Fallback question"):
        st.write(mission["fallback"])

    if st.button("Show hint (-1 point once)", key=f"hint_{mission['id']}"):
        st.session_state.hints_used.add(mission["id"])
    if mission["id"] in st.session_state.hints_used:
        st.warning(f"Hint: {mission['hint']}")

    mission_answers = st.session_state.answers.setdefault(mission["id"], {})
    for field in mission["fields"]:
        key = f"answer_{mission['id']}_{field['key']}"
        current = mission_answers.get(field["key"], "")
        if field["type"] == "textarea":
            mission_answers[field["key"]] = st.text_area(field["label"], value=current, key=key, height=90)
        elif field["type"] == "select":
            options = field["options"]
            index = options.index(current) if current in options else 0
            mission_answers[field["key"]] = st.selectbox(field["label"], options, index=index, key=key)
        else:
            mission_answers[field["key"]] = st.text_input(field["label"], value=current, key=key)

    st.markdown("</div>", unsafe_allow_html=True)

summary = build_summary()
st.divider()
st.header("Gene Evidence Summary Preview")
st.caption("This preview updates as your team fills in activity fields.")
st.json(summary, expanded=False)

download_cols = st.columns(2)
with download_cols[0]:
    st.download_button(
        "Download JSON summary",
        data=json.dumps(summary, indent=2),
        file_name=f"{st.session_state.assigned_gene}_workshop_summary.json",
        mime="application/json",
        use_container_width=True,
    )
with download_cols[1]:
    st.download_button(
        "Download CSV summary",
        data=summary_csv(summary),
        file_name=f"{st.session_state.assigned_gene}_workshop_summary.csv",
        mime="text/csv",
        use_container_width=True,
    )
