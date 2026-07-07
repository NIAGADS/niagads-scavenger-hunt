# Scavenger Hunt Questions and Workflow per Site

## Top Genes

### Purpose

The ADSP Gene Verification Committe Top Genes Repositories provides access to a curated list of high-confidence AD/ADRD genes and loci that have been rigorously reviewed by domain experts. It helps researchers move from genetic association signals to prioritized targets for functional validation, mechanistic follow-up, and therapeutic discovery.

### Getting Started

Search for your assigned gene, the select `View all Results`

### Questions

* How many reported locus records are returned for this gene?
* What is the strongest support tier shown for this gene? Remember: Tier 1 = strongest support; Tier 7 = weakest support.
* Record one supporting study and one nearby gene listed in the table.

### Additional Essential Info

Methods, understanding the "tiers"  <https://adsp.niagads.org/wp-content/uploads/2022/05/SingleVariantTest-V42.pdf>

## ADVP

### Purpose

The Alzheimer's Disease Variant Portal is a curated, AD-specific GWAS catalog. It helps researchers browse reported AD genetic associations from the literature, including associated genes, loci and variants, contextualized by populations, phenotypes, and supporting studies.

### Getting Started

Select `Genes` from the top-level navigation and then search for your assigned gene.

### Questions

* How many curated associations are there for your gene in ADVP?
* Curated from how many distinct publications?
* Click on the number in the `Association records` column to view all curated associations for your gene. Record one SNP, one supporting PubMed ID, one phenotype, and one reported p-value or effect size from the table.

## VariXam

### Purpose

VariXam is an ADSP variant browser. It helps researchers find WGS/WES variants called in ADSP releases within a gene or genomic region, using GRCh38 coordinates and PASS-filtered released variant calls.

### Getting Started

Search for your assigned gene.

### Questions

* Record the total number of ADSP variant records found in the footprint of your assigned gene.
* Sort by the `Multiallelic` column and then filter (search) for variants called in the most recent ADSP release (R5).  Report the chromosome and position of one multi-allelic variant.
* What are the alternative alleles?

## GenomicsDB

### Purpose

The NIAGADS Alzheimer’s Genomics Database is an interactive AD/ADRD genetics knowledgebase containing genes, variants, genomic regions, annotations, and related evidence on GRCh38. It helps researchers search, browse, and analyze Alzheimer’s disease genetic data in one integrated resource.

### Getting Started

create starting point from what is already there (search for gene)

### Questions

leave as is for now

## Functional Genomics

## Section 1 - xQTL Browser

### Purpose

The NIAGADS xQTL Browser contains harmonized brain xQTL associations across histone acetylation, DNA methylation, gene expression, splicing, and protein abundance, spanning multiple cohorts, brain regions, and cell types. It helps researchers connect genetic variation with functional molecular mechanisms in AD-relevant brain datasets.

### Getting Started

Search for your assigned gene.

### Questions

* What is the total number of variants that target your assigned gene?
* Which xQTL type has the highest number of associations?

#### Section 1a

Click on the associations tab.

* Are the xQTL associations for this gene mostly found within the local gene region, or are there also associations linked through the broader 3D genome/TAD context? Hint: expand Cis/TAD association summary by xQTL type section
* Which variant has the most significant association with this target gene?
* For what xQTL type?

### Section 2 - FILER

### Getting Started

Select `Search` from the top-level navigation. Select `hg38` for the Genome Build and then submit your gene region (that you saved in the GenomicsDB section).

### Purpose

FILER is a harmonized functional genomics repository containing indexed, searchable datasets from more than 20 human functional genomics data sources. It helps researchers find and reuse regulatory and functional genomics evidence by tissue, cell type, biosample, assay, data type, or data collection in consistent formats.

### Questions

* How many overlapping functional annotations (hint database intervals) found for your gene region?
* What was the total search time?
* Open the `genomic feature type overlap` summary.  What type of genomic feature has the highest number of overlaps in your region?
* Bonus: What does that suggest about the types of regulatory or functional annotations available for this region? Hint: what are the caveats?
* In the overlap heatmap, find the darkest cell and hover over it. Which data source and tissue category does it represent, and how many overlaps are reported?
* Across the heatmap, which tissue categories show the strongest concentration of overlaps for your gene region? Are any of them relevant to AD biology?

## NIAGADS Open Access API

leave as is for now
