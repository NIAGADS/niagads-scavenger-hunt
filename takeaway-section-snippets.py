"""
Suggested Streamlit snippets for replacing the current carry-forward summary
with an Evidence Trail Summary.

Usage:
    1. Copy these functions into the Streamlit app.
    2. Call inject_evidence_trail_css() once before rendering the summary.
    3. Replace the old carry-forward summary call with:

        render_evidence_trail_summary(st.session_state.answers)

Assumption:
    `answers` is a dict keyed by scavenger hunt field ids.
"""

from __future__ import annotations

import html
from typing import Any

import streamlit as st

NOT_COMPLETED = "Not completed"


def answer_value(answers: dict[str, Any], key: str) -> str:
    """Return a stripped answer value as text, or an empty string."""
    value = answers.get(key)

    if value is None:
        return ""

    value = str(value).strip()
    return value


def display_value(value: str) -> str:
    """Return display-safe fallback text for missing answers."""
    return value if value else NOT_COMPLETED


def format_varixam_finding(answers: dict[str, Any]) -> str:
    count = answer_value(answers, "varixam-1")

    if not count:
        return NOT_COMPLETED

    return f"{count} ADSP variant records in the gene footprint"


def format_advp_finding(answers: dict[str, Any]) -> str:
    variant = answer_value(answers, "advp-3")
    pvalue = answer_value(answers, "advp-4")

    if variant and pvalue:
        return f"{variant}; p-value: {pvalue}"

    if variant:
        return variant

    return NOT_COMPLETED


def format_genomicsdb_finding(answers: dict[str, Any]) -> str:
    selected_variant = answer_value(answers, "genomicsdb-gene-annotations-5")
    selected_track = answer_value(answers, "genomicsdb-gene-annotations-7")
    adsp_variant = answer_value(answers, "genomicsdb-dataset-summary-5")

    if adsp_variant and selected_track:
        return f"{adsp_variant} in {selected_track}"

    if selected_variant:
        return selected_variant

    if selected_track:
        return selected_track

    return NOT_COMPLETED


def format_xqtl_finding(answers: dict[str, Any]) -> str:
    xqtl_type = answer_value(answers, "xqtl-2")
    top_variant = answer_value(answers, "xqtl-associations-tab-2")
    context = answer_value(answers, "xqtl-associations-tab-3")

    if top_variant and context:
        return f"{top_variant} in {context}"

    if top_variant:
        return top_variant

    if xqtl_type:
        return xqtl_type

    return NOT_COMPLETED


def format_filer_finding(answers: dict[str, Any]) -> str:
    feature_type = answer_value(answers, "filer-3")
    heatmap_source = answer_value(answers, "filer-6")
    heatmap_tissue = answer_value(answers, "filer-7")
    heatmap_count = answer_value(answers, "filer-8")
    tissue_summary = answer_value(answers, "filer-9")

    if feature_type:
        return f"Top overlapping feature type: {feature_type}"

    if heatmap_source and heatmap_tissue and heatmap_count:
        return f"{heatmap_count} overlaps from {heatmap_source} in {heatmap_tissue}"

    if tissue_summary:
        return tissue_summary

    return NOT_COMPLETED


def build_evidence_trail_steps(answers: dict[str, Any]) -> list[dict[str, str]]:
    assigned_gene = answer_value(answers, "assigned_gene") or "Assigned gene"

    return [
        {
            "resource": "Assigned Gene",
            "evidence_type": "Workshop starting point",
            "finding": assigned_gene,
            "learning_point": "The same gene is followed across prioritization, variant, association, GWAS, and functional genomics resources.",
        },
        {
            "resource": "GVC Top Genes",
            "evidence_type": "Gene prioritization",
            "finding": display_value(answer_value(answers, "topgenes-2")),
            "learning_point": "Shows whether the gene has expert-reviewed AD/ADRD support.",
        },
        {
            "resource": "VariXam",
            "evidence_type": "ADSP variant inventory",
            "finding": format_varixam_finding(answers),
            "learning_point": "Shows released ADSP WGS/WES variants observed in the assigned gene footprint.",
        },
        {
            "resource": "ADVP",
            "evidence_type": "Curated AD association evidence",
            "finding": format_advp_finding(answers),
            "learning_point": "Links the gene or locus to manually curated AD genetic association literature.",
        },
        {
            "resource": "GenomicsDB",
            "evidence_type": "GWAS summary statistics and annotation context",
            "finding": format_genomicsdb_finding(answers),
            "learning_point": "Connects the gene region to GWAS datasets, traits, variants, and predicted functional annotations.",
        },
        {
            "resource": "Genome Browser",
            "evidence_type": "Regional genomic context",
            "finding": display_value(
                answer_value(answers, "genomicsdb-genome-browser-1")
            ),
            "learning_point": "Shows the selected variant in local genomic and annotation context.",
        },
        {
            "resource": "xQTL Browser",
            "evidence_type": "Molecular association context",
            "finding": format_xqtl_finding(answers),
            "learning_point": "Connects genetic variation to molecular readouts such as expression, splicing, methylation, histone acetylation, or protein abundance.",
        },
        {
            "resource": "FILER",
            "evidence_type": "Regulatory and functional annotation context",
            "finding": format_filer_finding(answers),
            "learning_point": "Shows what regulatory or functional annotations overlap the gene region and what biological contexts may be relevant.",
        },
        {
            "resource": "Final Interpretation",
            "evidence_type": "Synthesis",
            "finding": display_value(answer_value(answers, "interpretation-1")),
            "learning_point": "The value of the scavenger hunt is linking evidence across resources rather than relying on a single record or score.",
        },
    ]


def inject_evidence_trail_css() -> None:
    """Inject CSS for the evidence trail display."""
    st.markdown(
        """
        <style>
        .evidence-trail-container {
            border: 1px solid #d8e2ef;
            border-radius: 12px;
            padding: 1.25rem;
            background: #ffffff;
            margin-top: 1rem;
            margin-bottom: 1.5rem;
        }

        .evidence-step {
            display: flex;
            gap: 1rem;
            padding: 1rem 0;
            border-bottom: 1px solid #eef2f6;
        }

        .evidence-step:last-child {
            border-bottom: none;
        }

        .evidence-step-number {
            min-width: 2rem;
            height: 2rem;
            border-radius: 999px;
            background: #e8f1fb;
            color: #1f4e79;
            font-weight: 700;
            display: flex;
            align-items: center;
            justify-content: center;
            line-height: 2rem;
        }

        .evidence-step-content {
            flex: 1;
        }

        .evidence-resource {
            font-weight: 700;
            font-size: 1rem;
            color: #26323f;
            margin-bottom: 0.15rem;
        }

        .evidence-type {
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #5d6b7a;
            font-weight: 700;
            margin-bottom: 0.4rem;
        }

        .evidence-finding {
            color: #26323f;
            margin-bottom: 0.2rem;
        }

        .evidence-learning-point {
            color: #405064;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_evidence_trail_summary(answers: dict[str, Any]) -> None:
    """Render the replacement summary section."""
    assigned_gene = answer_value(answers, "assigned_gene") or "the assigned gene"
    steps = build_evidence_trail_steps(answers)

    st.markdown("## Evidence Trail Summary")
    st.caption(
        f"How this scavenger hunt connected {assigned_gene} across NIAGADS resources"
    )

    st.markdown('<div class="evidence-trail-container">', unsafe_allow_html=True)

    for index, step in enumerate(steps, start=1):
        resource = html.escape(step["resource"])
        evidence_type = html.escape(step["evidence_type"])
        finding = html.escape(step["finding"])
        learning_point = html.escape(step["learning_point"])

        st.markdown(
            f"""
            <div class="evidence-step">
                <div class="evidence-step-number">{index}</div>
                <div class="evidence-step-content">
                    <div class="evidence-resource">{resource}</div>
                    <div class="evidence-type">{evidence_type}</div>
                    <div class="evidence-finding"><strong>Finding:</strong> {finding}</div>
                    <div class="evidence-learning-point"><strong>Learning point:</strong> {learning_point}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

    render_api_bonus_summary(answers)


def render_api_bonus_summary(answers: dict[str, Any]) -> None:
    """Render the API bonus separately from the main evidence trail."""
    api_idea = answer_value(answers, "api-1")
    api_need = answer_value(answers, "api-2")

    if not api_idea and not api_need:
        return

    st.markdown("### Bonus API Integration Idea")

    if api_idea:
        st.markdown(f"**Idea:** {html.escape(api_idea)}")

    if api_need:
        st.markdown(f"**Needed data or lookup:** {html.escape(api_need)}")


# Example replacement call:
#
# inject_evidence_trail_css()
# render_evidence_trail_summary(st.session_state.answers)
