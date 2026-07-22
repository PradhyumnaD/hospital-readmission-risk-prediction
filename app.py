from __future__ import annotations

from io import BytesIO
from pathlib import Path
import hashlib

import pandas as pd
import streamlit as st

from prediction_service import (
    explain_readmission_batch,
    predict_readmission_batch,
)


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
# Project file paths
# ---------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent

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

FINAL_THRESHOLD_RESULTS_PATH = (
    PROJECT_ROOT
    / "outputs"
    / "metrics"
    / "notebook_7_final_threshold_comparison_table.csv"
)

GLOBAL_SHAP_IMPORTANCE_PATH = (
    PROJECT_ROOT
    / "outputs"
    / "metrics"
    / "notebook_8_grouped_original_shap_importance.csv"
)

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

FIGURES_DIR = PROJECT_ROOT / "outputs" / "figures"


# ---------------------------------------------------------
# Approved saved figures
# ---------------------------------------------------------
APPROVED_FIGURES = {
    "Overall Model Comparison Summary": {
        "filename": "dynamic_all_model_comparison_summary.png",
        "category": "Overall Comparison",
        "description": (
            "Summary comparison of the development-stage model "
            "configurations evaluated before final test evaluation."
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
            "Comparison of evaluation metrics for the baseline models."
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
        "description": "ROC curves for the baseline models.",
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
        "description": "ROC curves for the evaluated candidate models.",
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
    "Final Confusion Matrix — Threshold 0.50": {
        "filename": "notebook_7_final_confusion_matrix_threshold_050.png",
        "category": "Final Evaluation",
        "description": (
            "Final untouched test-set confusion matrix at the main "
            "balanced threshold of 0.50."
        ),
    },
    "Final Confusion Matrix — Threshold 0.45": {
        "filename": "notebook_7_final_confusion_matrix_threshold_045.png",
        "category": "Final Evaluation",
        "description": (
            "Final untouched test-set confusion matrix at the "
            "recall-focused screening threshold of 0.45."
        ),
    },
    "Final Threshold Comparison": {
        "filename": "notebook_7_final_threshold_comparison_table.png",
        "category": "Final Evaluation",
        "description": (
            "Visual comparison of the two final operating thresholds."
        ),
    },
    "Final Precision-Recall Curve": {
        "filename": "notebook_7_final_xgboost_precision_recall_curve.png",
        "category": "Final Evaluation",
        "description": (
            "Precision-recall performance of the finalized Tuned XGBoost "
            "model on the untouched test set."
        ),
    },
    "Final ROC Curve": {
        "filename": "notebook_7_final_xgboost_roc_curve.png",
        "category": "Final Evaluation",
        "description": (
            "ROC performance of the finalized Tuned XGBoost model on "
            "the untouched test set."
        ),
    },
    "Grouped Original Feature Importance": {
        "filename": (
            "notebook_8_top_15_grouped_original_feature_importance.png"
        ),
        "category": "Model Explainability",
        "description": (
            "Top grouped original predictors based on XGBoost feature "
            "importance."
        ),
    },
    "Grouped Original SHAP Importance": {
        "filename": "notebook_8_top_15_grouped_original_shap_importance.png",
        "category": "Model Explainability",
        "description": (
            "Top grouped original predictors based on global mean "
            "absolute SHAP values."
        ),
    },
    "Transformed Feature Importance": {
        "filename": "notebook_8_top_20_xgboost_feature_importance.png",
        "category": "Model Explainability",
        "description": (
            "Top transformed features according to XGBoost importance."
        ),
    },
    "Transformed SHAP Importance": {
        "filename": (
            "notebook_8_top_20_xgboost_shap_transformed_importance.png"
        ),
        "category": "Model Explainability",
        "description": (
            "Top transformed features according to global SHAP importance."
        ),
    },
    "High-Risk Patient SHAP Example": {
        "filename": (
            "notebook_8_selected_high_risk_patient_shap_explanation.png"
        ),
        "category": "Model Explainability",
        "description": (
            "Example local SHAP explanation for a selected high-risk "
            "patient encounter."
        ),
    },
    "True-Positive Patient SHAP Example": {
        "filename": "notebook_8_true_positive_patient_shap_explanation.png",
        "category": "Model Explainability",
        "description": (
            "Example local SHAP explanation for a correctly identified "
            "readmission encounter."
        ),
    },
}


FEATURE_LABELS = {
    "discharge_disposition_id": "Discharge Disposition",
    "medical_specialty_group": "Medical Specialty",
    "diag_1_group": "Primary Diagnosis Group",
    "diag_2_group": "Secondary Diagnosis Group",
    "diag_3_group": "Additional Diagnosis Group",
    "number_inpatient": "Previous Inpatient Visits",
    "number_outpatient": "Previous Outpatient Visits",
    "number_emergency": "Previous Emergency Visits",
    "A1Cresult": "A1C Test Result",
    "max_glu_serum": "Maximum Glucose Serum Result",
}


DISCHARGE_DISPOSITION_LABELS = {
    "1": "Discharged to Home",
    "2": "Transferred to Short-Term Hospital",
    "3": "Transferred to Skilled Nursing Facility",
    "4": "Transferred to Intermediate Care Facility",
    "5": "Transferred to Inpatient Care Institution",
    "6": "Discharged Home with Home Health Service",
    "7": "Left Against Medical Advice",
    "8": "Discharged Home with IV Provider",
    "9": "Admitted as an Inpatient to This Hospital",
    "10": "Transferred to Another Hospital",
    "12": "Still a Patient or Expected to Return",
    "15": "Transferred Within Institution",
    "16": "Transferred to Outpatient Services",
    "17": "Transferred to Emergency Department",
    "18": "Unknown or Not Mapped",
    "22": "Transferred to Rehabilitation Facility",
    "23": "Transferred to Long-Term Care Hospital",
    "24": "Transferred to Nursing Facility",
    "25": "Unknown or Not Mapped",
    "27": "Transferred to Federal Healthcare Facility",
    "28": "Transferred to Psychiatric Hospital",
}


# ---------------------------------------------------------
# Cached data loaders
# ---------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_dataset_summary(csv_path: str) -> dict:
    """Calculate summary statistics from the cleaned modeling dataset."""

    header = pd.read_csv(csv_path, nrows=0)
    all_columns = header.columns.tolist()

    required_columns = [
        column
        for column in ["patient_nbr", "readmitted_30"]
        if column in all_columns
    ]

    summary_data = pd.read_csv(csv_path, usecols=required_columns)

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

    unique_patients = (
        int(summary_data["patient_nbr"].nunique())
        if "patient_nbr" in summary_data.columns
        else None
    )

    not_readmitted_count = None
    readmitted_count = None
    readmitted_rate = None

    if "readmitted_30" in summary_data.columns:
        target = pd.to_numeric(
            summary_data["readmitted_30"],
            errors="coerce",
        )
        not_readmitted_count = int((target == 0).sum())
        readmitted_count = int((target == 1).sum())
        valid_target_count = not_readmitted_count + readmitted_count
        readmitted_rate = (
            (readmitted_count / valid_target_count) * 100
            if valid_target_count > 0
            else 0.0
        )

    return {
        "total_encounters": total_encounters,
        "total_columns": total_columns,
        "unique_patients": unique_patients,
        "predictor_count": predictor_count,
        "not_readmitted_count": not_readmitted_count,
        "readmitted_count": readmitted_count,
        "readmitted_rate": readmitted_rate,
    }


@st.cache_data(show_spinner=False)
def load_model_comparison(csv_path: str) -> pd.DataFrame:
    """Load model-development comparison results from stages 4–6B."""

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
            "The comparison file is missing required columns: "
            + ", ".join(missing_columns)
        )

    safe_comparison = comparison_data[
        comparison_data["Stage"]
        .astype(str)
        .str.match(r"^Notebook (4|5|6)", na=False)
    ].copy()

    if safe_comparison.empty:
        raise ValueError(
            "No model-development comparison rows were found."
        )

    numeric_columns = [
        column
        for column in required_columns
        if column not in ["Stage", "Model"]
    ]
    for column in numeric_columns:
        safe_comparison[column] = pd.to_numeric(
            safe_comparison[column],
            errors="coerce",
        )

    safe_comparison["Analysis Stage"] = (
        safe_comparison["Stage"].astype(str).map(format_analysis_stage)
    )

    return safe_comparison[
        ["Analysis Stage"]
        + [column for column in required_columns if column != "Stage"]
    ]


@st.cache_data(show_spinner=False)
def load_final_threshold_results(csv_path: str) -> pd.DataFrame:
    """Load the final untouched test-set threshold results."""

    final_results = pd.read_csv(csv_path)

    required_columns = [
        "Operating Point",
        "Threshold",
        "Accuracy (%)",
        "Balanced Accuracy (%)",
        "Precision (%)",
        "Recall (%)",
        "Specificity (%)",
        "F1 Score (%)",
        "ROC-AUC (%)",
        "PR-AUC (%)",
        "Readmissions Caught",
        "Readmissions Missed",
        "False Positives",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in final_results.columns
    ]
    if missing_columns:
        raise ValueError(
            "The final results file is missing required columns: "
            + ", ".join(missing_columns)
        )

    numeric_columns = [
        column
        for column in required_columns
        if column != "Operating Point"
    ]
    for column in numeric_columns:
        final_results[column] = pd.to_numeric(
            final_results[column],
            errors="coerce",
        )

    return final_results[required_columns]


@st.cache_data(show_spinner=False)
def load_global_shap_importance(csv_path: str) -> pd.DataFrame:
    """Load grouped original-feature SHAP importance."""

    shap_data = pd.read_csv(csv_path)
    required_columns = [
        "rank",
        "original_feature",
        "total_mean_absolute_shap",
        "mean_shap",
        "number_transformed_features",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in shap_data.columns
    ]
    if missing_columns:
        raise ValueError(
            "The SHAP importance file is missing required columns: "
            + ", ".join(missing_columns)
        )

    shap_data = shap_data[required_columns].copy()
    shap_data["Feature"] = shap_data["original_feature"].map(
        format_feature_name
    )

    return shap_data.sort_values("rank")


# ---------------------------------------------------------
# Helper functions
# ---------------------------------------------------------
def format_analysis_stage(stage: str) -> str:
    """Convert notebook-stage text into a user-friendly label."""

    stage_lower = stage.lower()
    if "baseline" in stage_lower:
        return "Baseline Models"
    if "candidate" in stage_lower:
        return "Candidate Models"
    if "threshold" in stage_lower:
        return "Threshold Analysis"
    if "tuned" in stage_lower:
        return "Tuned Models"
    if "advanced" in stage_lower or "6b" in stage_lower:
        return "Advanced Models"
    return stage.replace("Notebook", "Modeling Stage")


def format_feature_name(feature_name: str) -> str:
    """Convert an internal feature name into a readable label."""

    if feature_name in FEATURE_LABELS:
        return FEATURE_LABELS[feature_name]

    return (
        str(feature_name)
        .replace("_", " ")
        .replace("-", " ")
        .title()
    )


def format_patient_value(
    original_feature: str,
    patient_value,
) -> str:
    """Convert coded patient values into readable descriptions."""

    if original_feature == "discharge_disposition_id":
        value_key = str(patient_value).strip()

        try:
            numeric_value = float(value_key)
            if numeric_value.is_integer():
                value_key = str(int(numeric_value))
        except (TypeError, ValueError):
            pass

        return DISCHARGE_DISPOSITION_LABELS.get(
            value_key,
            f"Disposition Code {value_key}",
        )

    return str(patient_value)


def find_threshold_row(
    final_results: pd.DataFrame,
    threshold: float,
) -> pd.Series | None:
    """Return the row closest to a requested threshold."""

    if final_results.empty:
        return None

    threshold_difference = (
        final_results["Threshold"] - threshold
    ).abs()
    row_index = threshold_difference.idxmin()
    row = final_results.loc[row_index]

    if abs(float(row["Threshold"]) - threshold) > 0.001:
        return None

    return row


def metric_value(row: pd.Series | None, column: str) -> str:
    """Format a percentage metric from a final-results row."""

    if row is None or pd.isna(row[column]):
        return "Unavailable"
    return f"{float(row[column]):.2f}%"


def integer_value(row: pd.Series | None, column: str) -> str:
    """Format an integer count from a final-results row."""

    if row is None or pd.isna(row[column]):
        return "Unavailable"
    return f"{int(row[column]):,}"


def create_user_friendly_screening_results(
    prediction_results: pd.DataFrame,
) -> pd.DataFrame:
    """Convert technical model output into user-friendly screening labels."""

    screening_results = prediction_results.copy()

    screening_results["Main Classification"] = (
        screening_results["Main Classification"].replace(
            {
                "Flagged at Main Threshold": "Review Recommended",
                "Not Flagged at Main Threshold": (
                    "No Standard Review Flag"
                ),
            }
        )
    )

    screening_results["Recall-Focused Classification"] = (
        screening_results[
            "Recall-Focused Classification"
        ].replace(
            {
                "Flagged for Screening": (
                    "Additional Screening Recommended"
                ),
                "Not Flagged": "No Additional Screening Flag",
            }
        )
    )

    return screening_results.rename(
        columns={
            "Record Number": "Record",
            "Readmission Probability (%)": (
                "Estimated 30-Day Readmission Risk (%)"
            ),
            "Main Threshold": "Standard Review Cutoff",
            "Main Classification": "Standard Review Result",
            "Recall-Focused Threshold": (
                "Additional Screening Cutoff"
            ),
            "Recall-Focused Classification": (
                "Additional Screening Result"
            ),
        }
    )


# ---------------------------------------------------------
# Page sections
# ---------------------------------------------------------
def render_project_overview() -> None:
    st.header("Project Overview")

    st.markdown(
        """
        This capstone developed a machine-learning decision-support system
        for estimating the risk of hospital readmission within 30 days.
        The finalized Tuned XGBoost model is evaluated at two operating
        thresholds and is available through a CSV-based prediction workflow.
        """
    )

    status_col1, status_col2, status_col3, status_col4 = st.columns(4)
    with status_col1:
        st.metric("Project Status", "Completed")
    with status_col2:
        st.metric("Final Model", "Tuned XGBoost")
    with status_col3:
        st.metric("Main Threshold", "0.50")
    with status_col4:
        st.metric("Screening Threshold", "0.45")

    st.divider()

    overview_col1, overview_col2 = st.columns(2)

    with overview_col1:
        st.subheader("Business Problem")
        st.write(
            """
            Hospital readmissions can increase healthcare costs and may
            indicate that some patients require additional follow-up after
            discharge. Earlier risk identification can support prioritization
            of post-discharge review and intervention resources.
            """
        )

        st.subheader("Project Objective")
        st.write(
            """
            Develop, compare, tune, evaluate, and explain machine-learning
            models that estimate whether a hospital encounter is associated
            with readmission within 30 days.
            """
        )

    with overview_col2:
        st.subheader("Prediction Target")
        st.markdown(
            """
            The target variable is **readmitted_30**:

            - **1:** Readmitted within 30 days
            - **0:** Not readmitted within 30 days
            """
        )

        st.subheader("Modeling Priority")
        st.write(
            """
            Recall was prioritized because missing a true readmission is
            important in a screening context. Accuracy, precision,
            specificity, balanced accuracy, F1-score, ROC-AUC, PR-AUC,
            false positives, and false negatives were considered together.
            """
        )

    st.subheader("Completed Project Workflow")
    st.markdown(
        """
        1. **Data audit and cleaning** — Completed  
        2. **Exploratory data analysis** — Completed  
        3. **Patient-level splitting and preprocessing** — Completed  
        4. **Baseline and candidate model evaluation** — Completed  
        5. **Model tuning and threshold analysis** — Completed  
        6. **Final model and threshold selection** — Completed  
        7. **Untouched test-set evaluation** — Completed  
        8. **Model explainability analysis** — Completed  
        9. **CSV-based Streamlit prediction workflow** — Completed
        """
    )

    st.info(
        "The finalized model is Tuned XGBoost. Threshold 0.50 is the main "
        "balanced operating point, while threshold 0.45 is the "
        "recall-focused screening option."
    )


def render_dataset_summary() -> None:
    st.header("Dataset Summary")
    st.write(
        """
        The summary below is calculated from the cleaned modeling dataset.
        Identifiers are retained for tracking and patient-level grouping but
        are not used as model predictors.
        """
    )

    if not DATASET_PATH.exists():
        st.error(
            "The cleaned modeling dataset could not be found at: "
            f"`{DATASET_PATH}`"
        )
        return

    try:
        summary = load_dataset_summary(str(DATASET_PATH))

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Encounters", f"{summary['total_encounters']:,}")
        with col2:
            st.metric(
                "Unique Patients",
                (
                    f"{summary['unique_patients']:,}"
                    if summary["unique_patients"] is not None
                    else "Unavailable"
                ),
            )
        with col3:
            st.metric("Dataset Columns", f"{summary['total_columns']:,}")

        col4, col5 = st.columns(2)
        with col4:
            st.metric("Modeling Predictors", f"{summary['predictor_count']:,}")
        with col5:
            rate = summary["readmitted_rate"]
            st.metric(
                "30-Day Readmission Rate",
                f"{rate:.2f}%" if rate is not None else "Unavailable",
            )

        st.subheader("Target Class Distribution")

        if (
            summary["not_readmitted_count"] is not None
            and summary["readmitted_count"] is not None
        ):
            total = (
                summary["not_readmitted_count"]
                + summary["readmitted_count"]
            )
            class_distribution = pd.DataFrame(
                {
                    "Target Value": [0, 1],
                    "Target Meaning": [
                        "Not readmitted within 30 days",
                        "Readmitted within 30 days",
                    ],
                    "Number of Encounters": [
                        summary["not_readmitted_count"],
                        summary["readmitted_count"],
                    ],
                    "Percentage": [
                        (summary["not_readmitted_count"] / total) * 100,
                        (summary["readmitted_count"] / total) * 100,
                    ],
                }
            )

            st.dataframe(
                class_distribution,
                hide_index=True,
                width="stretch",
                column_config={
                    "Percentage": st.column_config.NumberColumn(
                        "Percentage",
                        format="%.2f%%",
                    )
                },
            )

        st.info(
            "`encounter_id` is used for encounter tracking and "
            "`patient_nbr` is used for patient-level grouping. Neither is "
            "used as a prediction input."
        )
        st.caption(
            "Source: data/processed/diabetic_modeling_data_final.csv"
        )

    except Exception as error:
        st.error("The dataset summary could not be calculated.")
        st.exception(error)


def render_model_development() -> None:
    st.header("Model Development Comparison")
    st.write(
        """
        These are development and validation results from the baseline,
        candidate, tuned, and threshold-analysis stages. They explain how
        the final model decision was reached; they are separate from the
        final untouched test-set evaluation.
        """
    )

    if not MODEL_COMPARISON_PATH.exists():
        st.error(
            "The model-comparison file could not be found at: "
            f"`{MODEL_COMPARISON_PATH}`"
        )
        return

    try:
        comparison = load_model_comparison(str(MODEL_COMPARISON_PATH))

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Compared Configurations", f"{len(comparison):,}")
        with col2:
            st.metric(
                "Highest Development Recall",
                f"{comparison['Recall (%)'].max():.2f}%",
            )
        with col3:
            st.metric(
                "Highest Development Accuracy",
                f"{comparison['Accuracy (%)'].max():.2f}%",
            )

        st.caption(
            "The highest recall and highest accuracy can come from different "
            "configurations. Final selection considered the complete metric "
            "trade-off rather than a single value."
        )

        key_columns = [
            "Analysis Stage",
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
        ]

        number_columns = {
            column: st.column_config.NumberColumn(column, format="%.2f")
            for column in key_columns
            if column not in ["Analysis Stage", "Model"]
        }

        st.dataframe(
            comparison[key_columns],
            hide_index=True,
            width="stretch",
            height=600,
            column_config={
                "Analysis Stage": st.column_config.TextColumn(
                    "Analysis Stage",
                    width="medium",
                ),
                "Model": st.column_config.TextColumn(
                    "Model Configuration",
                    width="large",
                ),
                **number_columns,
            },
        )

        with st.expander("View confusion-matrix counts"):
            st.dataframe(
                comparison[
                    [
                        "Analysis Stage",
                        "Model",
                        "Threshold",
                        "True Positives",
                        "False Negatives",
                        "False Positives",
                    ]
                ],
                hide_index=True,
                width="stretch",
            )

        st.info(
            "Recall was treated as a priority, but it was interpreted with "
            "precision, specificity, false positives, false negatives, and "
            "operational usefulness."
        )
        st.caption(
            "Source: outputs/metrics/"
            "dynamic_all_model_comparison_summary.csv"
        )

    except Exception as error:
        st.error("The development comparison table could not be loaded.")
        st.exception(error)


def render_final_evaluation() -> None:
    st.header("Final Model Evaluation")

    st.success(
        "Tuned XGBoost was selected as the final model and evaluated once "
        "on the previously untouched test set."
    )

    model_col1, model_col2, model_col3, model_col4 = st.columns(4)
    with model_col1:
        st.metric("Final Model", "Tuned XGBoost")
    with model_col2:
        st.metric("Test Encounters", "14,976")
    with model_col3:
        st.metric("Main Threshold", "0.50")
    with model_col4:
        st.metric("Screening Threshold", "0.45")

    if not FINAL_THRESHOLD_RESULTS_PATH.exists():
        st.error(
            "The final threshold-results file could not be found at: "
            f"`{FINAL_THRESHOLD_RESULTS_PATH}`"
        )
        return

    try:
        final_results = load_final_threshold_results(
            str(FINAL_THRESHOLD_RESULTS_PATH)
        )

        st.subheader("Final Untouched Test-Set Results")
        st.dataframe(
            final_results,
            hide_index=True,
            width="stretch",
            column_config={
                column: st.column_config.NumberColumn(
                    column,
                    format="%.2f",
                )
                for column in [
                    "Threshold",
                    "Accuracy (%)",
                    "Balanced Accuracy (%)",
                    "Precision (%)",
                    "Recall (%)",
                    "Specificity (%)",
                    "F1 Score (%)",
                    "ROC-AUC (%)",
                    "PR-AUC (%)",
                ]
            },
        )

        main_row = find_threshold_row(final_results, 0.50)
        recall_row = find_threshold_row(final_results, 0.45)

        st.subheader("Threshold Interpretation")
        threshold_col1, threshold_col2 = st.columns(2)

        with threshold_col1:
            st.markdown("#### Main Balanced Threshold — 0.50")
            st.markdown(
                f"""
                - Accuracy: **{metric_value(main_row, 'Accuracy (%)')}**
                - Recall: **{metric_value(main_row, 'Recall (%)')}**
                - Specificity: **{metric_value(main_row, 'Specificity (%)')}**
                - Readmissions caught: **{integer_value(main_row, 'Readmissions Caught')}**
                - Readmissions missed: **{integer_value(main_row, 'Readmissions Missed')}**
                - False positives: **{integer_value(main_row, 'False Positives')}**
                """
            )

        with threshold_col2:
            st.markdown("#### Recall-Focused Threshold — 0.45")
            st.markdown(
                f"""
                - Accuracy: **{metric_value(recall_row, 'Accuracy (%)')}**
                - Recall: **{metric_value(recall_row, 'Recall (%)')}**
                - Specificity: **{metric_value(recall_row, 'Specificity (%)')}**
                - Readmissions caught: **{integer_value(recall_row, 'Readmissions Caught')}**
                - Readmissions missed: **{integer_value(recall_row, 'Readmissions Missed')}**
                - False positives: **{integer_value(recall_row, 'False Positives')}**
                """
            )

        if main_row is not None and recall_row is not None:
            additional_caught = int(
                recall_row["Readmissions Caught"]
                - main_row["Readmissions Caught"]
            )
            additional_false_positives = int(
                recall_row["False Positives"]
                - main_row["False Positives"]
            )

            st.warning(
                f"Lowering the threshold from 0.50 to 0.45 caught "
                f"{additional_caught:,} additional readmissions, but it "
                f"also generated {additional_false_positives:,} additional "
                "false-positive alerts."
            )

        st.info(
            "Threshold 0.50 is the main balanced operating point. "
            "Threshold 0.45 is the recall-focused screening option and "
            "flags more encounters for additional review."
        )
        st.caption(
            "Source: outputs/metrics/"
            "notebook_7_final_threshold_comparison_table.csv"
        )

    except Exception as error:
        st.error("The final test-set results could not be loaded.")
        st.exception(error)


def render_saved_figures() -> None:
    st.header("Saved Figures")
    st.write(
        """
        Review approved visualizations from model development, final
        evaluation, and explainability analysis.
        """
    )

    if not FIGURES_DIR.exists():
        st.error(
            "The saved-figures folder could not be found at: "
            f"`{FIGURES_DIR}`"
        )
        return

    available_figures = {}
    missing_figures = []

    for label, information in APPROVED_FIGURES.items():
        path = FIGURES_DIR / information["filename"]
        if path.exists():
            available_figures[label] = {**information, "path": path}
        else:
            missing_figures.append(information["filename"])

    if not available_figures:
        st.error("None of the approved saved figures could be found.")
        return

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Approved Figures Found", len(available_figures))
    with col2:
        st.metric("Missing Approved Figures", len(missing_figures))

    categories = []
    for information in available_figures.values():
        category = information["category"]
        if category not in categories:
            categories.append(category)

    selected_category = st.selectbox(
        "Select an analysis stage",
        options=categories,
        key="figure_category",
    )

    category_figures = {
        label: information
        for label, information in available_figures.items()
        if information["category"] == selected_category
    }

    selected_label = st.selectbox(
        "Select a saved figure",
        options=list(category_figures.keys()),
        key="figure_selection",
    )

    selected_figure = category_figures[selected_label]
    st.subheader(selected_label)
    st.write(selected_figure["description"])
    st.image(
        selected_figure["path"],
        caption=selected_label,
        width="stretch",
    )
    st.caption(
        "Source: outputs/figures/"
        f"{selected_figure['filename']}"
    )

    with st.expander("View all approved figure filenames"):
        for label, information in available_figures.items():
            st.write(f"**{information['category']} — {label}**")
            st.code(information["filename"], language=None)

    if missing_figures:
        with st.expander("View missing approved figures"):
            for filename in missing_figures:
                st.write(f"- `{filename}`")


def render_explainability() -> None:
    st.header("Model Explainability")
    st.write(
        """
        Explainability analysis was completed after final model evaluation.
        The table below presents global model drivers grouped back to the
        original input features.
        """
    )

    st.info(
        "Global importance describes overall model behavior. For an "
        "explanation of a specific uploaded record, use the Patient Risk "
        "Prediction page."
    )

    if not GLOBAL_SHAP_IMPORTANCE_PATH.exists():
        st.error(
            "The grouped SHAP importance file could not be found at: "
            f"`{GLOBAL_SHAP_IMPORTANCE_PATH}`"
        )
        return

    try:
        shap_data = load_global_shap_importance(
            str(GLOBAL_SHAP_IMPORTANCE_PATH)
        )

        top_features = shap_data.head(10).copy()
        display_table = top_features[
            [
                "rank",
                "Feature",
                "total_mean_absolute_shap",
                "mean_shap",
                "number_transformed_features",
            ]
        ].rename(
            columns={
                "rank": "Rank",
                "total_mean_absolute_shap": "Global SHAP Importance",
                "mean_shap": "Average SHAP Direction",
                "number_transformed_features": "Transformed Features",
            }
        )

        st.subheader("Top Global Model Drivers")
        st.dataframe(
            display_table,
            hide_index=True,
            width="stretch",
            column_config={
                "Global SHAP Importance": st.column_config.NumberColumn(
                    "Global SHAP Importance",
                    format="%.4f",
                ),
                "Average SHAP Direction": st.column_config.NumberColumn(
                    "Average SHAP Direction",
                    format="%.4f",
                ),
            },
        )

        top_names = top_features["Feature"].head(5).tolist()
        st.info(
            "The strongest global drivers include: "
            + ", ".join(top_names)
            + ". Their effect for an individual encounter depends on the "
            "specific values entered and the model's interactions."
        )

        st.caption(
            "Source: outputs/metrics/"
            "notebook_8_grouped_original_shap_importance.csv"
        )

    except Exception as error:
        st.error("The explainability results could not be loaded.")
        st.exception(error)


def render_prediction() -> None:
    st.header("Patient Readmission Risk Prediction")
    st.write(
        """
        Upload a CSV containing one or more hospital encounter records.
        The file must contain the 43 predictors required by the finalized
        Tuned XGBoost pipeline.
        """
    )

    st.info(
        "Download the blank template to prepare new records. Use the sample "
        "file to test the workflow without using a real patient record."
    )
    st.warning(
        "This application is an academic decision-support prototype. "
        "Predictions must not replace clinical judgment, medical assessment, "
        "or established hospital procedures."
    )

    download_col1, download_col2 = st.columns(2)

    with download_col1:
        if PATIENT_TEMPLATE_PATH.exists():
            st.download_button(
                "Download Blank CSV Template",
                data=PATIENT_TEMPLATE_PATH.read_bytes(),
                file_name="patient_input_template.csv",
                mime="text/csv",
                use_container_width=True,
            )
        else:
            st.error("The blank patient-input template could not be found.")

    with download_col2:
        if SAMPLE_PATIENT_PATH.exists():
            st.download_button(
                "Download Sample Test CSV",
                data=SAMPLE_PATIENT_PATH.read_bytes(),
                file_name="sample_patient_input.csv",
                mime="text/csv",
                use_container_width=True,
            )
        else:
            st.error("The sample patient-input CSV could not be found.")

    uploaded_file = st.file_uploader(
        "Upload a completed patient CSV",
        type=["csv"],
        accept_multiple_files=False,
        help=(
            "The CSV must contain all 43 required predictor columns and may "
            "contain one or multiple hospital encounter rows."
        ),
    )

    if uploaded_file is None:
        return

    try:
        uploaded_bytes = uploaded_file.getvalue()
        upload_signature = hashlib.sha256(uploaded_bytes).hexdigest()

        if upload_signature != st.session_state.get(
            "patient_upload_signature"
        ):
            st.session_state["patient_upload_signature"] = upload_signature
            st.session_state.pop("batch_prediction_results", None)
            st.session_state.pop("batch_prediction_download", None)
            st.session_state.pop("batch_explanation_results", None)
            st.session_state.pop("batch_explanation_download", None)

        uploaded_data = pd.read_csv(BytesIO(uploaded_bytes))

        st.success(
            f"CSV loaded successfully: {len(uploaded_data):,} record(s) "
            f"and {len(uploaded_data.columns):,} column(s)."
        )

        st.subheader("Uploaded Data Preview")
        st.dataframe(
            uploaded_data.head(10),
            hide_index=True,
            width="stretch",
        )

        if len(uploaded_data.columns) != 43:
            st.warning(
                "The uploaded file does not contain exactly 43 columns. "
                "Generate predictions to receive a detailed validation "
                "message identifying missing or unexpected columns."
            )

        if st.button(
            "Generate Readmission Predictions",
            type="primary",
            use_container_width=True,
        ):
            with st.spinner(
                "Validating the CSV and calculating predictions..."
            ):
                prediction_results = predict_readmission_batch(
                    uploaded_data
                )
                explanation_results = explain_readmission_batch(
                    uploaded_data,
                    top_n=5,
                )

                screening_results = (
                    create_user_friendly_screening_results(
                        prediction_results
                    )
                )

                combined_results = pd.concat(
                    [
                        screening_results.reset_index(drop=True),
                        uploaded_data.reset_index(drop=True),
                    ],
                    axis=1,
                )

                explanation_download = explanation_results[
                    [
                        "Record Number",
                        "Readmission Probability (%)",
                        "Direction",
                        "Factor Rank",
                        "Feature",
                        "Patient Value",
                    ]
                ].copy()

                st.session_state["batch_prediction_results"] = (
                    prediction_results
                )
                st.session_state["batch_prediction_download"] = (
                    combined_results.to_csv(index=False).encode("utf-8")
                )
                st.session_state["batch_explanation_results"] = (
                    explanation_results
                )
                st.session_state["batch_explanation_download"] = (
                    explanation_download.to_csv(index=False).encode("utf-8")
                )

        prediction_results = st.session_state.get(
            "batch_prediction_results"
        )
        downloadable_results = st.session_state.get(
            "batch_prediction_download"
        )
        explanation_results = st.session_state.get(
            "batch_explanation_results"
        )
        downloadable_explanations = st.session_state.get(
            "batch_explanation_download"
        )

        if prediction_results is None:
            return

        st.divider()
        st.subheader("30-Day Readmission Screening Results")

        total_records = len(prediction_results)
        main_high_risk_count = int(
            (
                prediction_results["Main Classification"]
                == "Flagged at Main Threshold"
            ).sum()
        )
        recall_flagged_count = int(
            (
                prediction_results["Recall-Focused Classification"]
                == "Flagged for Screening"
            ).sum()
        )
        average_probability = prediction_results[
            "Readmission Probability (%)"
        ].mean()

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Records Reviewed", f"{total_records:,}")
        with col2:
            st.metric("Standard Review Flags", f"{main_high_risk_count:,}")
        with col3:
            st.metric("Additional Screening Flags", f"{recall_flagged_count:,}")
        with col4:
            st.metric(
                "Average Estimated Readmission Risk",
                f"{average_probability:.2f}%",
            )

        display_results = create_user_friendly_screening_results(
            prediction_results
        )[
            [
                "Record",
                "Estimated 30-Day Readmission Risk (%)",
                "Standard Review Cutoff",
                "Standard Review Result",
                "Additional Screening Cutoff",
                "Additional Screening Result",
            ]
        ].copy()

        display_results[
            "Estimated 30-Day Readmission Risk (%)"
        ] = display_results[
            "Estimated 30-Day Readmission Risk (%)"
        ].round(2)

        st.dataframe(
            display_results,
            hide_index=True,
            width="stretch",
            column_config={
                "Estimated 30-Day Readmission Risk (%)": (
                    st.column_config.NumberColumn(
                        "Estimated 30-Day Readmission Risk (%)",
                        format="%.2f",
                    )
                ),
                "Standard Review Cutoff": (
                    st.column_config.NumberColumn(
                        "Standard Review Cutoff",
                        format="%.2f",
                    )
                ),
                "Additional Screening Cutoff": (
                    st.column_config.NumberColumn(
                        "Additional Screening Cutoff",
                        format="%.2f",
                    )
                ),
            },
        )

        st.caption(
            "The standard review uses a 50% cutoff. Additional screening "
            "uses a lower 45% cutoff, so it identifies more records that "
            "may benefit from follow-up."
        )

        if explanation_results is not None:
            st.divider()
            st.subheader("Why the Model Produced Each Prediction")
            st.write(
                "Select a record to review the strongest factors that moved "
                "its estimated readmission risk higher or lower."
            )
            st.caption(
                "These factors explain the model's calculation. They do not "
                "prove that a factor caused or prevented readmission."
            )

            available_record_numbers = (
                prediction_results["Record Number"]
                .astype(int)
                .tolist()
            )

            selected_record_number = st.selectbox(
                "Select a record to explain",
                options=available_record_numbers,
                format_func=lambda record: f"Record {record}",
                key="prediction_explanation_record",
            )

            selected_prediction = prediction_results[
                prediction_results["Record Number"]
                == selected_record_number
            ].iloc[0]

            selected_explanation = explanation_results[
                explanation_results["Record Number"]
                == selected_record_number
            ].copy()

            explanation_col1, explanation_col2, explanation_col3 = (
                st.columns(3)
            )
            with explanation_col1:
                st.metric(
                    "Estimated 30-Day Readmission Risk",
                    (
                        f"{selected_prediction['Readmission Probability (%)']:.2f}%"
                    ),
                )

            with explanation_col2:
                st.markdown("**Standard Review Result**")

                if (
                    selected_prediction["Main Classification"]
                    == "Flagged at Main Threshold"
                ):
                    st.warning("Review Recommended")
                else:
                    st.success("No Standard Review Flag")

            with explanation_col3:
                st.markdown("**Additional Screening Result**")

                if (
                    selected_prediction[
                        "Recall-Focused Classification"
                    ]
                    == "Flagged for Screening"
                ):
                    st.warning("Additional Screening Recommended")
                else:
                    st.success("No Additional Screening Flag")

            increasing_factors = selected_explanation[
                selected_explanation["Direction"]
                == "Increases estimated readmission risk"
            ].sort_values("Factor Rank")

            reducing_factors = selected_explanation[
                selected_explanation["Direction"]
                == "Reduces estimated readmission risk"
            ].sort_values("Factor Rank")

            factors_col1, factors_col2 = st.columns(2)

            with factors_col1:
                st.markdown(
                    "#### Factors increasing the estimated risk"
                )
                if increasing_factors.empty:
                    st.write(
                        "No meaningful increasing factors were identified."
                    )
                else:
                    for _, factor in increasing_factors.iterrows():
                        readable_value = format_patient_value(
                            factor["Original Feature"],
                            factor["Patient Value"],
                        )
                        st.markdown(
                            f"- **{factor['Feature']}**: "
                            f"{readable_value}"
                        )

            with factors_col2:
                st.markdown(
                    "#### Factors reducing the estimated risk"
                )
                if reducing_factors.empty:
                    st.write(
                        "No meaningful reducing factors were identified."
                    )
                else:
                    for _, factor in reducing_factors.iterrows():
                        readable_value = format_patient_value(
                            factor["Original Feature"],
                            factor["Patient Value"],
                        )
                        st.markdown(
                            f"- **{factor['Feature']}**: "
                            f"{readable_value}"
                        )

            st.info(
                "A factor can influence the model differently for another "
                "record because the prediction depends on all entered values "
                "and their interactions."
            )

        download_col1, download_col2 = st.columns(2)

        with download_col1:
            if downloadable_results is not None:
                st.download_button(
                    "Download Screening Results",
                    data=downloadable_results,
                    file_name="hospital_readmission_screening_results.csv",
                    mime="text/csv",
                    type="primary",
                    use_container_width=True,
                )

        with download_col2:
            if downloadable_explanations is not None:
                st.download_button(
                    "Download Prediction Factors",
                    data=downloadable_explanations,
                    file_name="hospital_readmission_prediction_factors.csv",
                    mime="text/csv",
                    use_container_width=True,
                )

    except pd.errors.EmptyDataError:
        st.error("The uploaded CSV is empty or contains no readable data.")
    except pd.errors.ParserError:
        st.error(
            "The uploaded file could not be parsed as a valid CSV. "
            "Check its formatting and try again."
        )
    except Exception as error:
        st.error("The uploaded CSV could not be processed.")
        st.exception(error)


# ---------------------------------------------------------
# Sidebar navigation
# ---------------------------------------------------------
with st.sidebar:
    st.title("Project Navigation")

    selected_page = st.radio(
        "Go to",
        options=[
            "Project Overview",
            "Dataset Summary",
            "Model Development",
            "Final Evaluation",
            "Saved Figures",
            "Model Explainability",
            "Patient Risk Prediction",
        ],
        label_visibility="collapsed",
    )

    st.divider()
    st.success(
        "Project completed. Tuned XGBoost is the finalized prediction model."
    )
    st.caption("Main threshold: 0.50")
    st.caption("Recall-focused threshold: 0.45")


# ---------------------------------------------------------
# Main page heading and selected section
# ---------------------------------------------------------
st.title("🏥 Hospital Readmission Risk Prediction")
st.subheader("ASDS 6306 Capstone Project")

if selected_page == "Project Overview":
    render_project_overview()
elif selected_page == "Dataset Summary":
    render_dataset_summary()
elif selected_page == "Model Development":
    render_model_development()
elif selected_page == "Final Evaluation":
    render_final_evaluation()
elif selected_page == "Saved Figures":
    render_saved_figures()
elif selected_page == "Model Explainability":
    render_explainability()
elif selected_page == "Patient Risk Prediction":
    render_prediction()

st.divider()
st.caption(
    "Academic decision-support prototype. The model output is not a medical "
    "diagnosis and must not be used as the sole basis for patient-care "
    "decisions."
)
