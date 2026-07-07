Build and refine a single-page Streamlit app for a 20-30 minute NIAGADS Open Access genomics workshop.

The app should feel like a professional workshop challenge, not a roleplay scavenger hunt. Avoid detective/dossier language. Participants are genomics workshop attendees with varying skill levels who are reviewing open NIAGADS resources for one Alzheimer disease gene and building a concise gene evidence summary.

## Current Tone and UI Direction

- Use "workshop challenge", "activity", "skill", and "gene evidence summary" language.
- Avoid "detective", "dossier", "mission control", "codename", and similar roleplay terms.
- Keep points, progress, hints, completion states, and badge-style visual chips.
- Badge chips use a trophy icon and distinguish earned vs pending by color.
- Use a compact sidebar labeled "Workshop Progress" with team, team label, assigned gene, timer, score, progress, and completed skills.
- On initial page load for a new Streamlit session, assign a random gene and generate a random team label.
- Keep controls for manually rerolling the team label, randomly assigning another gene, and manually overriding the gene.
- Resource links should remain buttons.
- Keep the app single-page, with no database, using only Streamlit `session_state`.

## Resources

- ADVP: <https://advp.niagads.org/>
- GenomicsDB: <https://www.niagads.org/genomics>
- FILER: <https://tf.lisanwanglab.org/FILER/>
- VariXam: <https://varixam.niagads.org/>
- TopGenes: <https://topgenes.niagads.org/>
- xQTL Browser: <https://xqtl.niagads.org/>
- API: <https://api.niagads.org/>

## Genes

APOE, BIN1, TREM2, ABCA7, CLU, PICALM, CR1, SORL1, MS4A6A, CD33

## Activity Design Standard

Each resource activity should teach a realistic discovery path through that resource, not ask for one isolated fact. Future section rewrites should follow the GenomicsDB pattern:

- Start from the actual page or search behavior participants will use.
- Name the expected page context in the form of section headers, e.g. "Gene Record", "Dataset Record", "Variant Record", "Genome Browser".
- Ask questions in the order participants encounter the evidence.
- Make the activity feel like a story: "I started here, found this result, followed this link, learned this, and carried this forward."
- Avoid implying that one resource continues or validates another resource unless the workflow truly does that.
- Distinguish resources by what they are best for. For example, ADVP and GenomicsDB both show AD association-related evidence, but GenomicsDB is currently framed around NIAGADS GWAS summary statistics, linked records, datasets, and genome-browser exploration.
- Hints should guide where to look, not give away answers.
- Bonus questions may be optional by setting `required: False` and should not block activity completion.

## Game Mechanics

- Each activity has a skill label, point value, resource link, task, answer fields, hint, and fallback.
- An activity is complete when all required fields are filled.
- Optional fields do not block completion.
- Hints subtract 1 point once per activity.
- Field-specific bonus hints may exist and should not use the regular hint penalty unless explicitly requested.
- The API activity remains optional bonus credit.
- The final preview and downloads should be a gene evidence summary in JSON and CSV.

## Current GenomicsDB Activity Model

GenomicsDB is the main within-site navigation activity and is worth more points than simpler lookup activities.

Title: Explore GWAS summary statistics in GenomicsDB
Skills: Record Linker, Signal Mapper, Genome Browser
Points: 8

GenomicsDB is large enough to earn multiple badges within one activity:

- Record Linker: connect the gene record table result to linked dataset and variant records.
- Signal Mapper: use the dataset record, Manhattan plot, and locus zoom to choose a signal or peak to inspect.
- Genome Browser: load the same dataset track in the genome browser and choose a region to carry forward.

Discovery path:

1. Search and Gene Record
   - Participants open GenomicsDB and search for the assigned gene.
   - They record the Ensembl ID, genomic location, and an overview-chart takeaway.

2. Gene Record / NIAGADS GWAS
   - Participants go to Trait associations -> NIAGADS GWAS.
   - They choose either the Alzheimer disease or AD-related neuropathologies table.
   - They select one significant summary-statistics variant and record relative position, p-value, linked dataset/track, and whether it is marked in the ADSP Variant column.

3. Dataset Record
   - Participants open the linked dataset/track record.
   - They record the dataset title.
   - They use the dataset-level significant variants table or Manhattan plot to identify another strong region outside the assigned gene if possible.
   - They toggle locus zoom view on the Manhattan plot and select a variant or peak to inspect next.

4. Variant Record
   - Participants click the selected variant link and review the variant record header.
   - They record variant ID, RefSNP ID if shown, alleles, and consequence or impacted gene/transcript.
   - Optional bonus: if the variant is ADSP-flagged, describe what the ADSP Variant label indicates. The bonus hint should only tell them where to find the label, not provide the answer.

5. Genome Browser
   - Participants click View on Genome Browser.
   - They find and load the same dataset track used earlier.
   - They explore the track and identify a region or pattern worth inspecting in FILER.

6. Carry Forward
   - Participants record the final region to carry forward to the functional annotation activity.

Current GenomicsDB hint:

- Search for the gene, open the gene record, then go to Trait associations -> NIAGADS GWAS.
- Choose one significant summary-statistics variant with a linked dataset or track.
- Open the dataset record, use locus zoom to select a variant from the Manhattan plot, then use View on Genome Browser to load the same dataset track and choose a region for the functional annotation activity.

## Functional Annotation Follow-Up

The FILER/xQTL activity should use the region carried forward from GenomicsDB. It should not be a disconnected lookup for the assigned gene.

Current direction:

- Use the carried-forward region to look for one regulatory, functional, or QTL-related evidence item.
- FILER is preferred for regulatory/functional tracks.
- xQTL Browser is appropriate for QTL-style evidence.
- Participants should record the region used, evidence type, dataset/track/result name, resource used, and a brief note about how the annotation may help interpret the region.

## Content Constraints

- VariXam only provides lists of ADSP variants in a gene footprint.
- Do not describe VariXam as variant interpretation.
- Frame VariXam as variant inventory.
- Do not imply that an ADSP Variant flag indicates AD-risk association. The label means the variant is present in ADSP samples and passed ADSP quality control checks, but participants should discover that from the GenomicsDB variant record when answering the bonus prompt.

## Remaining Activities To Revisit

ADVP, VariXam, TopGenes, interpretation, and API still need future review so their language and workflows match the updated activity design standard. ADVP in particular should be revised later to clarify how its curated association evidence differs from GenomicsDB summary-statistics exploration.

## Files

- `app.py`
- `requirements.txt`
- `README.md`
- `prompt.md`
