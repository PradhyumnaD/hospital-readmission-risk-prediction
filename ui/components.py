from __future__ import annotations

from base64 import b64encode
from html import escape

import streamlit as st




def _overview_icon_svg(icon_name: str) -> str:
    """Return a compact SVG icon for the professional Overview page."""

    icons = {
        "dataset": (
            '<svg viewBox="0 0 48 48" aria-hidden="true">'
            '<ellipse cx="24" cy="10" rx="13" ry="5"></ellipse>'
            '<path d="M11 10v10c0 2.8 5.8 5 13 5s13-2.2 13-5V10"></path>'
            '<path d="M11 20v10c0 2.8 5.8 5 13 5s13-2.2 13-5V20"></path>'
            '<path d="M11 30v8c0 2.8 5.8 5 13 5s13-2.2 13-5v-8"></path>'
            '</svg>'
        ),
        "model": (
            '<svg viewBox="0 0 48 48" aria-hidden="true">'
            '<rect x="14" y="14" width="20" height="20" rx="5"></rect>'
            '<path d="M19 4v7M29 4v7M19 37v7M29 37v7"></path>'
            '<path d="M4 19h7M4 29h7M37 19h7M37 29h7"></path>'
            '<circle cx="24" cy="24" r="5"></circle>'
            '<path d="M24 19v10M19 24h10"></path>'
            '</svg>'
        ),
        "shap": (
            '<svg viewBox="0 0 48 48" aria-hidden="true">'
            '<path d="M24 8c-4.4-5-12.5-1.8-11.6 5.3C6.2 14.5 5.7 23 12 25.3'
            'c-3.7 5.3 2.3 12.5 8.1 9.2 1 6.7 8.7 7.2 11.4 1.1'
            ' 6.4 2.2 11.1-4.8 7.5-10.3 6-3.3 4.4-11.8-2.2-12'
            'C37.3 6.1 29.1 3.1 24 8z"></path>'
            '<path d="M24 8v32M17 14c4 1.2 5.8 4.1 7 7M31 14c-4 1.2-5.8 4.1-7 7'
            'M14 26c4.6-.2 7.6 1.7 10 5M34 26c-4.6-.2-7.6 1.7-10 5"></path>'
            '</svg>'
        ),
        "validation": (
            '<svg viewBox="0 0 48 48" aria-hidden="true">'
            '<path d="M24 5l15 7v10c0 10-6.3 16.8-15 21-8.7-4.2-15-11-15-21V12z"></path>'
            '<path d="M16.5 24.5l5 5 10.5-11"></path>'
            '</svg>'
        ),
        "data": (
            '<svg viewBox="0 0 48 48" aria-hidden="true">'
            '<ellipse cx="24" cy="10" rx="13" ry="5"></ellipse>'
            '<path d="M11 10v10c0 2.8 5.8 5 13 5s13-2.2 13-5V10"></path>'
            '<path d="M11 20v10c0 2.8 5.8 5 13 5s13-2.2 13-5V20"></path>'
            '<path d="M11 30v8c0 2.8 5.8 5 13 5s13-2.2 13-5v-8"></path>'
            '</svg>'
        ),
        "split": (
            '<svg viewBox="0 0 48 48" aria-hidden="true">'
            '<circle cx="14" cy="14" r="5"></circle>'
            '<circle cx="34" cy="14" r="5"></circle>'
            '<circle cx="14" cy="34" r="5"></circle>'
            '<circle cx="34" cy="34" r="5"></circle>'
            '<path d="M19 14h10M14 19v10M34 19v10M19 34h10"></path>'
            '</svg>'
        ),
        "development": (
            '<svg viewBox="0 0 48 48" aria-hidden="true">'
            '<circle cx="24" cy="24" r="8"></circle>'
            '<path d="M24 5v6M24 37v6M5 24h6M37 24h6'
            'M10.6 10.6l4.3 4.3M33.1 33.1l4.3 4.3'
            'M37.4 10.6l-4.3 4.3M14.9 33.1l-4.3 4.3"></path>'
            '<circle cx="24" cy="24" r="16"></circle>'
            '</svg>'
        ),
        "threshold": (
            '<svg viewBox="0 0 48 48" aria-hidden="true">'
            '<path d="M24 7v34M11 14h26M8 37h32"></path>'
            '<path d="M15 14l-7 14h14zM33 14l-7 14h14z"></path>'
            '</svg>'
        ),
        "prediction": (
            '<svg viewBox="0 0 48 48" aria-hidden="true">'
            '<path d="M24 5l15 7v10c0 10-6.3 16.8-15 21-8.7-4.2-15-11-15-21V12z"></path>'
            '<path d="M16 26h5l3-8 4 13 3-5h5"></path>'
            '</svg>'
        ),
    }

    return icons.get(icon_name, icons["validation"])


def render_overview_hero(
    validation_text: str = "108 / 108 Validation Checks",
) -> None:
    """Render the large professional project Overview hero."""

    hospital_svg = """
    <svg xmlns="http://www.w3.org/2000/svg"
         viewBox="0 0 760 430"
         role="img"
         aria-label="Modern hospital and analytics illustration">
        <defs>
            <linearGradient id="sky" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0%" stop-color="#F8FCFE"/>
                <stop offset="58%" stop-color="#EDF8FA"/>
                <stop offset="100%" stop-color="#D9F0F3"/>
            </linearGradient>
            <linearGradient id="glass" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0%" stop-color="#73C8D3"/>
                <stop offset="100%" stop-color="#1E6FA3"/>
            </linearGradient>
            <linearGradient id="accent" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0%" stop-color="#18A7A2"/>
                <stop offset="100%" stop-color="#08706F"/>
            </linearGradient>
            <filter id="shadow" x="-25%" y="-25%" width="150%" height="150%">
                <feDropShadow dx="0" dy="12" stdDeviation="11"
                              flood-color="#0B3556" flood-opacity="0.16"/>
            </filter>
        </defs>

        <rect width="760" height="430" rx="34" fill="url(#sky)"/>
        <circle cx="625" cy="70" r="94" fill="#CBEAEC" opacity="0.55"/>
        <circle cx="625" cy="70" r="64" fill="none"
                stroke="#89CED0" stroke-width="2" opacity="0.65"/>
        <path d="M672 46h-25V21h-34v25h-25v34h25v25h34V80h25z"
              fill="#0F8F8D" opacity="0.14"/>

        <g opacity="0.55">
            <rect x="88" y="202" width="52" height="93" rx="4" fill="#D6E9F1"/>
            <rect x="148" y="176" width="64" height="119" rx="4" fill="#D6E9F1"/>
            <rect x="218" y="216" width="48" height="79" rx="4" fill="#D6E9F1"/>
            <g fill="#B8D8E4">
                <rect x="101" y="217" width="11" height="13" rx="2"/>
                <rect x="119" y="217" width="11" height="13" rx="2"/>
                <rect x="101" y="238" width="11" height="13" rx="2"/>
                <rect x="119" y="238" width="11" height="13" rx="2"/>
                <rect x="164" y="192" width="12" height="13" rx="2"/>
                <rect x="184" y="192" width="12" height="13" rx="2"/>
                <rect x="164" y="215" width="12" height="13" rx="2"/>
                <rect x="184" y="215" width="12" height="13" rx="2"/>
            </g>
        </g>

        <path d="M0 333C130 278 242 318 355 274
                 C485 224 610 244 760 185V430H0z"
              fill="#D8F0F1"/>

        <g filter="url(#shadow)">
            <rect x="248" y="154" width="126" height="190" rx="8"
                  fill="#F8FCFE" stroke="#B8D2E0" stroke-width="2"/>
            <rect x="562" y="154" width="126" height="190" rx="8"
                  fill="#F8FCFE" stroke="#B8D2E0" stroke-width="2"/>
            <rect x="350" y="86" width="236" height="258" rx="10"
                  fill="#FFFFFF" stroke="#AFCBDA" stroke-width="2"/>

            <rect x="405" y="104" width="126" height="74" rx="9"
                  fill="url(#glass)"/>
            <rect x="450" y="115" width="36" height="52" rx="5"
                  fill="#FFFFFF"/>
            <rect x="438" y="128" width="60" height="25" rx="5"
                  fill="#FFFFFF"/>

            <g fill="url(#glass)">
                <rect x="270" y="183" width="41" height="34" rx="4"/>
                <rect x="270" y="232" width="41" height="34" rx="4"/>
                <rect x="270" y="281" width="41" height="34" rx="4"/>
                <rect x="625" y="183" width="41" height="34" rx="4"/>
                <rect x="625" y="232" width="41" height="34" rx="4"/>
                <rect x="625" y="281" width="41" height="34" rx="4"/>
                <rect x="383" y="198" width="45" height="37" rx="4"/>
                <rect x="450" y="198" width="45" height="37" rx="4"/>
                <rect x="517" y="198" width="45" height="37" rx="4"/>
                <rect x="383" y="250" width="45" height="37" rx="4"/>
                <rect x="517" y="250" width="45" height="37" rx="4"/>
            </g>

            <rect x="431" y="250" width="75" height="94" rx="5"
                  fill="#164F74"/>
            <rect x="466" y="250" width="6" height="94" fill="#CDE5EF"/>
            <rect x="394" y="238" width="148" height="16" rx="8"
                  fill="url(#accent)"/>
            <rect x="326" y="326" width="282" height="18" rx="9"
                  fill="#C8DDE7"/>
        </g>

        <g filter="url(#shadow)">
            <rect x="82" y="70" width="150" height="126" rx="22"
                  fill="#FFFFFF" stroke="#C5DDE8" stroke-width="2"/>
            <path d="M110 155l28-27 23 17 39-42"
                  fill="none" stroke="#0F8F8D" stroke-width="6"
                  stroke-linecap="round" stroke-linejoin="round"/>
            <circle cx="110" cy="155" r="5" fill="#2878D0"/>
            <circle cx="138" cy="128" r="5" fill="#2878D0"/>
            <circle cx="161" cy="145" r="5" fill="#2878D0"/>
            <circle cx="200" cy="103" r="5" fill="#2878D0"/>
            <path d="M168 160l18 8 18-8v-20l-18-8-18 8z"
                  fill="#E8F7F5" stroke="#0F8F8D" stroke-width="3"/>
            <path d="M180 150h12M186 144v12"
                  stroke="#0F8F8D" stroke-width="3"
                  stroke-linecap="round"/>
        </g>

        <g>
            <circle cx="205" cy="330" r="31" fill="#62ADA4"/>
            <rect x="199" y="330" width="12" height="48" rx="6" fill="#267C72"/>
            <circle cx="705" cy="329" r="30" fill="#62ADA4"/>
            <rect x="699" y="329" width="12" height="49" rx="6" fill="#267C72"/>
            <circle cx="95" cy="348" r="24" fill="#7ABBB1"/>
            <rect x="90" y="348" width="10" height="37" rx="5" fill="#337F76"/>
        </g>

        <path d="M62 385H708" stroke="#9ECBD0" stroke-width="4"
              stroke-linecap="round"/>
    </svg>
    """

    encoded_svg = b64encode(hospital_svg.encode("utf-8")).decode("ascii")
    safe_validation_text = escape(validation_text)

    html = (
        '<section class="hr-overview-hero">'
        '<div class="hr-overview-hero-copy">'
        '<div class="hr-overview-eyebrow">ASDS 6306 Capstone Project</div>'
        '<h1 class="hr-overview-title">'
        'AI-Powered Hospital<br>Readmission Risk Prediction'
        '</h1>'
        '<div class="hr-overview-subtitle">'
        '<span>Machine Learning</span><i></i>'
        '<span>Explainable AI</span><i></i>'
        '<span>Clinical Decision Support</span>'
        '</div>'
        '<p class="hr-overview-description">'
        'A finalized academic decision-support prototype developed from '
        '99,343 hospital encounters to estimate the probability of 30-day '
        'readmission and identify encounters that may benefit from '
        'additional post-discharge review.'
        '</p>'
        '<div class="hr-overview-badges">'
        '<span>Tuned XGBoost</span>'
        '<span>Two Decision Thresholds</span>'
        '<span>SHAP Explanations</span>'
        f'<span>{safe_validation_text}</span>'
        '</div>'
        '</div>'
        '<div class="hr-overview-visual" aria-hidden="true">'
        f'<img class="hr-overview-hospital-svg" '
        f'src="data:image/svg+xml;base64,{encoded_svg}" '
        'alt="Modern hospital and analytics illustration">'
        '</div>'
        '</section>'
    )

    st.markdown(html, unsafe_allow_html=True)


def render_overview_fact_card(
    label: str,
    value: str,
    note: str,
    *,
    icon: str,
    details: list[str] | tuple[str, ...] | None = None,
) -> None:
    """Render a detailed project fact card."""

    detail_items = details or []
    details_html = "".join(
        f'<li>{escape(str(item))}</li>'
        for item in detail_items
    )

    html = (
        '<article class="hr-overview-fact-card">'
        '<div class="hr-overview-fact-icon">'
        f'{_overview_icon_svg(icon)}'
        '</div>'
        '<div class="hr-overview-fact-content">'
        f'<div class="hr-overview-fact-label">{escape(label)}</div>'
        f'<div class="hr-overview-fact-value">{escape(value)}</div>'
        f'<div class="hr-overview-fact-note">{escape(note)}</div>'
        f'<ul class="hr-overview-fact-details">{details_html}</ul>'
        '</div>'
        '</article>'
    )

    st.markdown(html, unsafe_allow_html=True)


def render_project_pipeline() -> None:
    """Render the horizontal five-stage project pipeline."""

    stages = [
        (
            "1",
            "data",
            "Data Preparation",
            "Audit, clean, group, and encode the hospital encounter data.",
        ),
        (
            "2",
            "split",
            "Patient-Level Splitting",
            "Keep each patient in one partition to prevent data leakage.",
        ),
        (
            "3",
            "development",
            "Model Development",
            "Compare candidates and tune the finalized XGBoost model.",
        ),
        (
            "4",
            "threshold",
            "Dual Thresholds",
            "Use 0.50 for standard review and 0.45 for added screening.",
        ),
        (
            "5",
            "prediction",
            "Risk Prediction & Explanation",
            "Estimate risk and provide record-level SHAP explanations.",
        ),
    ]

    stage_html = []
    for number, icon, title, copy in stages:
        stage_html.append(
            '<div class="hr-project-pipeline-step">'
            f'<div class="hr-project-pipeline-number">{number}</div>'
            '<div class="hr-project-pipeline-icon">'
            f'{_overview_icon_svg(icon)}'
            '</div>'
            f'<div class="hr-project-pipeline-step-title">{escape(title)}</div>'
            f'<div class="hr-project-pipeline-step-copy">{escape(copy)}</div>'
            '</div>'
        )

    html = (
        '<section class="hr-project-pipeline">'
        '<div class="hr-project-pipeline-heading">'
        '<div>'
        '<div class="hr-project-pipeline-title">Project Pipeline</div>'
        '<div class="hr-project-pipeline-subtitle">'
        'Finalized leakage-safe workflow used to build and deploy the '
        'readmission-risk application.'
        '</div>'
        '</div>'
        '<div class="hr-project-pipeline-badge">Leakage-Safe Workflow</div>'
        '</div>'
        '<div class="hr-project-pipeline-grid">'
        f'{"".join(stage_html)}'
        '</div>'
        '</section>'
    )

    st.markdown(html, unsafe_allow_html=True)

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

