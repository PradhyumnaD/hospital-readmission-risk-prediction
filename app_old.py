from io import BytesIO
from pathlib import Path

import pandas as pd
import streamlit as st

from prediction_service import predict_readmission_batch

# ---------------------------------------------------------
# Project file paths
# ---------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent

PATIENT_TEMPLATE_PATH = (
    PROJECT_ROOT
    / "outputs"
    / "patient_input_template.csv"
)

SAMPLE_PATIENT_PATH = (
    PROJECT_ROOT
    / "outputs"
    / "sample_patient_input.csv"
)

DATASET_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "diabetic_modeling_data_final.csv"
)

MODEL_COMPARISON_PATH = (
    PROJECT_ROOT
    / "outputs"
    / "metrics"
    / "dynamic_all_model_comparison_summary.csv"
)

FIGURES_DIR = (
    PROJECT_ROOT
    / "outputs"
    / "figures"
)

# ---------------------------------------------------------
# Safe saved figures from Notebooks 4–6B
# ---------------------------------------------------------
SAFE_FIGURES = {
    "Overall Model Comparison Summary": {
        "filename": "dynamic_all_model_comparison_summary.png",
        "category": "Overall Comparison",
        "description": (
            "Summary comparison of the model configurations evaluated "
            "during Notebooks 4–6B."
        ),
    },
    "Dummy Baseline Confusion Matrix": {
        "filename": "dummy_baseline_confusion_matrix.png",
        "category": "Baseline Models",
        "description": (
            "Confusion matrix for the majority-class dummy baseline."
        ),
    },
    "Baseline Metric Comparison": {
        "filename": "notebook_4_baseline_metric_comparison.png",
        "category": "Baseline Models",
        "description": (
            "Comparison of the baseline model evaluation metrics."
        ),
    },
    "Baseline Precision-Recall Curves": {
        "filename": "notebook_4_baseline_precision_recall_curves.png",
        "category": "Baseline Models",
        "description": (
            "Precision-recall curves for the baseline models."
        ),
    },
    "Baseline ROC Curves": {
        "filename": "notebook_4_baseline_roc_curves.png",
        "category": "Baseline Models",
        "description": (
            "ROC curves for the baseline models."
        ),
    },
    "Candidate Model Metric Comparison": {
        "filename": "notebook_5_candidate_metric_comparison.png",
        "category": "Candidate Models",
        "description": (
             "Performance comparison of the evaluated candidate models."
        ),
    },
    "Candidate Precision-Recall Curves": {
        "filename": "notebook_5_candidate_precision_recall_curves.png",
        "category": "Candidate Models",
        "description": (
            "Precision-recall curves for the evaluated candidate models."
        ),
    },
    "Candidate ROC Curves": {
        "filename": "notebook_5_candidate_roc_curves.png",
        "category": "Candidate Models",
        "description": (
            "ROC curves for the evaluated candidate models."
        ),
    },
    "Threshold Balanced Accuracy": {
        "filename": "notebook_6_threshold_balanced_accuracy.png",
        "category": "Threshold Analysis",
        "description": (
            "Balanced accuracy across the evaluated probability thresholds."
        ),
    },
    "False Positive and False Negative Trade-off": {
        "filename": (
            "notebook_6_threshold_false_positive_"
            "false_negative_tradeoff.png"
        ),
        "category": "Threshold Analysis",
        "description": (
            "Trade-off between false-positive and false-negative counts "
            "at different thresholds."
        ),
    },
    "Recall, Precision and F1 Trade-off": {
        "filename": "notebook_6_threshold_recall_precision_f1.png",
        "category": "Threshold Analysis",
        "description": (
            "Changes in recall, precision, and F1-score across "
            "different thresholds."
        ),
    },
}

# ---------------------------------------------------------
# Dataset summary loader
# ---------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_dataset_summary(csv_path: str) -> dict:
    """
    Read only the columns needed for the dashboard summary.

    This function does not load patient split assignments,
    trained models, validation predictions, or test results.
    """

    # Read only the header first to determine the total column count.
    header = pd.read_csv(csv_path, nrows=0)
    all_columns = header.columns.tolist()

    required_columns = [
        column
        for column in ["patient_nbr", "readmitted_30"]
        if column in all_columns
    ]

    # Read only the columns needed for summary calculations.
    summary_data = pd.read_csv(
        csv_path,
        usecols=required_columns,
    )

    total_encounters = len(summary_data)
    total_columns = len(all_columns)

    identifier_columns = [
        column
        for column in ["encounter_id", "patient_nbr"]
        if column in all_columns
    ]

    non_predictor_columns = identifier_columns.copy()

    if "readmitted_30" in all_columns:
        non_predictor_columns.append("readmitted_30")

    predictor_count = total_columns - len(non_predictor_columns)

    if "patient_nbr" in summary_data.columns:
        unique_patients = summary_data["patient_nbr"].nunique()
    else:
        unique_patients = None

    if "readmitted_30" in summary_data.columns:
        target = pd.to_numeric(
            summary_data["readmitted_30"],
            errors="coerce",
        )

        not_readmitted_count = int((target == 0).sum())
        readmitted_count = int((target == 1).sum())

        valid_target_count = not_readmitted_count + readmitted_count

        if valid_target_count > 0:
            readmitted_rate = (
                readmitted_count / valid_target_count
            ) * 100
        else:
            readmitted_rate = 0.0
    else:
        not_readmitted_count = None
        readmitted_count = None
        readmitted_rate = None

    return {
        "total_encounters": total_encounters,
        "total_columns": total_columns,
        "unique_patients": unique_patients,
        "predictor_count": predictor_count,
        "not_readmitted_count": not_readmitted_count,
        "readmitted_count": readmitted_count,
        "readmitted_rate": readmitted_rate,
    }

# ---------------------------------------------------------
# Model-comparison loader
# ---------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_model_comparison(csv_path: str) -> pd.DataFrame:
    """
    Load pre-final model-comparison results from Notebooks 4–6B.

    This function does not load trained models, patient predictions,
    Notebook 7 results, or untouched test-set results.
    """

    comparison_data = pd.read_csv(csv_path)

    required_columns = [
        "Stage",
        "Model",
        "Threshold",
        "Accuracy (%)",
        "Balanced Accuracy (%)",
        "Precision (%)",
        "Recall (%)",
        "Specificity (%)",
        "F1 Score (%)",
        "ROC-AUC (%)",
        "PR-AUC (%)",
        "True Positives",
        "False Negatives",
        "False Positives",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in comparison_data.columns
    ]

    if missing_columns:
        raise ValueError(
            "The comparison file is missing these required columns: "
            + ", ".join(missing_columns)
        )

    # Safety guard: display only results generated before Notebook 7.
    safe_stage_pattern = r"^Notebook (4|5|6)"

    safe_comparison_data = comparison_data[
        comparison_data["Stage"]
        .astype(str)
        .str.match(safe_stage_pattern, na=False)
    ].copy()

    if safe_comparison_data.empty:
        raise ValueError(
            "No safe Notebook 4–6 model-comparison rows were found."
        )

    numeric_columns = [
        column
        for column in required_columns
        if column not in ["Stage", "Model"]
    ]

    for column in numeric_columns:
        safe_comparison_data[column] = pd.to_numeric(
            safe_comparison_data[column],
            errors="coerce",
        )

    return safe_comparison_data[required_columns]

# ---------------------------------------------------------
# Streamlit page configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Hospital Readmission Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------
with st.sidebar:
    st.title("Project Navigation")

    st.markdown(
        """
        - Project Overview
        - Dataset Summary
        - Model Comparison
        - Saved Figures
        - Model Decision Status
        """
    )

    st.info(
        "The final prediction model has not been selected. "
    )


# ---------------------------------------------------------
# Main page heading
# ---------------------------------------------------------
st.title("🏥 Hospital Readmission Risk Prediction")

st.subheader("ASDS 6306 Capstone Project")

# ---------------------------------------------------------
# Project overview
# ---------------------------------------------------------
st.markdown(
    """
    This dashboard presents the current development status of a machine-learning
    system designed to identify hospital encounters with a higher risk of
    readmission within 30 days.
    """
)

st.divider()

st.header("Project Overview")

overview_col1, overview_col2 = st.columns(2)

with overview_col1:
    st.subheader("Business Problem")

    st.write(
        """
        Hospital readmissions can increase healthcare costs and may indicate
        that some patients require additional follow-up care after discharge.
        Identifying higher-risk encounters can help healthcare teams prioritize
        interventions and post-discharge support.
        """
    )

    st.subheader("Project Objective")

    st.write(
        """
        Develop and evaluate machine-learning models that can identify patients
        who may be readmitted within 30 days of hospital discharge.
        """
    )

with overview_col2:
    st.subheader("Prediction Target")

    st.write(
        """
        The target variable is **readmitted_30**:

        - **1:** The patient was readmitted within 30 days.
        - **0:** The patient was not readmitted within 30 days.
        """
    )

    st.subheader("Modeling Priority")

    st.write(
        """
        Recall is an important evaluation priority because the project aims to
        capture as many actual 30-day readmissions as reasonably possible while
        also reviewing precision, accuracy, specificity, F1-score, ROC-AUC,
        and PR-AUC.
        """
    )

st.subheader("Current Project Workflow")

st.markdown(
    """
    1. **Data audit and cleaning** — Completed  
    2. **Exploratory data analysis** — Completed  
    3. **Patient-level data splitting and preprocessing** — Completed  
    4. **Baseline and candidate model evaluation** — Completed  
    5. **Model tuning and threshold analysis** — Completed through Notebook 6B  
    6. **Professor review and final model selection** — Pending  
    7. **Final untouched test-set evaluation** — Not started  
    8. **Patient prediction application** — Not started
    """
)

# ---------------------------------------------------------
# Dataset summary
# ---------------------------------------------------------
st.divider()

st.header("Dataset Summary")

st.write(
    """
    The following statistics are calculated from the cleaned modeling dataset
    created during Notebook 1. The dashboard does not access the final test set
    or calculate any model-performance results in this section.
    """
)

if not DATASET_PATH.exists():
    st.error(
        "The cleaned modeling dataset could not be found at: "
        f"`{DATASET_PATH}`"
    )

    st.info(
        "Confirm that the file "
        "`data/processed/diabetic_modeling_data_final.csv` exists."
    )

else:
    try:
        dataset_summary = load_dataset_summary(
            str(DATASET_PATH)
        )

        dataset_col1, dataset_col2, dataset_col3 = st.columns(3)

        with dataset_col1:
            st.metric(
                label="Total Encounters",
                value=f"{dataset_summary['total_encounters']:,}",
            )

        with dataset_col2:
            unique_patients = dataset_summary["unique_patients"]

            st.metric(
                label="Unique Patients",
                value=(
                    f"{unique_patients:,}"
                    if unique_patients is not None
                    else "Unavailable"
                ),
            )

        with dataset_col3:
            st.metric(
                label="Dataset Columns",
                value=f"{dataset_summary['total_columns']:,}",
            )

        dataset_col4, dataset_col5 = st.columns(2)

        with dataset_col4:
            st.metric(
                label="Modeling Predictors",
                value=f"{dataset_summary['predictor_count']:,}",
            )

        with dataset_col5:
            readmitted_rate = dataset_summary["readmitted_rate"]

            st.metric(
                label="30-Day Readmission Rate",
                value=(
                    f"{readmitted_rate:.2f}%"
                    if readmitted_rate is not None
                    else "Unavailable"
                ),
            )

        st.subheader("Target Class Distribution")

        if (
            dataset_summary["not_readmitted_count"] is not None
            and dataset_summary["readmitted_count"] is not None
        ):
            total_target_records = (
                dataset_summary["not_readmitted_count"]
                + dataset_summary["readmitted_count"]
            )

            class_distribution = pd.DataFrame(
                {
                    "Target Value": [0, 1],
                    "Target Meaning": [
                        "Not readmitted within 30 days",
                        "Readmitted within 30 days",
                    ],
                    "Number of Encounters": [
                        dataset_summary["not_readmitted_count"],
                        dataset_summary["readmitted_count"],
                    ],
                    "Percentage": [
                        (
                            dataset_summary["not_readmitted_count"]
                            / total_target_records
                        )
                        * 100,
                        (
                            dataset_summary["readmitted_count"]
                            / total_target_records
                        )
                        * 100,
                    ],
                }
            )

            class_distribution["Percentage"] = (
                class_distribution["Percentage"]
                .map(lambda value: f"{value:.2f}%")
            )

            st.dataframe(
                class_distribution,
                hide_index=True,
                use_container_width=True,
            )

        st.info(
            """
            `encounter_id` is retained for encounter tracking, while
            `patient_nbr` identifies repeated encounters belonging to the same
            patient. Neither identifier is used as a model predictor.
            """
        )

        st.caption(
            "Source: data/processed/"
            "diabetic_modeling_data_final.csv"
        )

    except Exception as error:
        st.error(
            "The dataset summary could not be calculated."
        )

        st.exception(error)

# ---------------------------------------------------------
# Model comparison
# ---------------------------------------------------------
st.divider()

st.header("Model Comparison")

st.write(
    """
    This section displays the pre-final model results produced during
    Notebooks 4–6B. These results support discussion with the professor,
    but they do not represent a locked final model.
    """
)

st.warning(
    """
    The comparison below does not contain final test-set evaluation.
    Notebook 7 has not started, and no model is being declared as the
    final prediction model.
    """
)

if not MODEL_COMPARISON_PATH.exists():
    st.error(
        "The model-comparison file could not be found at: "
        f"`{MODEL_COMPARISON_PATH}`"
    )

    st.info(
        "Confirm that "
        "`outputs/metrics/dynamic_all_model_comparison_summary.csv` "
        "exists."
    )

else:
    try:
        model_comparison = load_model_comparison(
            str(MODEL_COMPARISON_PATH)
        )

        comparison_col1, comparison_col2, comparison_col3 = st.columns(3)

        with comparison_col1:
            st.metric(
                label="Compared Configurations",
                value=f"{len(model_comparison):,}",
            )

        with comparison_col2:
            st.metric(
                label="Highest Recall Observed",
                value=f"{model_comparison['Recall (%)'].max():.2f}%",
            )

        with comparison_col3:
            st.metric(
                label="Highest Accuracy Observed",
                value=f"{model_comparison['Accuracy (%)'].max():.2f}%",
            )

        st.caption(
            "The highest recall and highest accuracy may come from different "
            "model configurations. These values do not select a final model."
        )

        st.subheader("Key Model Metrics")

        key_metric_columns = [
            "Stage",
            "Model",
            "Threshold",
            "Accuracy (%)",
            "Precision (%)",
            "Recall (%)",
            "Specificity (%)",
            "F1 Score (%)",
            "ROC-AUC (%)",
            "PR-AUC (%)",
        ]

        key_metrics_table = model_comparison[
            key_metric_columns
        ].copy()

        st.dataframe(
            key_metrics_table,
            hide_index=True,
            width="stretch",
            height=600,
            column_config={
                "Stage": st.column_config.TextColumn(
                    "Notebook Stage",
                    width="medium",
                ),
                "Model": st.column_config.TextColumn(
                    "Model Configuration",
                    width="large",
                ),
                "Threshold": st.column_config.NumberColumn(
                    "Threshold",
                    format="%.2f",
                ),
                "Accuracy (%)": st.column_config.NumberColumn(
                    "Accuracy (%)",
                    format="%.2f",
                ),
                "Precision (%)": st.column_config.NumberColumn(
                    "Precision (%)",
                    format="%.2f",
                ),
                "Recall (%)": st.column_config.NumberColumn(
                    "Recall (%)",
                    format="%.2f",
                ),
                "Specificity (%)": st.column_config.NumberColumn(
                    "Specificity (%)",
                    format="%.2f",
                ),
                "F1 Score (%)": st.column_config.NumberColumn(
                    "F1 Score (%)",
                    format="%.2f",
                ),
                "ROC-AUC (%)": st.column_config.NumberColumn(
                    "ROC-AUC (%)",
                    format="%.2f",
                ),
                "PR-AUC (%)": st.column_config.NumberColumn(
                    "PR-AUC (%)",
                    format="%.2f",
                ),
            },
        )

        with st.expander("View confusion-matrix counts"):
            count_columns = [
                "Stage",
                "Model",
                "Threshold",
                "True Positives",
                "False Negatives",
                "False Positives",
            ]

            st.dataframe(
                model_comparison[count_columns],
                hide_index=True,
                width="stretch",
            )

        st.info(
            """
            Because recall is the project priority, higher recall means that
            more actual readmissions were identified. However, recall must be
            interpreted together with false positives, precision, specificity,
            and operational usefulness.
            """
        )

        st.caption(
            "Source: outputs/metrics/"
            "dynamic_all_model_comparison_summary.csv"
        )

    except Exception as error:
        st.error(
            "The model-comparison table could not be loaded."
        )

        st.exception(error)

# ---------------------------------------------------------
# Saved figures
# ---------------------------------------------------------
st.divider()

st.header("Saved Figures")

st.write(
    """
    This section displays visualizations generated during baseline modeling,
    candidate-model evaluation, and threshold analysis. The figures are shown for model-development review
    and do not contain final test-set evaluation.
    """
)

st.warning(
    """
    Only approved model-development figures are available here.
    Final evaluation figures and test-set results are not loaded.
    """
)

if not FIGURES_DIR.exists():
    st.error(
        "The saved-figures folder could not be found at: "
        f"`{FIGURES_DIR}`"
    )

else:
    available_figures = {}
    missing_figures = []

    for figure_label, figure_info in SAFE_FIGURES.items():
        figure_path = FIGURES_DIR / figure_info["filename"]

        if figure_path.exists():
            available_figures[figure_label] = {
                **figure_info,
                "path": figure_path,
            }
        else:
            missing_figures.append(figure_info["filename"])

    if not available_figures:
        st.error(
            "None of the approved saved figures could be found."
        )

    else:
        figure_col1, figure_col2 = st.columns(2)

        with figure_col1:
            st.metric(
                label="Approved Figures Found",
                value=len(available_figures),
            )

        with figure_col2:
            st.metric(
                label="Missing Approved Figures",
                value=len(missing_figures),
            )

        available_categories = []

        for figure_info in available_figures.values():
            category = figure_info["category"]

            if category not in available_categories:
                available_categories.append(category)

        selected_category = st.selectbox(
             "Select an analysis stage",
             options=available_categories,
        )

        category_figures = {
            figure_label: figure_info
            for figure_label, figure_info in available_figures.items()
            if figure_info["category"] == selected_category
        }

        selected_figure_label = st.selectbox(
            "Select a saved figure",
            options=list(category_figures.keys()),
        )

        selected_figure = category_figures[
            selected_figure_label
        ]

        st.subheader(selected_figure_label)

        st.write(selected_figure["description"])

        st.image(
            selected_figure["path"],
            caption=selected_figure_label,
            width="stretch",
        )

        st.caption(
            "Source: outputs/figures/"
            f"{selected_figure['filename']}"
        )

        with st.expander("View all approved figure filenames"):
            for figure_label, figure_info in available_figures.items():
                st.write(
                    f"**{figure_info['category']} — "
                    f"{figure_label}**"
                )

                st.code(
                    figure_info["filename"],
                    language=None,
                )

        if missing_figures:
            with st.expander("View missing approved figures"):
                for missing_filename in missing_figures:
                    st.write(f"- `{missing_filename}`")

# ---------------------------------------------------------
# CSV readmission-risk prediction
# ---------------------------------------------------------
st.divider()

st.header("Patient Readmission Risk Prediction")

st.markdown(
    """
    - Project Overview
    - Dataset Summary
    - Model Comparison
    - Saved Figures
    - Patient Risk Prediction
    - Final Model Status
    """
)

st.write(
    """
    Upload a CSV containing one or more hospital encounter records.
    The file must contain the 43 predictors required by the finalized
    Tuned XGBoost model.
    """
)

st.info(
    """
    Download the blank template when preparing new records. For testing,
    use the sample file containing one demonstration record.
    """
)

st.warning(
    """
    This application is an academic decision-support demonstration.
    Predictions should not replace clinical judgment, medical assessment,
    or established hospital procedures.
    """
)

download_col1, download_col2 = st.columns(2)

with download_col1:
    if PATIENT_TEMPLATE_PATH.exists():
        st.download_button(
            label="Download Blank CSV Template",
            data=PATIENT_TEMPLATE_PATH.read_bytes(),
            file_name="patient_input_template.csv",
            mime="text/csv",
            use_container_width=True,
        )
    else:
        st.error(
            "The blank patient-input template could not be found."
        )

with download_col2:
    if SAMPLE_PATIENT_PATH.exists():
        st.download_button(
            label="Download Sample Test CSV",
            data=SAMPLE_PATIENT_PATH.read_bytes(),
            file_name="sample_patient_input.csv",
            mime="text/csv",
            use_container_width=True,
        )
    else:
        st.error(
            "The sample patient-input CSV could not be found."
        )

uploaded_patient_file = st.file_uploader(
    "Upload a completed patient CSV",
    type=["csv"],
    accept_multiple_files=False,
    help=(
        "The CSV must contain all 43 required predictor columns. "
        "It may contain one or multiple patient encounter rows."
    ),
)

if uploaded_patient_file is not None:
    try:
        uploaded_file_bytes = uploaded_patient_file.getvalue()

        upload_signature = (
            uploaded_patient_file.name,
            len(uploaded_file_bytes),
        )

        previous_signature = st.session_state.get(
            "patient_upload_signature"
        )

        if upload_signature != previous_signature:
            st.session_state[
                "patient_upload_signature"
            ] = upload_signature

            st.session_state.pop(
                "batch_prediction_results",
                None,
            )

            st.session_state.pop(
                "batch_prediction_download",
                None,
            )

        uploaded_patient_data = pd.read_csv(
            BytesIO(uploaded_file_bytes)
        )

        st.success(
            f"CSV loaded successfully: "
            f"{len(uploaded_patient_data):,} record(s) and "
            f"{len(uploaded_patient_data.columns):,} column(s)."
        )

        st.subheader("Uploaded Data Preview")

        st.dataframe(
            uploaded_patient_data.head(10),
            hide_index=True,
            width="stretch",
        )

        if len(uploaded_patient_data.columns) != 43:
            st.warning(
                """
                The uploaded file does not currently contain exactly
                43 columns. Click the prediction button to receive a
                detailed validation message identifying missing or
                unexpected columns.
                """
            )

        predict_button = st.button(
            "Generate Readmission Predictions",
            type="primary",
            use_container_width=True,
        )

        if predict_button:
            with st.spinner(
                "Validating the CSV and calculating predictions..."
            ):
                prediction_results = (
                    predict_readmission_batch(
                        uploaded_patient_data
                    )
                )

                combined_results = pd.concat(
                    [
                        prediction_results.reset_index(
                            drop=True
                        ),
                        uploaded_patient_data.reset_index(
                            drop=True
                        ),
                    ],
                    axis=1,
                )

                downloadable_results = (
                    combined_results.to_csv(
                        index=False
                    ).encode("utf-8")
                )

                st.session_state[
                    "batch_prediction_results"
                ] = prediction_results

                st.session_state[
                    "batch_prediction_download"
                ] = downloadable_results

        prediction_results = st.session_state.get(
            "batch_prediction_results"
        )

        downloadable_results = st.session_state.get(
            "batch_prediction_download"
        )

        if prediction_results is not None:
            st.divider()

            st.subheader("Prediction Results")

            total_records = len(prediction_results)

            main_high_risk_count = int(
                (
                    prediction_results[
                        "Main Classification"
                    ]
                    == "Higher Readmission Risk"
                ).sum()
            )

            recall_flagged_count = int(
                (
                    prediction_results[
                        "Recall-Focused Classification"
                    ]
                    == "Flagged for Screening"
                ).sum()
            )

            average_probability = (
                prediction_results[
                    "Readmission Probability (%)"
                ].mean()
            )

            result_col1, result_col2, result_col3, result_col4 = (
                st.columns(4)
            )

            with result_col1:
                st.metric(
                    label="Records Processed",
                    value=f"{total_records:,}",
                )

            with result_col2:
                st.metric(
                    label="Main Higher-Risk Records",
                    value=f"{main_high_risk_count:,}",
                )

            with result_col3:
                st.metric(
                    label="Recall-Focused Flags",
                    value=f"{recall_flagged_count:,}",
                )

            with result_col4:
                st.metric(
                    label="Average Probability",
                    value=f"{average_probability:.2f}%",
                )

            display_results = prediction_results[
                [
                    "Record Number",
                    "Readmission Probability (%)",
                    "Main Threshold",
                    "Main Classification",
                    "Recall-Focused Threshold",
                    "Recall-Focused Classification",
                ]
            ].copy()

            display_results[
                "Readmission Probability (%)"
            ] = display_results[
                "Readmission Probability (%)"
            ].round(2)

            st.dataframe(
                display_results,
                hide_index=True,
                width="stretch",
                column_config={
                    "Readmission Probability (%)": (
                        st.column_config.NumberColumn(
                            "Readmission Probability (%)",
                            format="%.2f",
                        )
                    ),
                    "Main Threshold": (
                        st.column_config.NumberColumn(
                            "Main Threshold",
                            format="%.2f",
                        )
                    ),
                    "Recall-Focused Threshold": (
                        st.column_config.NumberColumn(
                            "Recall-Focused Threshold",
                            format="%.2f",
                        )
                    ),
                },
            )

            st.caption(
                """
                Main classification uses threshold 0.50. Recall-focused
                screening uses threshold 0.45 and therefore flags more
                encounters for additional review.
                """
            )

            if downloadable_results is not None:
                st.download_button(
                    label="Download Prediction Results",
                    data=downloadable_results,
                    file_name=(
                        "hospital_readmission_predictions.csv"
                    ),
                    mime="text/csv",
                    type="primary",
                    use_container_width=True,
                )

    except pd.errors.EmptyDataError:
        st.error(
            "The uploaded CSV is empty or does not contain readable data."
        )

    except pd.errors.ParserError:
        st.error(
            """
            The uploaded file could not be parsed as a valid CSV.
            Check its formatting and try again.
            """
        )

    except Exception as error:
        st.error(
            "The uploaded CSV could not be processed."
        )

        st.exception(error)

# ---------------------------------------------------------
# Model decision status
# ---------------------------------------------------------
st.divider()

st.header("Model Decision Status")

st.warning(
    """
    Final model selection is currently paused while awaiting professor
    guidance. The validation results are available for review, but no model
    or probability threshold has been approved as final.
    """
)

status_col1, status_col2, status_col3, status_col4 = st.columns(4)

with status_col1:
    st.metric(
        label="Completed Development",
        value="Notebooks 1–6B",
    )

with status_col2:
    st.metric(
        label="Professor Review",
        value="Pending",
    )

with status_col3:
    st.metric(
        label="Final Model",
        value="Not Selected",
    )

with status_col4:
    st.metric(
        label="Test Set",
        value="Untouched",
    )

st.subheader("Decision Checklist")

decision_checklist = pd.DataFrame(
    {
        "Decision Item": [
            "Validation models compared",
            "Threshold alternatives reviewed",
            "Professor recommendation received",
            "Final model selected",
            "Final prediction threshold selected",
            "Notebook 7 test evaluation started",
            "Untouched test set evaluated",
            "Patient prediction form enabled",
        ],
        "Current Status": [
            "Completed",
            "Completed",
            "Pending",
            "Not completed",
            "Not completed",
            "Not started",
            "Not started",
            "Disabled",
        ],
    }
)

st.dataframe(
    decision_checklist,
    hide_index=True,
    width="stretch",
    column_config={
        "Decision Item": st.column_config.TextColumn(
            "Project Decision Item",
            width="large",
        ),
        "Current Status": st.column_config.TextColumn(
            "Status",
            width="medium",
        ),
    },
)

st.subheader("Current Decision Principles")

st.markdown(
    """
    - **Recall remains the primary modeling priority** because the objective is
      to identify as many actual 30-day readmissions as reasonably possible.
    - Accuracy alone will not be used to select the model.
    - Precision, specificity, balanced accuracy, F1-score, ROC-AUC, PR-AUC,
      false positives, and false negatives must also be considered.
    - Validation results are used only for model development and comparison.
    - The untouched test set will be used only after the final model and
      threshold are approved.
    """
)

with st.expander("What happens after the professor responds?"):
    st.markdown(
        """
        1. Record the professor's model-selection recommendation.
        2. Confirm the final model configuration.
        3. Confirm the final probability threshold.
        4. Lock the final preprocessing and prediction pipeline.
        5. Start Notebook 7.
        6. Evaluate the selected model once on the untouched test set.
        7. Report the final test metrics.
        8. Add the patient prediction form only after final evaluation.
        """
    )

st.error(
    """
    Current restriction: do not start Notebook 7, do not access the test set,
    and do not enable patient-level predictions until the final model decision
    is confirmed.
    """
)
