from __future__ import annotations

from html import escape

import streamlit as st


def render_page_hero(
    title: str,
    subtitle: str,
    *,
    eyebrow: str = "ASDS 6306 Capstone Project",
    icon: str = "✚",
) -> None:
    """Render a professional page-level hero block."""

    st.markdown(
        f"""
        <section class="hr-hero">
            <div class="hr-hero-eyebrow">{escape(eyebrow)}</div>
            <div class="hr-hero-row">
                <div class="hr-hero-icon">{escape(icon)}</div>
                <div>
                    <h1 class="hr-hero-title">{escape(title)}</h1>
                    <div class="hr-hero-subtitle">
                        {escape(subtitle)}
                    </div>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_metric_card(
    label: str,
    value: str,
    *,
    note: str = "",
    icon: str = "●",
) -> None:
    """Render a compact summary metric card."""

    note_html = (
        f'<div class="hr-metric-note">{escape(note)}</div>'
        if note
        else ""
    )

    st.markdown(
        f"""
        <div class="hr-metric-card">
            <div class="hr-metric-top">
                <div class="hr-metric-label">{escape(label)}</div>
                <div class="hr-metric-icon">{escape(icon)}</div>
            </div>
            <div class="hr-metric-value">{escape(value)}</div>
            {note_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_info_card(
    title: str,
    body: str,
    *,
    icon: str = "i",
) -> None:
    """Render a reusable information card."""

    st.markdown(
        f"""
        <div class="hr-info-card">
            <div class="hr-info-card-title">
                <span class="hr-info-card-icon">{escape(icon)}</span>
                <span>{escape(title)}</span>
            </div>
            <div class="hr-info-card-body">{escape(body)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_three_step_workflow() -> None:
    """Render the three-step application workflow."""

    st.markdown(
        """
        <div class="hr-workflow">
            <div class="hr-workflow-step">
                <span class="hr-workflow-number">1</span>
                <div class="hr-workflow-title">Provide encounter data</div>
                <div class="hr-workflow-copy">
                    Enter one de-identified record, upload multiple rows,
                    or load a synthetic demonstration record.
                </div>
            </div>
            <div class="hr-workflow-step">
                <span class="hr-workflow-number">2</span>
                <div class="hr-workflow-title">Estimate readmission risk</div>
                <div class="hr-workflow-copy">
                    The finalized Tuned XGBoost pipeline calculates the
                    estimated probability of readmission within 30 days.
                </div>
            </div>
            <div class="hr-workflow-step">
                <span class="hr-workflow-number">3</span>
                <div class="hr-workflow-title">Review contributing factors</div>
                <div class="hr-workflow-copy">
                    Compare both screening cutoffs and review the strongest
                    factors increasing or reducing the model estimate.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_threshold_card(
    title: str,
    threshold: str,
    *,
    recall: str,
    precision: str,
    specificity: str,
    caught: str,
    missed: str,
    false_positives: str,
    tone: str = "teal",
) -> None:
    """Render one final operating-point comparison card."""

    safe_tone = tone if tone in {"teal", "blue"} else "teal"

    st.markdown(
        f"""
        <div class="hr-threshold-card hr-threshold-{safe_tone}">
            <div class="hr-threshold-heading">
                <div>
                    <div class="hr-threshold-title">{escape(title)}</div>
                    <div class="hr-threshold-value">{escape(threshold)}</div>
                </div>
                <div class="hr-threshold-badge">Final</div>
            </div>
            <div class="hr-threshold-grid">
                <div><span>Recall</span><strong>{escape(recall)}</strong></div>
                <div><span>Precision</span><strong>{escape(precision)}</strong></div>
                <div><span>Specificity</span><strong>{escape(specificity)}</strong></div>
                <div><span>Readmissions caught</span><strong>{escape(caught)}</strong></div>
                <div><span>Readmissions missed</span><strong>{escape(missed)}</strong></div>
                <div><span>False-positive alerts</span><strong>{escape(false_positives)}</strong></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_key_message(
    title: str,
    message: str,
    *,
    icon: str = "i",
    tone: str = "blue",
) -> None:
    """Render a reusable highlighted message panel."""

    safe_tone = tone if tone in {"blue", "teal", "amber"} else "blue"

    st.markdown(
        f"""
        <div class="hr-message hr-message-{safe_tone}">
            <div class="hr-message-icon">{escape(icon)}</div>
            <div>
                <div class="hr-message-title">{escape(title)}</div>
                <div class="hr-message-copy">{escape(message)}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
