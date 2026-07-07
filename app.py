import streamlit as st

from scoring import (
    completed_skill_names,
    earned_points,
    mission_complete,
    mission_skills,
    skill_complete,
)
from state import initialize_state
from summary import build_summary
from ui import (
    render_leaderboard_view,
    render_missions,
    render_page_header,
    render_sidebar,
    render_styles,
    render_summary_and_submit,
)

st.set_page_config(
    page_title="NIAGADS AD Gene Workshop Challenge",
    page_icon="🧬",
    layout="wide",
)

ASSIGNMENT_POOL = [
    "ABCA1",
    "ABCA7",
    "ABI3",
    "ACE",
    "ADAM10",
    "ADAMTS1",
    "ADAMTS20",
    "ADAMTS4",
    "ANK3",
    "APH1B",
    "APOC1",
    "APOC2",
    "APOE",
    "APP",
    "BCAM",
    "BIN1",
    "CASS4",
    "CD2AP",
    "CD33",
    "CLNK",
    "CLPTM1",
    "CLU",
    "CNTNAP2",
    "COBL",
    "CR1",
    "ECHDC3",
    "EED",
    "EPHA1",
    "FBXL7",
    "FERMT2",
    "FST",
    "GRN",
    "HESX1",
    "HS3ST1",
    "IL34",
    "INPP5D",
    "INPPD5",
    "IQCK",
    "JAZF1",
    "KAT8",
    "MEF2C",
    "MS4A",
    "MS4A2",
    "MS4A4A",
    "MS4A6A",
    "NDUFAF6",
    "NME8",
    "NYAP1",
    "PICALM",
    "PILRA",
    "PLCG2",
    "PLEKHA1",
    "PSEN1",
    "PTK2B",
    "RIN3",
    "SCIMP",
    "SLC10A2",
    "SLC24A4",
    "SORL1",
    "SPI1",
    "SPPL2A",
    "TMEM106B",
    "TOMM40",
    "TP53INP1",
    "TREM2",
    "TREML2",
    "WNT3",
    "WWOX",
    "ZCWPW1",
]

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

MISSIONS = [
    {
        "id": "topgenes",
        "title": "Check gene prioritization",
        "skill": "Gene prioritization",
        "points": 3,
        "resources": ["TopGenes"],
        "task": "Look up the assigned gene and record its prioritization information if available.",
        "fields": [
            {
                "key": "Rank, score, category, or not found",
                "label": "Rank, score, category, or “not found”",
                "type": "text",
            },
            {
                "key": "Brief note on what the prioritization suggests",
                "label": "Brief note on what the prioritization suggests",
                "type": "textarea",
            },
        ],
        "hint": "Do not over-interpret. Capture how the resource ranks or categorizes the gene.",
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
            {
                "key": "Example variant ID or coordinate",
                "label": "Example variant ID or coordinate",
                "type": "text",
            },
            {
                "key": "Variant density",
                "label": "Variant density",
                "type": "select",
                "options": ["", "none", "few", "many"],
            },
        ],
        "hint": "This is an inventory task, not interpretation. Any returned ADSP variant is acceptable.",
        "bonus": False,
    },
    {
        "id": "advp",
        "title": "Review AD association evidence",
        "skill": "Association review",
        "points": 3,
        "resources": ["ADVP"],
        "task": "Search the assigned gene in ADVP and determine whether it has Alzheimer’s disease association evidence.",
        "fields": [
            {
                "key": "AD association status",
                "label": "AD association status",
                "type": "text",
            },
            {
                "key": "One association or evidence detail",
                "label": "One association or evidence detail",
                "type": "textarea",
            },
        ],
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
            {
                "key": "Ensembl ID",
                "label": "After searching for the assigned gene, what Ensembl ID is shown?",
                "type": "text",
            },
            {
                "key": "Gene location",
                "label": "What genomic location is shown on the gene record?",
                "type": "text",
            },
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
            {
                "key": "Selected variant",
                "label": "Which significant summary-statistics variant did you choose from the table?",
                "type": "text",
            },
            {
                "key": "Relative position",
                "label": "Where is that variant relative to the gene?",
                "type": "select",
                "options": ["", "upstream", "in gene", "downstream"],
            },
            {
                "key": "Variant p-value",
                "label": "What p-value is reported for that variant?",
                "type": "text",
            },
            {
                "key": "Dataset or track name",
                "label": "What linked dataset or track contains this summary-statistics result?",
                "type": "text",
            },
            {
                "key": "ADSP variant",
                "label": "Is the selected variant marked in the ADSP Variant column?",
                "type": "select",
                "options": ["", "yes", "no", "not shown"],
            },
            {"type": "section", "label": "Dataset Record"},
            {
                "key": "Dataset record title",
                "label": "After opening the dataset link, what is the dataset record title?",
                "type": "text",
            },
            {
                "key": "Dataset top region",
                "label": "From the dataset record, identify another strong association region outside the assigned gene if possible.",
                "type": "text",
            },
            {
                "key": "Dataset top result",
                "label": "What top variant, p-value, or nearest result supports that region?",
                "type": "text",
            },
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
            {
                "key": "Variant record ID",
                "label": "After clicking the selected variant, what variant ID appears in the header?",
                "type": "text",
            },
            {
                "key": "Variant RefSNP",
                "label": "What RefSNP ID is shown, if any?",
                "type": "text",
            },
            {
                "key": "Variant alleles",
                "label": "What alleles are shown in the variant record header?",
                "type": "text",
            },
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
        "hint": (
            "Search for the gene, open the gene record, then go to Trait associations → NIAGADS GWAS. Choose one "
            "significant summary-statistics variant with a linked dataset or track. Open the dataset record, use "
            "locus zoom to select a variant from the Manhattan plot, then use View on Genome Browser to load the "
            "same dataset track and choose a region for the functional annotation activity."
        ),
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
            {
                "key": "Dataset, track, or result name",
                "label": "Dataset, track, or result name",
                "type": "text",
            },
            {
                "key": "Which resource was used",
                "label": "Which resource was used",
                "type": "select",
                "options": ["", "FILER", "xQTL Browser"],
            },
            {
                "key": "Functional annotation note",
                "label": "Brief note on how this annotation may help interpret the region",
                "type": "textarea",
            },
        ],
        "hint": (
            "Use FILER for regulatory tracks and xQTL Browser for QTL-style evidence. Start with the region "
            "from GenomicsDB so this activity connects back to the dataset-level GWAS result."
        ),
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
            {
                "key": "One-sentence interpretation",
                "label": "One-sentence interpretation",
                "type": "textarea",
            },
            {
                "key": "Most useful resource",
                "label": "Most useful resource",
                "type": "text",
            },
            {
                "key": "One limitation or unanswered question",
                "label": "One limitation or unanswered question",
                "type": "textarea",
            },
        ],
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
            {
                "key": "Why automation would help",
                "label": "Why automation would help",
                "type": "textarea",
            },
        ],
        "hint": "Think repeated lookup, coordinate retrieval, variant inventory, evidence aggregation, or report generation.",
        "bonus": True,
    },
]


def resource_url(resource):
    return RESOURCES[resource]


initialize_state(ASSIGNMENT_POOL)
render_styles()


if st.query_params.get("view") == "leaderboard":
    render_leaderboard_view()


required_missions = [mission for mission in MISSIONS if not mission["bonus"]]
completed_required = sum(mission_complete(mission) for mission in required_missions)
progress = completed_required / len(required_missions)
score = sum(earned_points(mission) for mission in MISSIONS)
completed_skills = completed_skill_names(MISSIONS)

render_sidebar(
    score,
    progress,
    completed_required,
    len(required_missions),
    completed_skills,
    ASSIGNMENT_POOL,
    AWARD_ICON,
)
render_page_header(
    completed_required, len(required_missions), score, completed_skills, AWARD_ICON
)
render_missions(
    MISSIONS,
    AWARD_ICON,
    mission_complete,
    mission_skills,
    skill_complete,
    resource_url,
)

summary = build_summary(MISSIONS)
render_summary_and_submit(summary, score)
