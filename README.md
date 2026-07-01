# NIAGADS Open Access Scavenger Hunt

A single-page Streamlit app for a 20–30 minute workshop where participants act as **AD Gene Detectives** building an evidence dossier for one Alzheimer’s disease gene.

## What participants do

Teams receive or choose one gene from:

`APOE`, `BIN1`, `TREM2`, `ABCA7`, `CLU`, `PICALM`, `CR1`, `SORL1`, `MS4A6A`, `CD33`

They complete mission cards using NIAGADS and related open resources:

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
- Team name and random codename generator
- Random assigned gene button plus manual gene override
- Visible 20-minute countdown timer
- Mission Control sidebar with timer, gene, score, progress, and earned badges
- Mission cards with resource buttons, required answer fields, fallback prompts, hints, and hint penalties
- Required and bonus mission styling
- Final Gene Evidence Dossier preview
- Downloadable JSON and CSV dossiers

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

- Suggested duration: 20 minutes of hunt time plus 5–10 minutes for discussion.
- The API mission is bonus and is not required for completion.
- Hints subtract 1 point once per mission.
- A mission is complete when all required fields for that mission are filled.
