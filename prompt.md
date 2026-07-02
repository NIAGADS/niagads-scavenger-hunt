Build a Streamlit app for a 20–30 minute NIAGADS Open Access scavenger hunt workshop.

Theme:
Participants are “AD Gene Detectives” building an evidence dossier for one Alzheimer’s disease gene.

Resources:

- ADVP: <https://advp.niagads.org/>
- GenomicsDB: <https://www.niagads.org/genomics>
- FILER: <https://tf.lisanwanglab.org/FILER/>
- VarIXam: <https://varixam.niagads.org/>
- TopGenes: <https://topgenes.niagads.org/>
- xQTL Browser: <https://xqtl.niagads.org/>
- API: <https://api.niagads.org/>

Important content constraint:
VarIXam only provides lists of ADSP variants in a gene footprint. Do not describe it as variant interpretation. Frame it as “variant inventory.”

Core requirements:

- single-page Streamlit app
- no database
- use Streamlit session_state only
- team name input
- random team codename generator
- random assigned gene button
- manual gene override dropdown
- visible 20-minute countdown timer or elapsed timer
- progress bar
- current score
- mission cards
- hint buttons
- hint penalty
- badges earned
- final evidence dossier preview
- downloadable JSON and CSV evidence dossier
- README and requirements.txt for Streamlit Cloud deployment

Genes:
APOE, BIN1, TREM2, ABCA7, CLU, PICALM, CR1, SORL1, MS4A6A, CD33

Game mechanics:

- Each mission has a badge, point value, resource link, task, answer fields, hint, and fallback question.
- A mission is complete when all required fields are filled.
- Hints subtract 1 point once per mission.
- Bonus API mission gives bonus points but is not required for completion.
- Show earned badges as visual chips near the top.
- Show incomplete, complete, and bonus missions differently.
- At the end, generate a “Gene Evidence Dossier” summarizing all answers.

Mission definitions:

1. ADVP Mission
Title: Confirm the AD signal
Badge: Association Scout
Resource: ADVP
Points: 3
Task: Search the assigned gene in ADVP and determine whether it has Alzheimer’s disease association evidence.
Required fields:

- AD association status
- One association or evidence detail
Fallback:
- If no result is found, write what ADVP is designed to help users find.
Hint:
- Search by gene symbol and look for curated association/evidence records.

1. GenomicsDB Mission
Title: Map the genomic territory
Badge: Genome Navigator
Resource: GenomicsDB
Points: 3
Task: Find the genomic location or region for the assigned gene.
Required fields:

- Chromosome
- Start coordinate
- End coordinate
Fallback:
- If coordinates are hard to find, record the page/result where the gene appears.
Hint:
- Search the gene symbol and look for chromosome and coordinate range.

1. VarIXam Mission
Title: Inventory ADSP variants
Badge: Variant Scout
Resource: VarIXam
Points: 3
Task: Find ADSP variants overlapping the assigned gene footprint. Record one example variant or summarize the returned variant set.
Required fields:

- Example variant ID or coordinate
- Variant density: none / few / many
Fallback:
- If too many variants are returned, write “many” and describe what kind of list VarIXam provides.
Hint:
- This is an inventory task, not interpretation. Any returned ADSP variant is acceptable.

1. FILER/xQTL Mission
Title: Track functional evidence
Badge: QTL Tracker
Resources: FILER and xQTL Browser
Points: 4
Task: Find one regulatory, functional, or QTL-related evidence item for the assigned gene or nearby region.
Required fields:

- Evidence type
- Dataset, track, or result name
- Which resource was used: FILER or xQTL Browser
Fallback:
- If no evidence is found, describe what kind of evidence FILER or xQTL Browser is intended to provide.
Hint:
- Use xQTL for QTL-style evidence. Use FILER for functional or regulatory track evidence.

1. TopGenes Mission
Title: Check gene prioritization
Badge: Priority Analyst
Resource: TopGenes
Points: 3
Task: Look up the assigned gene and record its prioritization information if available.
Required fields:

- Rank, score, category, or “not found”
- Brief note on what the prioritization suggests
Fallback:
- If no gene result is found, describe what TopGenes is designed to support.
Hint:
- Do not over-interpret. Capture how the resource ranks or categorizes the gene.

1. Interpretation Mission
Title: Build the evidence dossier
Badge: Evidence Curator
Resource: none
Points: 4
Task: Write a short synthesis of what the collected evidence suggests.
Required fields:

- One-sentence interpretation
- Most useful resource
- One limitation or unanswered question
Fallback:
- None
Hint:
- Good answers combine association, genomic context, variant inventory, and functional/prioritization evidence.

1. API Bonus Mission
Title: Automate the next hunt
Badge: API Strategist
Resource: API
Points: 2 bonus
Task: Identify one step in the scavenger hunt that should eventually be automated through the NIAGADS API.
Required fields:

- Step to automate
- Why automation would help
Fallback:
- Name one lookup that would be useful to retrieve programmatically.
Hint:
- Think repeated lookup, coordinate retrieval, variant inventory, evidence aggregation, or report generation.

Visual design:

- Use wide layout
- Use clear mission cards
- Use emoji sparingly for badges/progress
- Use colored status indicators if possible
- Avoid childish styling
- Make it professional but game-like
- Keep all resource links as buttons
- Show a compact “Mission Control” sidebar with team, gene, timer, score, progress, and badges

Files to create:

- app.py
- requirements.txt
- README.md
