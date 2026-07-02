# NIAGADS Open Access Workshop Challenge

A single-page Streamlit app for a 20–30 minute genomics workshop where teams review open NIAGADS resources for one Alzheimer’s disease gene and build a gene evidence summary.

## What participants do

Teams receive or choose one gene from:

`APOE`, `BIN1`, `TREM2`, `ABCA7`, `CLU`, `PICALM`, `CR1`, `SORL1`, `MS4A6A`, `CD33`

They complete guided activities using NIAGADS and related open resources:

- [ADVP](https://advp.niagads.org/)
- [GenomicsDB](https://www.niagads.org/genomics)
- [FILER](https://tf.lisanwanglab.org/FILER/)
- [VarIXam](https://varixam.niagads.org/)
- [TopGenes](https://topgenes.niagads.org/)
- [xQTL Browser](https://xqtl.niagads.org/)
- [NIAGADS API](https://api.niagads.org/)

VarIXam is framed as an **ADSP variant inventory** activity: participants record variants overlapping a gene footprint or summarize the returned variant set. The app does not present VarIXam as variant interpretation.

## Features

- Single-page Streamlit app
- No database; uses `st.session_state` only
- Team name and random team label generator
- Random assigned gene button plus manual gene override
- Visible 20-minute countdown timer
- Workshop Progress sidebar with timer, gene, score, progress, and completed skills
- Activity sections with resource buttons, required answer fields, fallback prompts, hints, and hint penalties
- Required and bonus activity styling
- Final Gene Evidence Summary preview
- Downloadable JSON and CSV summaries

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

1. Push this repository to GitHub.
2. In Streamlit Community Cloud, create a new app from the repository.
3. Set the main file path to `app.py`.
4. Deploy. Streamlit will install dependencies from `requirements.txt`.

## Workshop facilitation notes

- Suggested duration: 20 minutes of activity time plus 5–10 minutes for discussion.
- The API activity is bonus and is not required for completion.
- Hints subtract 1 point once per activity.
- An activity is complete when all required fields for that activity are filled.
