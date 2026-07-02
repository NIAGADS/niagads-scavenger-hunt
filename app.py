import json
import random
import time
from datetime import datetime, timezone
from html import escape
from uuid import uuid4

import streamlit as st

from leaderboard_store import leaderboard_configured, leaderboard_rows, load_leaderboard, submit_to_leaderboard


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
        "title": "Explore GWAS summary statistics in GenomicsDB",
        "skill": "Record Linker",
        "sub_skills": [
            {
                "skill": "Record Linker",
                "fields": [
                    "Ensembl ID",
                    "Gene location",
                    "GWAS table used",
                    "Selected variant",
                    "Dataset or track name",
                    "Dataset record title",
                    "Variant record ID",
                ],
            },
            {
                "skill": "Signal Mapper",
                "fields": [
                    "Dataset top region",
                    "Dataset top result",
                    "Locus zoom variant",
                    "Locus zoom reason",
                ],
            },
            {
                "skill": "Genome Browser",
                "fields": [
                    "Genome browser dataset track",
                    "Genome browser observation",
                    "Region to carry forward",
                ],
            },
        ],
        "points": 8,
        "resources": ["GenomicsDB"],
        "task": (
            "Search for the assigned gene in GenomicsDB, then use the gene record to review significant NIAGADS "
            "GWAS summary-statistics results in the gene footprint. Follow one table result to its dataset record, "
            "use locus zoom to select a variant from the Manhattan plot, inspect that variant record, then load the "
            "same dataset in the genome browser and choose a region to carry forward into the functional annotation "
            "activity."
        ),
        "fields": [
            {"type": "section", "label": "Search and Gene Record"},
            {"key": "Ensembl ID", "label": "After searching for the assigned gene, what Ensembl ID is shown?", "type": "text"},
            {"key": "Gene location", "label": "What genomic location is shown on the gene record?", "type": "text"},
            {
                "key": "Gene overview takeaway",
                "label": "From the overview chart, which trait or biomarker category has the most significant variants near this gene?",
                "type": "text",
            },
            {"type": "section", "label": "Gene Record / NIAGADS GWAS"},
            {
                "key": "GWAS table used",
                "label": "Which NIAGADS GWAS table did you use?",
                "type": "select",
                "options": ["", "Alzheimer’s Disease", "AD-related neuropathologies"],
            },
            {"key": "Selected variant", "label": "Which significant summary-statistics variant did you choose from the table?", "type": "text"},
            {
                "key": "Relative position",
                "label": "Where is that variant relative to the gene?",
                "type": "select",
                "options": ["", "upstream", "in gene", "downstream"],
            },
            {"key": "Variant p-value", "label": "What p-value is reported for that variant?", "type": "text"},
            {"key": "Dataset or track name", "label": "What linked dataset or track contains this summary-statistics result?", "type": "text"},
            {
                "key": "ADSP variant",
                "label": "Is the selected variant marked in the ADSP Variant column?",
                "type": "select",
                "options": ["", "yes", "no", "not shown"],
            },
            {"type": "section", "label": "Dataset Record"},
            {"key": "Dataset record title", "label": "After opening the dataset link, what is the dataset record title?", "type": "text"},
            {
                "key": "Dataset top region",
                "label": "From the dataset record, identify another strong association region outside the assigned gene if possible.",
                "type": "text",
            },
            {"key": "Dataset top result", "label": "What top variant, p-value, or nearest result supports that region?", "type": "text"},
            {
                "key": "Locus zoom variant",
                "label": "After toggling locus zoom view on the dataset Manhattan plot, which variant did you select?",
                "type": "text",
            },
            {
                "key": "Locus zoom reason",
                "label": "Why did you choose that variant or peak to inspect next?",
                "type": "textarea",
            },
            {"type": "section", "label": "Variant Record"},
            {"key": "Variant record ID", "label": "After clicking the selected variant, what variant ID appears in the header?", "type": "text"},
            {"key": "Variant RefSNP", "label": "What RefSNP ID is shown, if any?", "type": "text"},
            {"key": "Variant alleles", "label": "What alleles are shown in the variant record header?", "type": "text"},
            {
                "key": "Variant consequence",
                "label": "What consequence or impacted gene/transcript is listed in the header?",
                "type": "text",
            },
            {
                "key": "ADSP variant record label",
                "label": "Bonus: If the variant is ADSP-flagged, what does the ADSP Variant label indicate?",
                "type": "textarea",
                "required": False,
                "hint": (
                    "Open the linked variant record and look for the ADSP Variant label in the overview."
                ),
            },
            {"type": "section", "label": "Genome Browser"},
            {
                "key": "Genome browser dataset track",
                "label": "Click View on Genome Browser. Which dataset track did you load?",
                "type": "text",
            },
            {
                "key": "Genome browser observation",
                "label": "After exploring the loaded track, what region or pattern looks useful to inspect in FILER?",
                "type": "textarea",
            },
            {"type": "section", "label": "Carry Forward"},
            {
                "key": "Region to carry forward",
                "label": "What final region will you carry forward to the functional annotation activity?",
                "type": "text",
            },
        ],
        "fallback": (
            "If the dataset record is difficult to use, carry forward the original gene-region variant from "
            "the gene table and note the dataset link you tried."
        ),
        "hint": (
            "Search for the gene, open the gene record, then go to Trait associations → NIAGADS GWAS. Choose one "
            "significant summary-statistics variant with a linked dataset or track. Open the dataset record, use "
            "locus zoom to select a variant from the Manhattan plot, then use View on Genome Browser to load the "
            "same dataset track and choose a region for the functional annotation activity."
        ),
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
        "title": "Review functional evidence for the carried-forward region",
        "skill": "Functional annotation",
        "points": 4,
        "resources": ["FILER", "xQTL Browser"],
        "task": (
            "Use the region carried forward from the GenomicsDB dataset record to look for one regulatory, "
            "functional, or QTL-related evidence item in FILER or the xQTL Browser."
        ),
        "fields": [
            {
                "key": "Region carried forward from GenomicsDB",
                "label": "Region carried forward from GenomicsDB",
                "type": "text",
            },
            {"key": "Evidence type", "label": "Evidence type", "type": "text"},
            {"key": "Dataset, track, or result name", "label": "Dataset, track, or result name", "type": "text"},
            {"key": "Which resource was used", "label": "Which resource was used", "type": "select", "options": ["", "FILER", "xQTL Browser"]},
            {
                "key": "Functional annotation note",
                "label": "Brief note on how this annotation may help interpret the region",
                "type": "textarea",
            },
        ],
        "fallback": (
            "If the carried-forward region is hard to use, inspect the original assigned gene region instead "
            "and record which region you used."
        ),
        "hint": (
            "Use FILER for regulatory tracks and xQTL Browser for QTL-style evidence. Start with the region "
            "from GenomicsDB so this activity connects back to the dataset-level GWAS result."
        ),
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


def random_team_label():
    return f"{random.choice(TEAM_LABEL_PREFIXES)} {random.choice(TEAM_LABEL_NOUNS)}"


def initialize_state():
    defaults = {
        "team_name": "",
        "leader_email": "",
        "team_label": random_team_label(),
        "assigned_gene": random.choice(GENES),
        "leaderboard_entry_id": uuid4().hex,
        "leaderboard_submitted": False,
        "timer_started_at": None,
        "answers": {},
        "hints_used": set(),
        "field_hints_used": set(),
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def mission_complete(mission):
    answers = st.session_state.answers.get(mission["id"], {})
    return all(
        str(answers.get(field["key"], "")).strip()
        for field in mission["fields"]
        if field.get("required", True) and field.get("type") != "section"
    )


def skill_complete(mission, skill):
    answers = st.session_state.answers.get(mission["id"], {})
    return all(str(answers.get(field_key, "")).strip() for field_key in skill["fields"])


def mission_skills(mission):
    if "sub_skills" in mission:
        return mission["sub_skills"]
    return [{"skill": mission["skill"], "fields": [field["key"] for field in mission["fields"] if field.get("type") != "section" and field.get("required", True)]}]


def completed_skill_names(missions):
    skills = []
    for mission in missions:
        if "sub_skills" in mission:
            skills.extend(skill["skill"] for skill in mission["sub_skills"] if skill_complete(mission, skill))
        elif mission_complete(mission):
            skills.append(mission["skill"])
    return skills


def earned_points(mission):
    if not mission_complete(mission):
        return 0
    return max(mission["points"] - (1 if mission["id"] in st.session_state.hints_used else 0), 0)


def build_summary():
    required = [mission for mission in MISSIONS if not mission["bonus"]]
    return {
        "team_name": st.session_state.team_name,
        "leader_email": st.session_state.leader_email,
        "team_label": st.session_state.team_label,
        "assigned_gene": st.session_state.assigned_gene,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "score": sum(earned_points(mission) for mission in MISSIONS),
        "required_activities_completed": sum(mission_complete(mission) for mission in required),
        "required_activities_total": len(required),
        "skills_completed": completed_skill_names(MISSIONS),
        "hints_used": sorted(st.session_state.hints_used),
        "activities": [
            {
                "id": mission["id"],
                "title": mission["title"],
                "skill": mission["skill"],
                "skills": [skill["skill"] for skill in mission_skills(mission)],
                "bonus": mission["bonus"],
                "complete": mission_complete(mission),
                "points_awarded": earned_points(mission),
                "answers": st.session_state.answers.get(mission["id"], {}),
            }
            for mission in MISSIONS
        ],
    }


def render_completed_skills(skill_names):
    if not skill_names:
        st.caption("No skills completed yet.")
        return
    st.markdown(
        " ".join(
            f"<span class='skill-chip skill-earned'>{AWARD_ICON} {skill}</span>"
            for skill in skill_names
        ),
        unsafe_allow_html=True,
    )


def render_activity_skills(mission):
    st.markdown(
        " ".join(
            f"<span class='skill-chip {'skill-earned' if skill_complete(mission, skill) else 'skill-pending'}'>{AWARD_ICON} {skill['skill']}</span>"
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
    advp_signal = first_answer(summary, "advp", ["AD association status", "One association or evidence detail"])
    gwas_signal = first_answer(summary, "genomicsdb", ["Selected variant", "Variant p-value"])
    dataset_signal = first_answer(summary, "genomicsdb", ["Locus zoom variant", "Dataset top region", "Dataset top result"])
    variant_signal = first_answer(summary, "genomicsdb", ["Variant consequence", "Variant record ID", "Variant RefSNP"])
    browser_region = first_answer(summary, "genomicsdb", ["Region to carry forward", "Genome browser observation"])
    functional_signal = first_answer(summary, "functional", ["Dataset, track, or result name", "Evidence type", "Functional annotation note"])
    interpretation = first_answer(summary, "interpretation", ["One-sentence interpretation", "One limitation or unanswered question"])

    progress_text = f"{summary['required_activities_completed']}/{summary['required_activities_total']}"
    skills_text = ", ".join(summary["skills_completed"]) if summary["skills_completed"] else "No skills completed yet"

    st.header("Evidence Pathway")
    snapshot_cols = st.columns(4)
    snapshot_cols[0].metric("Gene", summary["assigned_gene"])
    snapshot_cols[1].metric("Team label", summary["team_label"] or "Not set")
    snapshot_cols[2].metric("Score", f"{summary['score']} pts")
    snapshot_cols[3].metric("Required progress", progress_text)
    st.markdown(f"<div class='summary-skill-strip'>{display_value(skills_text)}</div>", unsafe_allow_html=True)

    nodes = [
        pathway_node("Assigned gene", "Workshop setup", summary["assigned_gene"], bool(summary["assigned_gene"])),
        pathway_node("Association evidence", "ADVP", advp_signal, bool(advp_signal)),
        pathway_node("GWAS table signal", "GenomicsDB", gwas_signal, bool(gwas_signal)),
        pathway_node("Dataset / locus zoom", "GenomicsDB", dataset_signal, bool(dataset_signal)),
        pathway_node("Variant record", "GenomicsDB", variant_signal, bool(variant_signal)),
        pathway_node("Browser region", "GenomicsDB", browser_region, bool(browser_region)),
        pathway_node("Functional annotation", "FILER / xQTL", functional_signal, bool(functional_signal)),
        pathway_node("Interpretation", "Synthesis", interpretation, bool(interpretation)),
    ]
    st.markdown(f"<div class='path-grid'>{''.join(nodes)}</div>", unsafe_allow_html=True)

    st.subheader("Carry-Forward Focus")
    focus_items = [
        ("Dataset / track", answer_value(summary, "genomicsdb", "Dataset or track name")),
        ("Locus zoom variant", answer_value(summary, "genomicsdb", "Locus zoom variant")),
        ("Variant context", first_answer(summary, "genomicsdb", ["Variant consequence", "Variant alleles", "Variant RefSNP"])),
        ("Genome browser region", answer_value(summary, "genomicsdb", "Region to carry forward")),
        ("Functional evidence", first_answer(summary, "functional", ["Dataset, track, or result name", "Evidence type"])),
        ("Limitation / question", answer_value(summary, "interpretation", "One limitation or unanswered question")),
    ]
    focus_html = "".join(
        f"<div class='focus-item'><div class='focus-label'>{escape(label)}</div><div class='focus-value'>{display_value(value)}</div></div>"
        for label, value in focus_items
    )
    st.markdown(f"<div class='focus-panel'>{focus_html}</div>", unsafe_allow_html=True)


def resource_url(resource):
    return RESOURCES[resource]


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
    st.caption("Scores are sorted by points, required activity progress, completed skills, and fewer hints used.")
    st.link_button("Return to workshop challenge", "?")

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


if st.query_params.get("view") == "leaderboard":
    render_leaderboard_view()


required_missions = [mission for mission in MISSIONS if not mission["bonus"]]
completed_required = sum(mission_complete(mission) for mission in required_missions)
progress = completed_required / len(required_missions)
score = sum(earned_points(mission) for mission in MISSIONS)
completed_skills = completed_skill_names(MISSIONS)

with st.sidebar:
    st.header("Workshop Progress")
    st.text_input("Table or group number", key="team_name", placeholder="e.g., Table 4")
    st.text_input("Team leader email (optional)", key="leader_email", placeholder="name@example.org")
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("Generate team label", use_container_width=True):
            st.session_state.team_label = random_team_label()
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
    render_completed_skills(completed_skills)
    st.link_button("🏆 View leaderboard", "?view=leaderboard", use_container_width=True)

st.title("NIAGADS Open Access Workshop Challenge")
st.subheader("Build a gene evidence summary")
st.markdown(
    f"Your team is reviewing **{st.session_state.assigned_gene}**. Complete the required activities in about 20 minutes; the API activity is optional bonus credit."
)

col1, col2, col3 = st.columns(3)
col1.metric("Assigned gene", st.session_state.assigned_gene)
col2.metric("Required activities", f"{completed_required}/{len(required_missions)}")
col3.metric("Score", f"{score} pts")
render_completed_skills(completed_skills)

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
        st.markdown(f"<span class='status-pill {pill_class}'>{status_text}</span>", unsafe_allow_html=True)
        render_activity_skills(mission)
    with header_cols[1]:
        label = f"+{mission['points']} bonus pts" if mission["bonus"] else f"{mission['points']} pts"
        st.metric("Value", label)

    st.write(mission["task"])
    if mission["id"] == "varixam":
        st.info("VarIXam is used here for ADSP variant inventory within a gene footprint, not variant interpretation.", icon="ℹ️")

    if mission["resources"]:
        link_cols = st.columns(max(len(mission["resources"]), 1))
        for idx, resource in enumerate(mission["resources"]):
            link_cols[idx].link_button(f"Open {resource}", resource_url(resource), use_container_width=True)

    with st.expander("Fallback question"):
        st.write(mission["fallback"])

    if st.button("Show hint (-1 point once)", key=f"hint_{mission['id']}"):
        st.session_state.hints_used.add(mission["id"])
    if mission["id"] in st.session_state.hints_used:
        st.warning(f"Hint: {mission['hint']}")

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
            if st.button("Show bonus hint", key=f"field_hint_{mission['id']}_{field['key']}"):
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

    st.markdown("</div>", unsafe_allow_html=True)

summary = build_summary()
st.divider()
render_evidence_pathway(summary)
st.divider()
st.header("Gene Evidence Summary Preview")
st.caption("This preview updates as your team fills in activity fields.")
st.json(summary, expanded=False)

st.divider()
st.header("Submit Results")
st.caption("Submit or update your team score when you are ready. The leaderboard is shown on a separate page.")

submit_cols = st.columns([1, 1])
with submit_cols[0]:
    if leaderboard_configured():
        if st.button("Submit / update leaderboard", type="primary", use_container_width=True):
            submit_to_leaderboard(summary, st.session_state.leaderboard_entry_id)
            st.session_state.leaderboard_submitted = True
            st.success("Leaderboard updated.")
    else:
        st.warning("Leaderboard submission is not configured yet.")
with submit_cols[1]:
    st.metric("Current score", f"{score} pts")

if st.session_state.leaderboard_submitted:
    st.success("This team has submitted during the current session. Submit again to update the score.")

st.link_button("🏆 Open leaderboard", "?view=leaderboard")
