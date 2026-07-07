import streamlit as st

from scoring import (
    completed_skill_names,
    earned_points,
    mission_complete,
    mission_ready,
    mission_skills,
    skill_complete,
)
from state import initialize_state
from summary import build_summary
from ui import (
    render_landing_page,
    render_leaderboard_view,
    render_missions,
    render_page_header,
    render_sidebar,
    render_styles,
    render_summary_and_submit,
)

st.set_page_config(
    page_title="NIAGADS Open Access AD Gene Challenge",
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
    "VariXam": "https://varixam.niagads.org/",
    "GVC Top Genes": "https://topgenes.niagads.org/",
    "xQTL Browser": "https://xqtl.niagads.org/",
    "API": "https://api.niagads.org/",
}

AWARD_ICON = "🏆"
INTRO_VIDEO_PATH = "assets/scavenger-hunt-intro.mp4"

MISSIONS = [
    {
        "id": "topgenes",
        "title": "Check gene prioritization",
        "skill": "Therapeutic Target Prioritization",
        "points": 3,
        "resources": ["GVC Top Genes"],
        "resource_notes": [
            {
                "label": "GVC Top Genes",
                "message": "Alpha release. This new resource is under active development, and content or interface details may change.</br></br>"
                "For now, please see the <a href='https://adsp.niagads.org/wp-content/uploads/2022/05/SingleVariantTest-V42.pdf' target='_blank' rel='noopener noreferrer'>ADSP GVC Methods</a> "
                "for details on how confidence tiers are defined and assigned.",
            }
        ],
        "purpose": (
            "The ADSP Gene Verification Committee Top Genes repository provides access to a curated list of "
            "high-confidence AD/ADRD genes and loci that have been rigorously reviewed by domain experts. It helps "
            "researchers move from genetic association signals to prioritized targets for functional validation, "
            "mechanistic follow-up, and therapeutic discovery."
        ),
        "getting_started": "Search for your assigned gene, then select <code>View all Results</code>.",
        "task": "Use GVC Top Genes to review how the assigned gene appears in curated reported locus records.",
        "fields": [
            {
                "key": "Reported locus records returned",
                "label": "How many reported locus records are returned for this gene?",
                "type": "text",
            },
            {
                "key": "Strongest support tier",
                "label": "What is the strongest support tier shown for this gene?",
                "hint": "Tier 1 = strongest support; Tier 7 = weakest support. More information about <a href='app/static/gvc-tiers.png' target='_blank'>GVC Confidence Tiers</a> (opens in new tab).",
                "type": "select",
                "options": [
                    "",
                    "Tier 1",
                    "Tier 2",
                    "Tier 3",
                    "Tier 4",
                    "Tier 5",
                    "Tier 6",
                    "Tier 7",
                ],
            },
            {
                "key": "Supporting study",
                "label": "Record one supporting study listed in the table.",
                "type": "text",
            },
            {
                "key": "Agora",
                "label": "Is this a gene also an Agora (AD Knowledge Portal) nominated target?",
                "type": "select",
                "options": ["", "yes", "no"],
            },
        ],
        "hint": "Use View all Results to see the table that contains reported locus records, support tiers, studies, and nearby genes.",
        "bonus": False,
    },
    {
        "id": "varixam",
        "title": "Inventory ADSP variants",
        "skill": "ADSP Variant Inspector",
        "points": 3,
        "resources": ["VariXam"],
        "purpose": (
            "VariXam is an ADSP variant browser. It helps researchers find WGS/WES variants called in "
            "ADSP releases within a gene or genomic region, using GRCh38 coordinates and PASS-filtered released "
            "variant calls."
        ),
        "getting_started": "Search for your assigned gene.",
        "task": "Use VariXam to inspect ADSP variant records in the footprint of your assigned gene.",
        "fields": [
            {
                "key": "Total ADSP variant records",
                "label": "What is the total number of ADSP variant records found in the footprint of your assigned gene?",
                "type": "text",
            },
            {
                "key": "R5 multiallelic variant coordinate",
                "label": "Use sort and search options to identifiy multi-allelic variants called in the most recent ADSP release (58k sequences). Report either the Ref SNP (rs) ID or chr:position of one multi-allelic variant.",
                "type": "text",
                "hint": "Sort by the <code>Multiallelic</code> column so that <code>Yes</code> values are visible and then search for <code>R5</code>.",
            },
            {
                "key": "Alternative alleles",
                "label": "Enter the variant alleles in <code>REF>ALT</code> format for this multiallelic variant.  Separate alternate alleles with <code>/</code> (for example, A>C/T).",
                "type": "text",
            },
        ],
    },
    {
        "id": "advp",
        "title": "Trace AD genetic associations",
        "skill": "AD Genetic Association Finder",
        "points": 4,
        "resources": ["ADVP"],
        "purpose": (
            "The Alzheimer's Disease Variant Portal is a curated, AD-specific GWAS catalog. It helps researchers "
            "browse reported AD genetic associations from the literature, including associated genes, loci and "
            "variants, contextualized by populations, phenotypes, and supporting studies."
        ),
        "getting_started": "Select <code>Genes</code> from the top-level navigation and then search for your assigned gene.",
        "task": "Use ADVP to review curated AD association evidence for the assigned gene.",
        "fields": [
            {
                "key": "Curated association count",
                "label": "How many curated associations are there for your gene in ADVP?",
                "type": "text",
            },
            {
                "key": "Distinct publication count",
                "label": "How many different publications were manually reviewed to extract those associations?",
                "type": "text",
            },
            {
                "key": "Example association SNP",
                "label": "Browse the list of curated variants associated with your assigned genes.  Report one that catches your interest.",
                "type": "text",
                "hint": "Click on the number in the <code>Association records</code> column from your previous search result to view all curated associations for your gene. ",
            },
            {
                "key": "Example association p-value or effect size",
                "label": "What is the significance of this association (p-value)?",
                "type": "text",
            },
            {
                "key": "Example association phenotype",
                "label": "What is the phenotypic context (e.g., population, disease) for the genetic association?",
                "type": "text",
            },
            {
                "key": "Example association PubMed ID",
                "label": "What is the source (associated <code>PubMed ID</code>) for this observation?",
                "type": "text",
            },
        ],
        "hint": "Start in the Genes view, then use the Association records link for your gene.",
        "bonus": False,
    },
    {
        "id": "genomicsdb",
        "title": "Explore GWAS summary statistics",
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
        "points": 10,
        "resources": ["GenomicsDB"],
        "resource_notes": [
            {
                "label": "GenomicsDB",
                "message": "This resource is currently being updated. Explore now, but please check back in early Fall 2026 for expanded data and new features.",
            }
        ],
        "purpose": (
            "The NIAGADS Alzheimer’s Genomics Database is an interactive AD/ADRD genetics knowledgebase containing "
            "genes, variants, genomic regions, annotations, and related evidence on GRCh38. It helps researchers "
            "search, browse, and analyze Alzheimer’s disease genetic data in one integrated resource."
        ),
        "getting_started": "Search for the assigned gene, then open the gene record.",
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
                "label": "Bonus: What is an <code>ADSP Variant</code>?",
                "type": "textarea",
                "required": False,
                "bonus_points": 1,
                "hint": (
                    "Open the linked variant record and mouse over the <code>ADSP Variant badge</code>."
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
        "id": "xqtl",
        "title": "Connect genetic variation to molecular function",
        "skill": "xQTL evidence",
        "points": 6,
        "resources": ["xQTL Browser"],
        "resource_notes": [
            {
                "label": "xQTL Browser",
                "message": "Alpha release. This new resource is under active development, and content or interface details may change.",
            }
        ],
        "purpose": (
            "The NIAGADS xQTL Browser contains harmonized brain xQTL associations across histone acetylation, "
            "DNA methylation, gene expression, splicing, and protein abundance, spanning multiple cohorts, brain "
            "regions, and cell types. It helps researchers connect genetic variation with functional molecular "
            "mechanisms in AD-relevant brain datasets."
        ),
        "getting_started": "Search for your assigned gene.",
        "task": "Use the xQTL Browser to review molecular association evidence connected to your assigned gene.",
        "fields": [
            {
                "key": "Total target variants",
                "label": "What is the total number of variants that target your assigned gene?",
                "type": "text",
            },
            {
                "key": "xQTL type with highest associations",
                "label": "Which xQTL type has the highest number of associations?",
                "type": "text",
            },
            {"type": "section", "label": "Associations Tab"},
            {
                "key": "Local or broader context",
                "label": "Are the xQTL associations for this gene mostly found within the local gene region, or are there also associations linked through the broader 3D genome/TAD context?",
                "type": "textarea",
            },
            {
                "key": "Most significant association variant",
                "label": "Which variant has the most significant association with this target gene?",
                "type": "text",
            },
            {
                "key": "Most significant association xQTL type",
                "label": "For what xQTL type?",
                "type": "text",
            },
        ],
        "hint": "Click on the Associations tab, then expand the Cis/TAD association summary by xQTL type section.",
        "bonus": False,
    },
    {
        "id": "filer",
        "title": "Exploring Regulatory and Functional Context",
        "skill": "Functional annotation",
        "points": 6,
        "resources": ["FILER"],
        "resource_notes": [
            {
                "label": "FILER",
                "message": "This resource is currently being updated. Explore now, but please check back in early Fall 2026 for expanded data and new features.",
            }
        ],
        "purpose": (
            "FILER is a harmonized functional genomics repository containing indexed, searchable datasets from "
            "more than 20 human functional genomics data sources. It helps researchers find and reuse regulatory "
            "and functional genomics evidence by tissue, cell type, biosample, assay, data type, or data collection "
            "in consistent formats."
        ),
        "getting_started": (
            "Select <code>Search</code> from the top-level navigation. Select <code>hg38</code> for the Genome Build and then submit your "
            "gene region from the GenomicsDB section."
        ),
        "task": "Use FILER to review functional annotations overlapping the region carried forward from GenomicsDB.",
        "fields": [
            {
                "key": "Region searched in FILER",
                "label": "What gene region from the GenomicsDB section did you submit to FILER?",
                "type": "text",
            },
            {
                "key": "Overlapping functional annotations",
                "label": "How many overlapping functional annotations (database intervals) were found for your gene region?",
                "type": "text",
            },
            {
                "key": "Total search time",
                "label": "What was the total search time?",
                "type": "text",
            },
            {
                "key": "Highest overlap genomic feature type",
                "label": "Open the <code>genomic feature type overlap</code> summary. What type of genomic feature has the highest number of overlaps in your region?",
                "type": "text",
            },
            {
                "key": "Functional annotation interpretation bonus",
                "label": "Bonus: What does that suggest about the types of regulatory or functional annotations available for this region? What caveats should you keep in mind?",
                "type": "textarea",
                "required": False,
                "bonus_points": 1,
                "hint": "Consider what overlap counts can and cannot tell you about disease mechanism.",
            },
            {
                "key": "Darkest heatmap data source",
                "label": "In the overlap heatmap, find the darkest cell and hover over it. Which data source does it represent?",
                "type": "text",
            },
            {
                "key": "Darkest heatmap tissue category",
                "label": "For that same darkest heatmap cell, which tissue category does it represent?",
                "type": "text",
            },
            {
                "key": "Darkest heatmap overlap count",
                "label": "For that same darkest heatmap cell, how many overlaps are reported?",
                "type": "text",
            },
            {
                "key": "Strongest heatmap tissue categories",
                "label": "Across the heatmap, which tissue categories show the strongest concentration of overlaps for your gene region? Are any of them relevant to AD biology?",
                "type": "textarea",
            },
        ],
        "hint": "Use the carried-forward GenomicsDB region, then inspect the feature type summary and heatmap.",
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
        "points": 4,
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

if not st.session_state.hunt_started:
    render_landing_page(INTRO_VIDEO_PATH)
    st.stop()


required_missions = [mission for mission in MISSIONS if not mission.get("bonus", None)]
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
    mission_ready,
    mission_skills,
    skill_complete,
    resource_url,
)

summary = build_summary(MISSIONS)
render_summary_and_submit(summary, score)
