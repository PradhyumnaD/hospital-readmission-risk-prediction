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


def render_screening_status_card(
    label: str,
    result: str,
    *,
    note: str,
    tone: str,
    icon: str,
) -> None:
    """Render one user-friendly prediction status card."""

    safe_tone = (
        tone
        if tone in {"teal", "green", "amber", "blue"}
        else "blue"
    )

    st.markdown(
        f"""
        <div class="hr-screening-card hr-screening-{safe_tone}">
            <div class="hr-screening-card-top">
                <div class="hr-screening-card-icon">
                    {escape(icon)}
                </div>
                <div class="hr-screening-card-label">
                    {escape(label)}
                </div>
            </div>
            <div class="hr-screening-card-result">
                {escape(result)}
            </div>
            <div class="hr-screening-card-note">
                {escape(note)}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_probability_scale(
    probability_percentage: float,
    *,
    additional_cutoff: float = 45.0,
    standard_cutoff: float = 50.0,
) -> None:
    """Render an estimated-risk bar with both validated cutoffs."""

    probability = max(0.0, min(float(probability_percentage), 100.0))
    additional = max(0.0, min(float(additional_cutoff), 100.0))
    standard = max(0.0, min(float(standard_cutoff), 100.0))

    html = (
        '<div class="hr-probability-card">'
        '<div class="hr-probability-heading">'
        '<div>'
        '<div class="hr-probability-label">'
        'Estimated 30-Day Readmission Risk'
        '</div>'
        f'<div class="hr-probability-value">{probability:.2f}%</div>'
        '</div>'
        '<div class="hr-probability-note">'
        'Model-estimated probability'
        '</div>'
        '</div>'
        '<div class="hr-probability-scale">'
        f'<div class="hr-probability-fill" '
        f'style="width:{probability:.4f}%;"></div>'
        f'<div class="hr-cutoff-line hr-cutoff-additional" '
        f'style="left:{additional:.4f}%;">'
        '<span>45%</span>'
        '</div>'
        f'<div class="hr-cutoff-line hr-cutoff-standard" '
        f'style="left:{standard:.4f}%;">'
        '<span>50%</span>'
        '</div>'
        f'<div class="hr-probability-marker" '
        f'style="left:{probability:.4f}%;">'
        f'<span>{probability:.2f}%</span>'
        '</div>'
        '</div>'
        '<div class="hr-probability-legend">'
        '<span>'
        '<i class="hr-legend-dot hr-dot-blue"></i>'
        'Additional screening cutoff'
        '</span>'
        '<span>'
        '<i class="hr-legend-dot hr-dot-teal"></i>'
        'Standard review cutoff'
        '</span>'
        '</div>'
        '</div>'
    )

    st.markdown(html, unsafe_allow_html=True)


def render_factor_panel(
    title: str,
    factors: list[tuple[str, str]],
    *,
    direction: str,
) -> None:
    """Render increasing or reducing record-level factors."""

    safe_direction = (
        direction
        if direction in {"increasing", "reducing"}
        else "increasing"
    )

    if factors:
        row_parts = []
        for index, (feature, value) in enumerate(factors, start=1):
            row_parts.append(
                '<div class="hr-factor-row">'
                f'<div class="hr-factor-rank">{index}</div>'
                '<div>'
                f'<div class="hr-factor-name">{escape(str(feature))}</div>'
                f'<div class="hr-factor-value">{escape(str(value))}</div>'
                '</div>'
                '</div>'
            )
        rows = "".join(row_parts)
    else:
        rows = (
            '<div class="hr-factor-empty">'
            'No meaningful factors were identified.'
            '</div>'
        )

    icon = "↗" if safe_direction == "increasing" else "↘"

    html = (
        f'<div class="hr-factor-panel hr-factor-{safe_direction}">'
        '<div class="hr-factor-panel-heading">'
        f'<span class="hr-factor-panel-icon">{icon}</span>'
        f'<span>{escape(title)}</span>'
        '</div>'
        f'<div class="hr-factor-list">{rows}</div>'
        '</div>'
    )

    st.markdown(html, unsafe_allow_html=True)

