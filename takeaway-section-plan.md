# Plan: Evidence Trail Summary

Replace the current `Carry-Forward Focus` display with an `Evidence Trail Summary`.

The purpose of this section is to show how the participant traced one assigned gene through the scavenger hunt resources. It should not display raw answers as unrelated cards.

The summary should follow this path:

```text
assigned gene → GVC Top Genes → VariXam → ADVP → GenomicsDB → Genome Browser → xQTL Browser → FILER → final interpretation
```

Use one vertical timeline/stepper. Each step should show:

- resource name
- evidence type
- participant finding
- learning point

Missing answers should display as:

```text
Not completed
```

Do not include the API bonus in the main evidence trail. If the API bonus was answered, show it separately below the trail.

## Evidence Trail Content

Use these steps:

| Step | Resource | Evidence type | Finding | Learning point |
|---|---|---|---|---|
| 1 | Assigned Gene | Workshop starting point | `assigned_gene` | The same gene is followed across prioritization, variant, association, GWAS, and functional genomics resources. |
| 2 | GVC Top Genes | Gene prioritization | `topgenes-2` | Shows whether the gene has expert-reviewed AD/ADRD support. |
| 3 | VariXam | ADSP variant inventory | `varixam-1` as `[value] ADSP variant records in the gene footprint` | Shows released ADSP WGS/WES variants observed in the assigned gene footprint. |
| 4 | ADVP | Curated AD association evidence | `advp-3`; add `advp-4` if present | Links the gene or locus to manually curated AD genetic association literature. |
| 5 | GenomicsDB | GWAS summary statistics and annotation context | Prefer `genomicsdb-dataset-summary-5` + `genomicsdb-gene-annotations-7`; otherwise `genomicsdb-gene-annotations-5`; otherwise `genomicsdb-gene-annotations-7` | Connects the gene region to GWAS datasets, traits, variants, and predicted functional annotations. |
| 6 | Genome Browser | Regional genomic context | `genomicsdb-genome-browser-1` | Shows the selected variant in local genomic and annotation context. |
| 7 | xQTL Browser | Molecular
