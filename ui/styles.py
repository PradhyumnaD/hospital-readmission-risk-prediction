from __future__ import annotations

import streamlit as st


def apply_global_styles() -> None:
    """Apply static presentation styles for the Streamlit interface."""

    st.markdown(
        """
        <style>
        :root {
            --hr-navy: #062C4C;
            --hr-navy-2: #0B3B63;
            --hr-teal: #0F8F8D;
            --hr-teal-dark: #08706F;
            --hr-blue: #2878D0;
            --hr-green: #148A5B;
            --hr-amber: #B7791F;
            --hr-red: #C53B3B;
            --hr-text: #10233F;
            --hr-muted: #607089;
            --hr-border: #DDE4EC;
            --hr-surface: #FFFFFF;
            --hr-bg: #F6F8FB;
            --hr-soft-teal: #E8F7F5;
            --hr-soft-blue: #EAF3FF;
            --hr-soft-amber: #FFF7E5;
            --hr-shadow: 0 8px 28px rgba(16, 35, 63, 0.07);
        }

        .stApp {
            background:
                radial-gradient(
                    circle at 88% 0%,
                    rgba(15, 143, 141, 0.06),
                    transparent 28rem
                ),
                var(--hr-bg);
        }

        .block-container {
            max-width: 1480px;
            padding-top: 2.25rem;
            padding-bottom: 3rem;
        }

        h1, h2, h3, h4 {
            color: var(--hr-text);
            letter-spacing: -0.02em;
        }

        p, li, label {
            color: var(--hr-text);
        }

        [data-testid="stCaptionContainer"] p {
            color: var(--hr-muted);
        }

        [data-testid="stSidebar"] {
            border-right: 1px solid rgba(255, 255, 255, 0.10);
        }

        [data-testid="stSidebar"] .block-container {
            padding-top: 1.45rem;
        }

        .hr-sidebar-brand {
            display: flex;
            align-items: center;
            gap: 0.8rem;
            margin: 0.15rem 0 1.6rem 0;
            padding: 0.2rem 0.2rem 0.9rem 0.2rem;
        }

        .hr-sidebar-logo {
            display: grid;
            place-items: center;
            width: 2.65rem;
            height: 2.65rem;
            border-radius: 0.85rem;
            background:
                linear-gradient(145deg, #19B6AE, #0F8F8D);
            box-shadow: 0 8px 22px rgba(15, 143, 141, 0.28);
            color: white;
            font-size: 1.35rem;
            font-weight: 800;
        }

        .hr-sidebar-title {
            color: #FFFFFF;
            font-size: 1.05rem;
            font-weight: 800;
            line-height: 1.15;
        }

        .hr-sidebar-subtitle {
            color: #AFC8DD;
            font-size: 0.74rem;
            margin-top: 0.18rem;
        }

        [data-testid="stSidebar"] div[role="radiogroup"] > label {
            border-radius: 0.65rem;
            padding: 0.56rem 0.65rem;
            margin-bottom: 0.15rem;
            transition: background-color 120ms ease;
        }

        [data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
            background: rgba(255, 255, 255, 0.08);
        }

        .hr-hero {
            position: relative;
            overflow: hidden;
            border: 1px solid #CFE0ED;
            border-radius: 1.15rem;
            padding: 1.65rem 1.8rem;
            margin-bottom: 1.35rem;
            background:
                linear-gradient(
                    110deg,
                    rgba(255,255,255,0.98) 0%,
                    rgba(243,250,252,0.98) 56%,
                    rgba(224,244,244,0.98) 100%
                );
            box-shadow: var(--hr-shadow);
        }

        .hr-hero::after {
            content: "";
            position: absolute;
            right: -4rem;
            top: -5rem;
            width: 15rem;
            height: 15rem;
            border-radius: 50%;
            background: rgba(15, 143, 141, 0.08);
        }

        .hr-hero-eyebrow {
            color: var(--hr-teal-dark);
            font-size: 0.75rem;
            font-weight: 800;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            margin-bottom: 0.55rem;
        }

        .hr-hero-row {
            display: flex;
            align-items: flex-start;
            gap: 1rem;
        }

        .hr-hero-icon {
            display: grid;
            place-items: center;
            flex: 0 0 auto;
            width: 3.25rem;
            height: 3.25rem;
            border-radius: 1rem;
            background: var(--hr-soft-teal);
            color: var(--hr-teal-dark);
            font-size: 1.55rem;
            border: 1px solid #CBEAE7;
        }

        .hr-hero-title {
            position: relative;
            z-index: 1;
            color: var(--hr-text);
            font-size: clamp(1.65rem, 2.6vw, 2.55rem);
            line-height: 1.12;
            font-weight: 850;
            margin: 0;
        }

        .hr-hero-subtitle {
            position: relative;
            z-index: 1;
            color: var(--hr-muted);
            max-width: 920px;
            font-size: 0.98rem;
            line-height: 1.6;
            margin-top: 0.55rem;
        }

        .hr-metric-card {
            min-height: 8.2rem;
            border: 1px solid var(--hr-border);
            border-radius: 1rem;
            padding: 1rem 1.1rem;
            background: var(--hr-surface);
            box-shadow: var(--hr-shadow);
            margin-bottom: 0.7rem;
        }

        .hr-metric-top {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 0.8rem;
        }

        .hr-metric-icon {
            display: grid;
            place-items: center;
            width: 2.35rem;
            height: 2.35rem;
            border-radius: 0.75rem;
            background: var(--hr-soft-teal);
            color: var(--hr-teal-dark);
            font-size: 1.08rem;
        }

        .hr-metric-label {
            color: var(--hr-muted);
            font-size: 0.78rem;
            font-weight: 700;
        }

        .hr-metric-value {
            color: var(--hr-text);
            font-size: 1.75rem;
            line-height: 1.15;
            font-weight: 850;
            margin-top: 0.65rem;
        }

        .hr-metric-note {
            color: var(--hr-muted);
            font-size: 0.74rem;
            margin-top: 0.35rem;
        }

        .hr-info-card {
            height: 100%;
            min-height: 13rem;
            border: 1px solid var(--hr-border);
            border-radius: 1rem;
            padding: 1.2rem 1.25rem;
            background: var(--hr-surface);
            box-shadow: var(--hr-shadow);
        }

        .hr-info-card-title {
            display: flex;
            align-items: center;
            gap: 0.55rem;
            color: var(--hr-text);
            font-size: 1rem;
            font-weight: 800;
            margin-bottom: 0.75rem;
        }

        .hr-info-card-icon {
            display: grid;
            place-items: center;
            width: 2.1rem;
            height: 2.1rem;
            border-radius: 0.7rem;
            background: var(--hr-soft-blue);
            color: var(--hr-blue);
            flex: 0 0 auto;
        }

        .hr-info-card-body {
            color: var(--hr-muted);
            font-size: 0.88rem;
            line-height: 1.62;
        }

        .hr-workflow {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 0.85rem;
            margin: 0.8rem 0 1.3rem 0;
        }

        .hr-workflow-step {
            border: 1px solid var(--hr-border);
            border-radius: 0.9rem;
            padding: 0.95rem 1rem;
            background: var(--hr-surface);
        }

        .hr-workflow-number {
            display: inline-grid;
            place-items: center;
            width: 1.9rem;
            height: 1.9rem;
            border-radius: 50%;
            color: white;
            background: var(--hr-teal);
            font-weight: 800;
            font-size: 0.82rem;
            margin-bottom: 0.55rem;
        }

        .hr-workflow-title {
            color: var(--hr-text);
            font-size: 0.88rem;
            font-weight: 800;
        }

        .hr-workflow-copy {
            color: var(--hr-muted);
            font-size: 0.76rem;
            line-height: 1.45;
            margin-top: 0.25rem;
        }

        .hr-section-title {
            color: var(--hr-text);
            font-size: 1.2rem;
            font-weight: 850;
            margin: 1.45rem 0 0.75rem 0;
        }

        div[data-testid="stMetric"] {
            border: 1px solid var(--hr-border);
            border-radius: 0.9rem;
            padding: 0.9rem 1rem;
            background: var(--hr-surface);
            box-shadow: 0 4px 16px rgba(16, 35, 63, 0.045);
        }

        div[data-testid="stForm"],
        div[data-testid="stDataFrame"],
        div[data-testid="stFileUploader"] {
            border-radius: 0.9rem;
        }

        div[role="radiogroup"][aria-label="Choose an input method"] {
            gap: 0.45rem;
        }

        div[role="radiogroup"][aria-label="Choose an input method"] > label {
            border: 1px solid var(--hr-border);
            border-radius: 999px;
            padding: 0.55rem 0.85rem;
            background: var(--hr-surface);
        }

        .stButton > button,
        .stDownloadButton > button {
            min-height: 2.55rem;
            font-weight: 750;
            border-width: 1px;
            transition:
                transform 120ms ease,
                box-shadow 120ms ease,
                background-color 120ms ease;
        }

        .stButton > button:hover,
        .stDownloadButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 7px 18px rgba(16, 35, 63, 0.10);
        }

        [data-testid="stAlert"] {
            border-radius: 0.85rem;
        }

        [data-testid="stExpander"] {
            border: 1px solid var(--hr-border);
            border-radius: 0.85rem;
            background: var(--hr-surface);
        }

        @media (max-width: 900px) {
            .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
            }

            .hr-workflow {
                grid-template-columns: 1fr;
            }

            .hr-hero {
                padding: 1.25rem;
            }

            .hr-hero-icon {
                width: 2.75rem;
                height: 2.75rem;
            }
        }

        .hr-threshold-card {
            border: 1px solid var(--hr-border);
            border-radius: 1rem;
            padding: 1.2rem;
            background: var(--hr-surface);
            box-shadow: var(--hr-shadow);
            min-height: 18rem;
        }

        .hr-threshold-teal {
            border-top: 4px solid var(--hr-teal);
        }

        .hr-threshold-blue {
            border-top: 4px solid var(--hr-blue);
        }

        .hr-threshold-heading {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 1rem;
            margin-bottom: 1rem;
        }

        .hr-threshold-title {
            color: var(--hr-muted);
            font-size: 0.82rem;
            font-weight: 800;
        }

        .hr-threshold-value {
            color: var(--hr-text);
            font-size: 2rem;
            font-weight: 850;
            margin-top: 0.2rem;
        }

        .hr-threshold-badge {
            padding: 0.28rem 0.55rem;
            border-radius: 999px;
            background: var(--hr-soft-teal);
            color: var(--hr-teal-dark);
            font-size: 0.7rem;
            font-weight: 800;
        }

        .hr-threshold-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 0.65rem;
        }

        .hr-threshold-grid > div {
            border: 1px solid var(--hr-border);
            border-radius: 0.7rem;
            padding: 0.7rem 0.75rem;
            background: #FBFCFE;
        }

        .hr-threshold-grid span {
            display: block;
            color: var(--hr-muted);
            font-size: 0.68rem;
            margin-bottom: 0.2rem;
        }

        .hr-threshold-grid strong {
            color: var(--hr-text);
            font-size: 0.9rem;
        }

        .hr-message {
            display: flex;
            gap: 0.8rem;
            align-items: flex-start;
            border-radius: 0.9rem;
            padding: 0.95rem 1rem;
            margin: 0.65rem 0;
            border: 1px solid var(--hr-border);
        }

        .hr-message-blue {
            background: var(--hr-soft-blue);
        }

        .hr-message-teal {
            background: var(--hr-soft-teal);
        }

        .hr-message-amber {
            background: var(--hr-soft-amber);
        }

        .hr-message-icon {
            display: grid;
            place-items: center;
            width: 2rem;
            height: 2rem;
            border-radius: 0.65rem;
            background: white;
            color: var(--hr-blue);
            font-weight: 850;
            flex: 0 0 auto;
        }

        .hr-message-title {
            color: var(--hr-text);
            font-weight: 850;
            font-size: 0.88rem;
        }

        .hr-message-copy {
            color: var(--hr-muted);
            font-size: 0.8rem;
            line-height: 1.5;
            margin-top: 0.18rem;
        }

        .hr-chart-shell {
            border: 1px solid var(--hr-border);
            border-radius: 1rem;
            padding: 1rem 1rem 0.4rem 1rem;
            background: var(--hr-surface);
            box-shadow: var(--hr-shadow);
        }

        .hr-table-intro {
            color: var(--hr-muted);
            font-size: 0.82rem;
            line-height: 1.55;
            margin-bottom: 0.65rem;
        }

        .hr-figure-shell {
            border: 1px solid var(--hr-border);
            border-radius: 1rem;
            padding: 1rem;
            background: var(--hr-surface);
            box-shadow: var(--hr-shadow);
        }

        @media (max-width: 900px) {
            .hr-threshold-grid {
                grid-template-columns: 1fr;
            }
        }


        /* ---------------------------------------------------------
           Sidebar contrast and navigation-state fixes
           --------------------------------------------------------- */
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] label *,
        [data-testid="stSidebar"] .stMarkdown p,
        [data-testid="stSidebar"] .stMarkdown span {
            color: #EAF4FB !important;
        }

        [data-testid="stSidebar"] div[role="radiogroup"] > label {
            background: transparent;
            border: 1px solid transparent;
            border-radius: 0.70rem;
            padding: 0.62rem 0.70rem;
            margin-bottom: 0.20rem;
        }

        [data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
            background: rgba(255, 255, 255, 0.09);
            border-color: rgba(255, 255, 255, 0.08);
        }

        [data-testid="stSidebar"]
        div[role="radiogroup"] > label:has(input:checked) {
            background: rgba(35, 196, 183, 0.20);
            border-color: rgba(35, 196, 183, 0.38);
        }

        [data-testid="stSidebar"]
        div[role="radiogroup"] > label:has(input:checked) * {
            color: #FFFFFF !important;
            font-weight: 750;
        }

        [data-testid="stSidebar"] [data-testid="stAlert"] {
            background: rgba(15, 143, 141, 0.30);
            border-color: rgba(35, 196, 183, 0.35);
        }

        [data-testid="stSidebar"] [data-testid="stAlert"] * {
            color: #F0FFFD !important;
        }

        [data-testid="stSidebar"]
        [data-testid="stCaptionContainer"] p,
        [data-testid="stSidebar"]
        [data-testid="stCaptionContainer"] span {
            color: #BFD4E5 !important;
        }

        [data-testid="stSidebar"] hr {
            border-color: rgba(255, 255, 255, 0.14);
        }


        /* ---------------------------------------------------------
           Prediction-result presentation
           --------------------------------------------------------- */
        .hr-screening-card {
            height: 100%;
            min-height: 10.2rem;
            border: 1px solid var(--hr-border);
            border-radius: 1rem;
            padding: 1rem 1.05rem;
            background: var(--hr-surface);
            box-shadow: var(--hr-shadow);
        }

        .hr-screening-card-top {
            display: flex;
            align-items: center;
            gap: 0.55rem;
        }

        .hr-screening-card-icon {
            display: grid;
            place-items: center;
            width: 2.15rem;
            height: 2.15rem;
            border-radius: 0.72rem;
            font-weight: 850;
        }

        .hr-screening-card-label {
            color: var(--hr-muted);
            font-size: 0.76rem;
            font-weight: 800;
        }

        .hr-screening-card-result {
            color: var(--hr-text);
            font-size: 1.12rem;
            line-height: 1.35;
            font-weight: 850;
            margin-top: 0.85rem;
        }

        .hr-screening-card-note {
            color: var(--hr-muted);
            font-size: 0.73rem;
            line-height: 1.45;
            margin-top: 0.45rem;
        }

        .hr-screening-green {
            border-top: 4px solid var(--hr-green);
        }

        .hr-screening-green .hr-screening-card-icon {
            background: #E8F6EF;
            color: var(--hr-green);
        }

        .hr-screening-amber {
            border-top: 4px solid var(--hr-amber);
        }

        .hr-screening-amber .hr-screening-card-icon {
            background: var(--hr-soft-amber);
            color: var(--hr-amber);
        }

        .hr-screening-teal {
            border-top: 4px solid var(--hr-teal);
        }

        .hr-screening-teal .hr-screening-card-icon {
            background: var(--hr-soft-teal);
            color: var(--hr-teal-dark);
        }

        .hr-screening-blue {
            border-top: 4px solid var(--hr-blue);
        }

        .hr-screening-blue .hr-screening-card-icon {
            background: var(--hr-soft-blue);
            color: var(--hr-blue);
        }

        .hr-probability-card {
            border: 1px solid var(--hr-border);
            border-radius: 1rem;
            padding: 1.15rem 1.2rem 1.05rem 1.2rem;
            margin: 1rem 0 1.2rem 0;
            background: var(--hr-surface);
            box-shadow: var(--hr-shadow);
        }

        .hr-probability-heading {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 1rem;
        }

        .hr-probability-label {
            color: var(--hr-muted);
            font-size: 0.76rem;
            font-weight: 800;
        }

        .hr-probability-value {
            color: var(--hr-text);
            font-size: 2rem;
            line-height: 1.1;
            font-weight: 900;
            margin-top: 0.25rem;
        }

        .hr-probability-note {
            color: var(--hr-muted);
            font-size: 0.72rem;
            padding-top: 0.25rem;
        }

        .hr-probability-scale {
            position: relative;
            height: 1rem;
            border-radius: 999px;
            margin: 2.55rem 0 2.65rem 0;
            background:
                linear-gradient(
                    90deg,
                    #DCE8F7 0%,
                    #DCE8F7 45%,
                    #FFF0C9 45%,
                    #FFF0C9 50%,
                    #DDF3EC 50%,
                    #DDF3EC 100%
                );
            overflow: visible;
        }

        .hr-probability-fill {
            position: absolute;
            inset: 0 auto 0 0;
            border-radius: 999px;
            background:
                linear-gradient(90deg, #2878D0, #0F8F8D);
            opacity: 0.88;
        }

        .hr-cutoff-line {
            position: absolute;
            top: -0.45rem;
            width: 2px;
            height: 1.9rem;
            transform: translateX(-1px);
        }

        .hr-cutoff-line span {
            position: absolute;
            top: 2.05rem;
            left: 50%;
            transform: translateX(-50%);
            white-space: nowrap;
            color: var(--hr-muted);
            font-size: 0.67rem;
            font-weight: 750;
        }

        .hr-cutoff-additional {
            background: var(--hr-blue);
        }

        .hr-cutoff-standard {
            background: var(--hr-teal);
        }

        .hr-probability-marker {
            position: absolute;
            top: 50%;
            width: 1.15rem;
            height: 1.15rem;
            border: 3px solid white;
            border-radius: 50%;
            background: var(--hr-text);
            box-shadow: 0 3px 10px rgba(16, 35, 63, 0.24);
            transform: translate(-50%, -50%);
        }

        .hr-probability-marker span {
            position: absolute;
            bottom: 1.45rem;
            left: 50%;
            transform: translateX(-50%);
            white-space: nowrap;
            border-radius: 0.45rem;
            padding: 0.25rem 0.42rem;
            background: var(--hr-text);
            color: white;
            font-size: 0.68rem;
            font-weight: 800;
        }

        .hr-probability-legend {
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            color: var(--hr-muted);
            font-size: 0.7rem;
        }

        .hr-legend-dot {
            display: inline-block;
            width: 0.52rem;
            height: 0.52rem;
            border-radius: 50%;
            margin-right: 0.32rem;
        }

        .hr-dot-blue {
            background: var(--hr-blue);
        }

        .hr-dot-teal {
            background: var(--hr-teal);
        }

        .hr-factor-panel {
            height: 100%;
            min-height: 23rem;
            border: 1px solid var(--hr-border);
            border-radius: 1rem;
            padding: 1rem 1.05rem;
            background: var(--hr-surface);
            box-shadow: var(--hr-shadow);
        }

        .hr-factor-increasing {
            border-top: 4px solid var(--hr-amber);
        }

        .hr-factor-reducing {
            border-top: 4px solid var(--hr-green);
        }

        .hr-factor-panel-heading {
            display: flex;
            align-items: center;
            gap: 0.55rem;
            color: var(--hr-text);
            font-size: 0.95rem;
            font-weight: 850;
            margin-bottom: 0.9rem;
        }

        .hr-factor-panel-icon {
            display: grid;
            place-items: center;
            width: 2rem;
            height: 2rem;
            border-radius: 0.65rem;
            background: #F5F7FA;
            font-weight: 900;
        }

        .hr-factor-increasing .hr-factor-panel-icon {
            color: var(--hr-amber);
            background: var(--hr-soft-amber);
        }

        .hr-factor-reducing .hr-factor-panel-icon {
            color: var(--hr-green);
            background: #E8F6EF;
        }

        .hr-factor-list {
            display: grid;
            gap: 0.58rem;
        }

        .hr-factor-row {
            display: grid;
            grid-template-columns: 1.8rem 1fr;
            gap: 0.65rem;
            align-items: center;
            border: 1px solid var(--hr-border);
            border-radius: 0.72rem;
            padding: 0.65rem 0.7rem;
            background: #FBFCFE;
        }

        .hr-factor-rank {
            display: grid;
            place-items: center;
            width: 1.65rem;
            height: 1.65rem;
            border-radius: 50%;
            background: #EEF3F8;
            color: var(--hr-text);
            font-size: 0.7rem;
            font-weight: 850;
        }

        .hr-factor-name {
            color: var(--hr-text);
            font-size: 0.79rem;
            font-weight: 800;
        }

        .hr-factor-value {
            color: var(--hr-muted);
            font-size: 0.72rem;
            margin-top: 0.12rem;
        }

        .hr-factor-empty {
            color: var(--hr-muted);
            font-size: 0.8rem;
            padding: 0.8rem;
        }

        @media (max-width: 900px) {
            .hr-probability-heading {
                display: block;
            }

            .hr-probability-note {
                margin-top: 0.4rem;
            }

            .hr-factor-panel {
                min-height: auto;
            }
        }

        </style>
        """,
        unsafe_allow_html=True,
    )
