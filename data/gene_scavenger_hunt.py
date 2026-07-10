ASSIGNMENT_POOL = [
    "ABCA1",
    "ABCA7",
    "ABI3",
    "ACE",
    "ADAM10",
    "ADAMTS1",
    "ADAMTS20",
    "ADAMTS4",
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
    "NIAGADS Open Access API": "https://api.niagads.org/",
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
        "fields": [
            {
                "key": "topgenes-1",
                "label": "How many reported locus records are returned for this gene?",
                "type": "text",
            },
            {
                "key": "topgenes-2",
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
                "key": "topgenes-3",
                "label": "Record one supporting study listed in the table.",
                "type": "text",
            },
            {
                "key": "topgenes-4",
                "label": "Is this a gene also an Agora (AD Knowledge Portal) nominated target?",
                "type": "select",
                "options": ["", "yes", "no"],
            },
        ],
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
        "fields": [
            {
                "key": "varixam-1",
                "label": "What is the total number of ADSP variant records found in the footprint of your assigned gene?",
                "type": "text",
            },
            {
                "key": "varixam-2",
                "label": "Use sort and search options to identifiy multi-allelic variants called in the most recent ADSP release (58k sequences). Report either the Ref SNP (rs) ID or chr:position of one multi-allelic variant.",
                "type": "text",
                "hint": "Sort by the <code>Multiallelic</code> column so that <code>Yes</code> values are visible and then search for <code>R5</code>.",
            },
            {
                "key": "varixam-3",
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
        "fields": [
            {
                "key": "advp-1",
                "label": "How many curated associations are there for your gene in ADVP?",
                "type": "text",
            },
            {
                "key": "advp-2",
                "label": "How many different publications were manually reviewed to extract those associations?",
                "type": "text",
            },
            {
                "key": "advp-3",
                "label": "Browse the list of curated variants associated with your assigned genes.  Report one that catches your interest.",
                "type": "text",
                "hint": "Click on the number in the <code>Association records</code> column from your previous search result to view all curated associations for your gene. ",
            },
            {
                "key": "advp-4",
                "label": "What is the significance of this association (p-value)?",
                "type": "text",
            },
            {
                "key": "advp-5",
                "label": "What is the phenotypic context (e.g., population, disease) for the genetic association?",
                "hint": "Click <code>Show/Hide Columns</code> to display more detailed phenotypic information.",
                "type": "text",
            },
            {
                "key": "advp-6",
                "label": "What is the source (associated <code>PubMed ID</code>) for this observation?",
                "type": "text",
            },
        ],
    },
    {
        "id": "genomicsdb",
        "title": "Explore GWAS summary statistics",
        "skill": "Record Linker",
        "sub_skills": [
            {
                "skill": "AD Genetics Reporter",
                "fields": [
                    "genomicsdb-gene-annotations-2",
                    "genomicsdb-gene-annotations-3",
                    "genomicsdb-gene-annotations-6",
                    "genomicsdb-gene-annotations-4",
                    "genomicsdb-gene-annotations-5",
                    "genomicsdb-gene-annotations-7",
                ],
            },
            {
                "skill": "Record Linker",
                "fields": [
                    "genomicsdb-gene-annotations-1",
                    "genomicsdb-dataset-summary-1",
                    "genomicsdb-dataset-summary-2",
                    "genomicsdb-variant-record-1",
                    "genomicsdb-variant-record-2",
                ],
            },
            {
                "skill": "Data Miner",
                "fields": [
                    "genomicsdb-dataset-summary-3",
                    "genomicsdb-dataset-summary-4",
                    "genomicsdb-dataset-summary-5",
                    "genomicsdb-dataset-summary-6",
                    "genomicsdb-variant-record-4",
                    "genomicsdb-variant-record-5",
                ],
            },
            {
                "skill": "Genome Browser",
                "fields": [
                    "genomicsdb-genome-browser-1",
                    "genomicsdb-genome-browser-2",
                    "genomicsdb-genome-browser-3",
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
        "getting_started": "Search for the assigned gene.",
        "fields": [
            {
                "type": "section",
                "key": "genomicsdb-gene-annotations",
                "label": "Gene Annotations",
            },
            {
                "key": "genomicsdb-gene-annotations-1",
                "label": "What is the genomic location (chrN:start-end) of this gene?",
                "type": "text",
                "carry_forward": True,
            },
            {
                "key": "genomicsdb-gene-annotations-2",
                "label": "Which phenotype (specific disease, neuropathology, or biomarker) has the most number of trait associated variants proximal to this gene?",
                "hint": "Mouse over the interactive bar charts in the report header that provide a quick summary of significant AD/ADRD associations relative to the gene span.",
                "type": "text",
            },
            {
                "key": "genomicsdb-gene-annotations-3",
                "label": "Where are the majority of the informative variants located relative to the gene?",
                "type": "select",
                "options": ["", "upstream", "downstream", "in gene"],
            },
            {
                "key": "genomicsdb-gene-annotations-4",
                "label": "The GenomicsDB separates curated summary statistics datasets into AD and ADRD/AD Biomarker collections.  Which table will you browse?",
                "type": "select",
                "options": [
                    "",
                    "Alzheimer’s Disease",
                    "AD-related neuropathologies and biomarkers",
                ],
            },
            {
                "key": "genomicsdb-gene-annotations-5",
                "label": "Report one variant (Ref SNP ID or positional identifier) listed in the selected table that catches your interest.",
                "type": "text",
            },
            {
                "key": "genomicsdb-gene-annotations-6",
                "label": "What is the predicted functional consequence of the variant?",
                "hint": "Add the <code>Consequence</code> column to the table.",
                "type": "text",
            },
            {
                "key": "genomicsdb-gene-annotations-7",
                "label": "In which track (dataset) was this association reported?",
                "type": "text",
                "carry_forward": True,
            },
            {
                "type": "section",
                "key": "genomicsdb-dataset-summary",
                "label": "Dataset Summary",
                "next_step": "Click on the <code>track</code> name you selected to carry forward to open a brief report for this GWAS summary statistics dataset.",
            },
            {
                "key": "genomicsdb-dataset-summary-1",
                "label": "What is the accession number for this dataset?",
                "type": "text",
            },
            {
                "key": "genomicsdb-dataset-summary-2",
                "label": "Is it a NIAGADS or EMBL-EBI GWAS Catalog Accession?",
                "type": "select",
                "options": ["", "NIAGADS", "GWAS Catalog"],
            },
            {
                "key": "genomicsdb-dataset-summary-3",
                "label": "On what chromosome is the most significant GWAS signal?",
                "hint": "Answer at glance using the Manhattan plot.",
                "type": "text",
            },
            {
                "key": "genomicsdb-dataset-summary-4",
                "label": "List one or more potentially impacted genes associated with peaks other than the one identified for the previous quesiton.",
                "hint": "The Manhattan plot is interactive!",
                "type": "text",
            },
            {
                "key": "genomicsdb-dataset-summary-5",
                "label": "Report one <code>ADSP variant</code> that is reported to have a significant genetic association in this dataset.",
                "type": "text",
                "carry_forward": True,
                "hint": "ADSP variants have a red check in the <code>ADSP Variant?</code> column.",
            },
            {
                "key": "genomicsdb-dataset-summary-6",
                "label": "Are any nearby significant variants in LD with the variant you selected in ADSP samples (European/NHW)?",
                "hint": "Toggle the <code>LocusZoom</code> view from the <code>Top Variants</code> table toolbar and then check a row in the table to center the LocusZoom view on that variant. </br> </br>"
                "<strong>Future Feature</strong>: The upcoming release will have ADSP-population based linkage for more ethnic groups (populations). </br>"
                "These panels (<a href='https://dss.niagads.org/open-access-data-portal/#NG00067'>R5 58K Reference Panel</a>) are <code>Open Access</code> and available for download through the <code>NIAGADS DSS Open Access Portal</code> (filter for fileset <code>fsa000165</code>).",
                "type": "text",
            },
            {
                "type": "section",
                "key": "genomicsdb-variant-record",
                "label": "Variant Annotations",
                "next_step": "Click on the <code>variant</code> you selected to carry forward to open a variant annotation report.",
            },
            {
                "key": "genomicsdb-variant-record-1",
                "label": "Is this variant associated with a Ref SNP record? If so, what is its Ref SNP ID?",
                "type": "text",
            },
            {
                "key": "genomicsdb-variant-record-2",
                "label": "Is this variant multi-allelic or co-located with any other variants? If so, how many? Enter <strong>0</strong> for none.",
                "type": "text",
            },
            {
                "key": "genomicsdb-variant-record-3",
                "label": "Bonus: What is an <code>ADSP Variant</code>?",
                "type": "textarea",
                "required": False,
                "bonus_points": 1,
                "hint": "Mouse over the <code>ADSP Variant</code> badge in the report header.",
            },
            {
                "key": "genomicsdb-variant-record-4",
                "label": "Does this variant have any reported significant associations with AD-related neuropathologies or biomarkers?",
                "type": "select",
                "options": ["", "yes", "no"],
            },
            {
                "key": "genomicsdb-variant-record-5",
                "label": "How did you figure that out?",
                "type": "select",
                "options": [
                    "",
                    "Overview Summary Graphic",
                    "NIAGADS GWAS: AD-related neuropathologies and biomarkers",
                    "GWAS Catalog: Other Traits",
                ],
            },
            {
                "type": "section",
                "key": "genomicsdb-genome-browser",
                "label": "Genome Browser",
                "next_step": "Click the <code>View on Genome Browser</code> button in the variant report navigation menu on the page left.</br></br>"
                "In a new tab, the <code>NIAGADS Genome Browser</code> will open with the current variant highlighted.",
            },
            {
                "key": "genomicsdb-genome-browser-1",
                "label": "Genome Browser tracks are interactive! What is one new thing you can learn about the highlighed variant?",
                "hint": "Zoom in and then click on the highlighted square in the <code>ADSP 36K R4 Varaints</code> track. </br></br>"
                "<strong>Future Feature</strong>: The upcoming release will have updated ADSP reference tracks based on the newest data release (R5) with variants called from ~58k genomes.",
                "type": "text",
            },
            {
                "key": "genomicsdb-genome-browser-2",
                "label": "What does the color coding on the ADSP variant track tell us?",
                "hint": "Click on the track label to display the legend or on the gear to the right to select an alternative color scale and report what you discover.",
                "type": "select",
                "options": [
                    "",
                    "Variant Type",
                    "Consequence Severity",
                    "CADD Score",
                    "Consequence Type",
                    "Coding Variant Flag",
                ],
            },
            {
                "key": "genomicsdb-genome-browser-3",
                "label": "Search for the track you explored earlier and click the <code>Display Track</code> to load.  Report about a significant variant other than the one selected.",
                "hint": "Genome browser tracks are interactive!  Click on a point - what information is provided?  You may have to Zoom back out again!",
                "type": "text",
            },
        ],
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
        "fields": [
            {
                "key": "xqtl-1",
                "label": "What is the total number of variants that target your assigned gene?",
                "type": "text",
            },
            {
                "key": "xqtl-2",
                "label": "Which xQTL type has the highest number of associations?",
                "type": "select",
                "options": ["", "mQTL", "pQTL", "haQTL", "eQTL", "snuc-eQTL"],
            },
            {
                "type": "section",
                "key": "xqtl-associations-tab",
                "label": "Associations Browser",
                "next_step": "Select the <code>Associations</code> tab from the local record page navigation.",
            },
            {
                "key": "xqtl-associations-tab-1",
                "label": "Are the xQTL associations for this gene mostly found within the local gene region, or are there also associations linked through the broader 3D genome/TAD context?",
                "hint": "Expand the section labeled: <code>Cis/TAD association summary by xQTL type</code>.",
                "type": "select",
                "options": ["", "local gene region", "broader genomic context"],
            },
            {
                "key": "xqtl-associations-tab-2",
                "label": "Which variant has the most significant association with this target gene?",
                "hint": "Expand the section labeled: <code>Top associations per xQTL type</code>.",
                "type": "text",
            },
            {
                "key": "xqtl-associations-tab-3",
                "label": "In which context?",
                "type": "text",
            },
        ],
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
            "Select <code>Search</code> from the top-level navigation. Select <code>hg38</code> for the Genome Build and then enter the "
            "gene region - you recorded in the GenomicsDB Gene Annotation section."
        ),
        "fields": [
            {
                "key": "filer-1",
                "label": "How many overlapping functional annotations (database intervals) were found for your gene region?",
                "type": "text",
            },
            {
                "key": "filer-2",
                "label": "What was the total search time?",
                "type": "text",
            },
            {
                "key": "filer-3",
                "label": "Open the <code>Genomic Feature Type Overlap</code> summary. What type of genomic feature has the highest number of overlaps in your region?",
                "type": "text",
            },
            {
                "key": "filer-5",
                "label": "Bonus: What does that suggest about the types of regulatory or functional annotations available for this region? What caveats should you keep in mind?",
                "type": "textarea",
                "required": False,
                "bonus_points": 1,
                "hint": "Consider what overlap counts can and cannot tell you about disease mechanism.",
            },
            {
                "key": "filer-6",
                "label": "In the overlap heatmap, find the darkest cell and hover over it. Which data source does it represent?",
                "type": "text",
            },
            {
                "key": "filer-7",
                "label": "For that same darkest heatmap cell, which tissue category does it represent?",
                "type": "text",
            },
            {
                "key": "filer-8",
                "label": "For that same darkest heatmap cell, how many overlaps are reported?",
                "type": "text",
            },
            {
                "key": "filer-9",
                "label": "Across the heatmap, which tissue categories show the strongest concentration of overlaps for your gene region? Are any of them relevant to AD biology?",
                "type": "textarea",
            },
        ],
    },
    {
        "id": "interpretation",
        "title": "Summarize the evidence",
        "skill": "Evidence summary",
        "points": 4,
        "resources": [],
        "fields": [
            {
                "key": "interpretation-1",
                "label": "One-sentence interpretation",
                "type": "textarea",
            },
            {
                "key": "interpretation-2",
                "label": "Most useful resource",
                "type": "select",
                "options": [
                    "",
                    "GVC Top Genes",
                    "ADVP",
                    "GenomicsDB",
                    "VariXam",
                    "xQTL Browser",
                    "FILER",
                ],
            },
            {
                "key": "interpretation-3",
                "label": "One limitation or unanswered question",
                "type": "textarea",
            },
        ],
    },
    {
        "id": "api_bonus",
        "title": "Design an API integration",
        "skill": "Integration Contributor",
        "points": 0,
        "resources": ["NIAGADS Open Access API"],
        "resource_notes": [
            {
                "label": "NIAGADS Open Access API",
                "message": "This resource is currently being updated.  Limited endpoints available to explore now, but please check back in early Fall 2026 for expanded data and new features.",
            }
        ],
        "fields": [
            {
                "key": "api-1",
                "label": "Where could programmatic NIAGADS access fit into an external toolkit, analysis workflow, or data portal?",
                "type": "text",
            },
            {
                "key": "api-2",
                "label": "Bonus: What NIAGADS data or lookup would that integration need, and how would it help users?",
                "type": "textarea",
                "required": False,
                "bonus_points": 4,
            },
        ],
    },
]
