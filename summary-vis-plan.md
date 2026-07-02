# Visual Evidence Summary First Pass

## Summary

Add a visual evidence summary above the raw JSON preview in `app.py`. The display should show the team’s evidence path from assigned gene through key resources and the carry-forward region, without duplicating every form answer. Keep the raw JSON preview underneath.

## Implementation Changes

- Add helper functions to extract selected answers from `summary` by activity title and answer key.
- Add `render_evidence_pathway(summary)` with:
  - **Gene Snapshot**: assigned gene, team label, score, required progress, completed skills.
  - **Evidence Pathway**: compact visual nodes for Gene, ADVP, GenomicsDB GWAS, Dataset Signal, Variant Record, Genome Browser, Functional Annotation, Interpretation.
  - **Carry-Forward Focus**: dataset/track, locus zoom variant, variant consequence, genome browser region, FILER/xQTL evidence, limitation.
- Add CSS for pathway nodes:
  - complete nodes use green accent styling.
  - pending nodes use muted gray styling.
  - carry-forward panel uses a restrained highlight treatment.
- Place the visual summary immediately before `Gene Evidence Summary Preview`.
- Leave JSON preview in place as raw submission data.

## Behavior

- Do not relist every answer in a table.
- Show “Pending” or “Not recorded yet” when key values are missing.
- Do not change scoring, completion logic, badges, leaderboard behavior, Google Sheets storage, or `prompt.md`.

## Assumptions

- First pass uses Streamlit markdown/columns/CSS only.
- The graphic should be instructional and compact, not decorative.
