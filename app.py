from __future__ import annotations

from io import BytesIO
from pathlib import Path
import hashlib

import altair as alt
import pandas as pd
import streamlit as st

from prediction_service import (
    build_default_input,
    explain_readmission_batch,
    load_input_schema,
    predict_readmission,
    predict_readmission_batch,
    validate_batch_input,
)

from ui.form_config import (
    ADDITIONAL_MEDICATION_FIELDS,
    FORM_STEPS,
    PRIMARY_DIABETES_FIELDS,
    get_feature_help,
    get_feature_label,
    get_option_label,
    validate_form_configuration,
)
from ui.components import (
    render_factor_panel,
    render_info_card,
    render_key_message,
    render_metric_card,
    render_page_hero,
    render_probability_scale,
    render_screening_status_card,
    render_threshold_card,
    render_three_step_workflow,
)
from ui.styles import apply_global_styles


# ---------------------------------------------------------
# Streamlit page configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Hospital Readmission Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_global_styles()


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
# Guided single-patient form foundation
# ---------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_guided_form_schema() -> dict:
    """Load and validate the schema used by the direct-entry form."""

    schema = load_input_schema()
    validation = validate_form_configuration(schema["feature_order"])

    configuration_errors = {
        key: value
        for key, value in validation.items()
        if value
    }

    if configuration_errors:
        raise ValueError(
            "The guided form configuration does not match the "
            f"deployment schema: {configuration_errors}"
        )

    return schema


def initialize_single_patient_state() -> None:
    """Create persistent state for the guided direct-entry workflow."""

    if "single_patient_values" not in st.session_state:
        st.session_state["single_patient_values"] = build_default_input()

    if "single_patient_form_step" not in st.session_state:
        st.session_state["single_patient_form_step"] = 0

    if "single_prediction_result" not in st.session_state:
        st.session_state["single_prediction_result"] = None

    if "single_explanation_result" not in st.session_state:
        st.session_state["single_explanation_result"] = None


def clear_single_patient_widget_state() -> None:
    """Remove widget keys used by the guided patient form."""

    widget_keys = [
        key
        for key in st.session_state
        if str(key).startswith("single_input_")
    ]

    for key in widget_keys:
        st.session_state.pop(key, None)


def invalidate_single_patient_results() -> None:
    """Clear saved results whenever a direct-entry value changes."""

    st.session_state["single_prediction_result"] = None
    st.session_state["single_explanation_result"] = None
    st.session_state.pop("single_screening_download", None)
    st.session_state.pop("single_explanation_download", None)


def reset_single_patient_form() -> None:
    """Restore schema defaults and return to the first form step."""

    st.session_state["single_patient_values"] = build_default_input()
    st.session_state["single_patient_form_step"] = 0
    invalidate_single_patient_results()
    clear_single_patient_widget_state()


def load_sample_record_into_form() -> None:
    """Load the first validated synthetic sample into the guided form."""

    if not SAMPLE_PATIENT_PATH.exists():
        st.session_state["sample_load_error"] = (
            f"Sample file not found: {SAMPLE_PATIENT_PATH}"
        )
        return

    try:
        sample_data = pd.read_csv(SAMPLE_PATIENT_PATH)
        validated_sample = validate_batch_input(sample_data)

        schema = load_guided_form_schema()
        first_record = {
            feature: validated_sample.iloc[0][feature]
            for feature in schema["feature_order"]
        }

        st.session_state["single_patient_values"] = first_record
        st.session_state["single_patient_form_step"] = len(FORM_STEPS)
        invalidate_single_patient_results()
        clear_single_patient_widget_state()

        st.session_state["prediction_input_mode"] = "Enter One Patient"
        st.session_state["sample_load_success"] = True
        st.session_state.pop("sample_load_error", None)

    except Exception as error:
        st.session_state["sample_load_error"] = str(error)


def render_single_patient_progress(current_step: int) -> None:
    """Display the current position in the five-step workflow."""

    step_titles = [
        "Patient Profile",
        "Hospital Encounter",
        "Healthcare Use",
        "Diabetes Management",
        "Review",
    ]

    st.progress(
        (current_step + 1) / len(step_titles),
        text=f"Step {current_step + 1} of {len(step_titles)}",
    )

    progress_columns = st.columns(len(step_titles))

    for index, title in enumerate(step_titles):
        with progress_columns[index]:
            if index < current_step:
                st.markdown(f"✅ **{index + 1}. {title}**")
            elif index == current_step:
                st.markdown(f"🔷 **{index + 1}. {title}**")
            else:
                st.caption(f"{index + 1}. {title}")


def render_single_input_field(
    feature: str,
    schema: dict,
) -> None:
    """Render one schema-controlled patient input widget."""

    patient_values = st.session_state["single_patient_values"]
    widget_key = f"single_input_{feature}"
    field_label = get_feature_label(feature)
    field_help = get_feature_help(feature)

    if feature in schema["numeric_features"]:
        settings = schema["numeric_features"][feature]

        if widget_key not in st.session_state:
            st.session_state[widget_key] = patient_values.get(
                feature,
                settings["default"],
            )

        entered_value = st.number_input(
            field_label,
            min_value=settings["minimum"],
            max_value=settings["maximum"],
            step=settings["step"],
            key=widget_key,
            help=field_help,
            on_change=invalidate_single_patient_results,
        )

        patient_values[feature] = entered_value
        return

    settings = schema["categorical_features"][feature]
    options = settings["options"]

    current_value = str(
        patient_values.get(feature, settings["default"])
    )

    if current_value not in options:
        current_value = str(settings["default"])

    if widget_key not in st.session_state:
        st.session_state[widget_key] = current_value

    selected_value = st.selectbox(
        field_label,
        options=options,
        key=widget_key,
        help=field_help,
        format_func=lambda value, current_feature=feature: (
            get_option_label(current_feature, value)
        ),
        on_change=invalidate_single_patient_results,
    )

    patient_values[feature] = selected_value


def render_field_grid(
    features: list[str],
    schema: dict,
    column_count: int = 3,
) -> None:
    """Render several input fields in a responsive column grid."""

    columns = st.columns(column_count)

    for index, feature in enumerate(features):
        with columns[index % column_count]:
            render_single_input_field(feature, schema)


def render_diabetes_management_fields(schema: dict) -> None:
    """Render primary diabetes inputs and detailed medication fields."""

    st.markdown("#### Diabetes Tests and Treatment")
    render_field_grid(
        PRIMARY_DIABETES_FIELDS,
        schema,
        column_count=3,
    )

    with st.expander(
        "Additional Diabetes Medication Details",
        expanded=False,
    ):
        st.caption(
            "Review each medication. Status options describe whether the "
            "medication was not prescribed, remained steady, increased, "
            "or decreased."
        )
        render_field_grid(
            ADDITIONAL_MEDICATION_FIELDS,
            schema,
            column_count=3,
        )


def readable_form_value(
    feature: str,
    value,
    schema: dict,
) -> str:
    """Return a readable form value for the review screen."""

    if feature in schema["categorical_features"]:
        return get_option_label(feature, value)

    if feature == "time_in_hospital":
        return f"{value} day(s)"

    return str(value)


def render_single_patient_review(schema: dict) -> None:
    """Display all entered values before prediction."""

    patient_values = st.session_state["single_patient_values"]

    st.subheader("Review Entered Information")
    st.write(
        "Confirm the information below before calculating the "
        "30-day readmission-risk estimate."
    )

    for section in FORM_STEPS:
        st.markdown(f"#### {section['title']}")

        review_rows = [
            {
                "Field": get_feature_label(feature),
                "Entered Value": readable_form_value(
                    feature,
                    patient_values[feature],
                    schema,
                ),
            }
            for feature in section["fields"]
        ]

        st.dataframe(
            pd.DataFrame(review_rows),
            hide_index=True,
            width="stretch",
        )

    st.warning(
        "This is an academic decision-support prototype. Confirm that all "
        "values are correct and appropriately de-identified."
    )


def calculate_single_patient_results(schema: dict) -> None:
    """Calculate and store a direct-entry prediction and explanation."""

    patient_values = {
        feature: st.session_state["single_patient_values"][feature]
        for feature in schema["feature_order"]
    }

    prediction_result = predict_readmission(patient_values)

    input_dataframe = pd.DataFrame(
        [patient_values],
        columns=schema["feature_order"],
    )

    explanation_result = explain_readmission_batch(
        input_dataframe,
        top_n=5,
    )

    standard_result = (
        "Review Recommended"
        if prediction_result["main_threshold_prediction"] == 1
        else "Standard Review Not Triggered"
    )

    additional_result = (
        "Additional Screening Recommended"
        if prediction_result["recall_focused_prediction"] == 1
        else "No Additional Screening Flag"
    )

    screening_row = {
        "Estimated 30-Day Readmission Risk (%)": round(
            prediction_result["probability_percentage"],
            4,
        ),
        "Standard Review Cutoff": prediction_result["main_threshold"],
        "Standard Review Result": standard_result,
        "Additional Screening Cutoff": (
            prediction_result["recall_focused_threshold"]
        ),
        "Additional Screening Result": additional_result,
        **patient_values,
    }

    explanation_download = explanation_result[
        [
            "Record Number",
            "Readmission Probability (%)",
            "Direction",
            "Factor Rank",
            "Feature",
            "Patient Value",
            "Original Feature",
        ]
    ].copy()

    st.session_state["single_prediction_result"] = prediction_result
    st.session_state["single_explanation_result"] = explanation_result
    st.session_state["single_screening_download"] = (
        pd.DataFrame([screening_row])
        .to_csv(index=False)
        .encode("utf-8")
    )
    st.session_state["single_explanation_download"] = (
        explanation_download
        .to_csv(index=False)
        .encode("utf-8")
    )


def render_single_patient_results(schema: dict) -> None:
    """Display a polished direct-entry prediction result."""

    prediction_result = st.session_state.get(
        "single_prediction_result"
    )
    explanation_result = st.session_state.get(
        "single_explanation_result"
    )

    if prediction_result is None or explanation_result is None:
        return

    probability_percentage = float(
        prediction_result["probability_percentage"]
    )

    standard_flagged = (
        prediction_result["main_threshold_prediction"] == 1
    )
    additional_flagged = (
        prediction_result["recall_focused_prediction"] == 1
    )

    st.divider()
    st.markdown(
        '<div class="hr-section-title">'
        '30-Day Readmission Screening Result'
        '</div>',
        unsafe_allow_html=True,
    )

    result_col1, result_col2 = st.columns(2)

    with result_col1:
        render_screening_status_card(
            "Standard Review Result",
            (
                "Review Recommended"
                if standard_flagged
                else "Standard Review Not Triggered"
            ),
            note=(
                "Uses the finalized 50% standard-review cutoff."
            ),
            tone="amber" if standard_flagged else "green",
            icon="!" if standard_flagged else "✓",
        )

    with result_col2:
        render_screening_status_card(
            "Additional Screening Result",
            (
                "Additional Screening Recommended"
                if additional_flagged
                else "No Additional Screening Flag"
            ),
            note=(
                "Uses the lower 45% recall-focused screening cutoff."
            ),
            tone="blue" if additional_flagged else "green",
            icon="+" if additional_flagged else "✓",
        )

    render_probability_scale(
        probability_percentage,
        additional_cutoff=45.0,
        standard_cutoff=50.0,
    )

    st.markdown(
        '<div class="hr-section-title">'
        'Why the Model Produced This Result'
        '</div>',
        unsafe_allow_html=True,
    )
    st.caption(
        "These factors explain the model calculation for this record. "
        "They do not prove that a factor caused or prevented readmission."
    )

    increasing_factors = explanation_result[
        explanation_result["Direction"]
        == "Increases estimated readmission risk"
    ].sort_values("Factor Rank")

    reducing_factors = explanation_result[
        explanation_result["Direction"]
        == "Reduces estimated readmission risk"
    ].sort_values("Factor Rank")

    increasing_items = []
    for _, factor in increasing_factors.iterrows():
        feature = factor["Original Feature"]
        value = readable_form_value(
            feature,
            factor["Patient Value"],
            schema,
        )
        increasing_items.append(
            (str(factor["Feature"]), value)
        )

    reducing_items = []
    for _, factor in reducing_factors.iterrows():
        feature = factor["Original Feature"]
        value = readable_form_value(
            feature,
            factor["Patient Value"],
            schema,
        )
        reducing_items.append(
            (str(factor["Feature"]), value)
        )

    factor_col1, factor_col2 = st.columns(2)

    with factor_col1:
        render_factor_panel(
            "Factors increasing the estimated risk",
            increasing_items,
            direction="increasing",
        )

    with factor_col2:
        render_factor_panel(
            "Factors reducing the estimated risk",
            reducing_items,
            direction="reducing",
        )

    render_key_message(
        "Interpret factors in context",
        (
            "A factor can influence another record differently because "
            "the prediction depends on all entered values and their "
            "interactions."
        ),
        icon="i",
        tone="blue",
    )

    download_col1, download_col2 = st.columns(2)

    with download_col1:
        screening_download = st.session_state.get(
            "single_screening_download"
        )
        if screening_download is not None:
            st.download_button(
                "Download Screening Result",
                data=screening_download,
                file_name=(
                    "single_patient_readmission_screening_result.csv"
                ),
                mime="text/csv",
                type="primary",
                use_container_width=True,
            )

    with download_col2:
        explanation_download = st.session_state.get(
            "single_explanation_download"
        )
        if explanation_download is not None:
            st.download_button(
                "Download Prediction Factors",
                data=explanation_download,
                file_name=(
                    "single_patient_readmission_prediction_factors.csv"
                ),
                mime="text/csv",
                use_container_width=True,
            )


def render_single_patient_form() -> None:
    """Render the complete five-step guided patient-entry form."""

    initialize_single_patient_state()
    schema = load_guided_form_schema()

    current_step = int(
        st.session_state.get("single_patient_form_step", 0)
    )
    current_step = max(0, min(current_step, len(FORM_STEPS)))
    st.session_state["single_patient_form_step"] = current_step

    render_single_patient_progress(current_step)
    st.divider()

    if current_step < len(FORM_STEPS):
        section = FORM_STEPS[current_step]

        st.subheader(section["title"])
        st.write(section["description"])

        if section["key"] == "diabetes_management":
            render_diabetes_management_fields(schema)
        else:
            render_field_grid(
                section["fields"],
                schema,
                column_count=3,
            )

        st.caption(
            "Schema defaults are provided for convenience. Review every "
            "field before calculating a prediction."
        )

    else:
        render_single_patient_review(schema)

    st.divider()

    navigation_col1, navigation_col2, navigation_col3 = st.columns(
        [1, 1, 1]
    )

    with navigation_col1:
        if st.button(
            "← Previous",
            disabled=current_step == 0,
            use_container_width=True,
            key="single_form_previous",
        ):
            st.session_state["single_patient_form_step"] = (
                current_step - 1
            )
            st.rerun()

    with navigation_col2:
        st.button(
            "Reset Form",
            use_container_width=True,
            key="single_form_reset",
            on_click=reset_single_patient_form,
        )

    with navigation_col3:
        if current_step < len(FORM_STEPS):
            if st.button(
                "Next →",
                type="primary",
                use_container_width=True,
                key="single_form_next",
            ):
                st.session_state["single_patient_form_step"] = (
                    current_step + 1
                )
                st.rerun()
        else:
            if st.button(
                "Calculate Readmission Risk",
                type="primary",
                use_container_width=True,
                key="single_form_calculate",
            ):
                try:
                    with st.spinner(
                        "Calculating the readmission-risk estimate..."
                    ):
                        calculate_single_patient_results(schema)
                except Exception as error:
                    st.error(
                        "The direct-entry prediction could not be calculated."
                    )
                    st.exception(error)

    render_single_patient_results(schema)


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
                    "Standard Review Not Triggered"
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
    """Render the redesigned project overview page."""

    render_page_hero(
        "Hospital Readmission Risk Prediction",
        (
            "Identify hospital encounters that may benefit from additional "
            "follow-up review using a finalized machine-learning screening "
            "pipeline and record-level explanations."
        ),
        icon="🏥",
    )

    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

    with metric_col1:
        render_metric_card(
            "Historical Encounters",
            "99,343",
            note="Cleaned modeling dataset",
            icon="▦",
        )

    with metric_col2:
        render_metric_card(
            "Unique Patients",
            "69,990",
            note="Patient-level grouping retained",
            icon="◎",
        )

    with metric_col3:
        render_metric_card(
            "30-Day Readmission Rate",
            "11.39%",
            note="Positive target class",
            icon="↗",
        )

    with metric_col4:
        render_metric_card(
            "Final Model",
            "Tuned XGBoost",
            note="43 raw predictors",
            icon="◆",
        )

    st.markdown(
        '<div class="hr-section-title">How the application works</div>',
        unsafe_allow_html=True,
    )
    render_three_step_workflow()

    info_col1, info_col2, info_col3 = st.columns(3)

    with info_col1:
        render_info_card(
            "Business Problem",
            (
                "Hospital readmissions can increase healthcare costs and "
                "may indicate that some patients need additional follow-up "
                "after discharge. Earlier screening can support prioritizing "
                "post-discharge review resources."
            ),
            icon="▥",
        )

    with info_col2:
        render_info_card(
            "Prediction Target",
            (
                "The target is readmitted_30. A value of 1 represents "
                "readmission within 30 days; a value of 0 represents no "
                "readmission within 30 days."
            ),
            icon="◎",
        )

    with info_col3:
        render_info_card(
            "Modeling Priority",
            (
                "Recall was prioritized because missing a true readmission "
                "is important in a screening context. Precision, specificity, "
                "PR-AUC, ROC-AUC, false positives, and false negatives were "
                "considered together."
            ),
            icon="♟",
        )

    st.markdown(
        '<div class="hr-section-title">Final operating points</div>',
        unsafe_allow_html=True,
    )

    threshold_col1, threshold_col2 = st.columns(2)

    with threshold_col1:
        st.info(
            "**Standard review cutoff — 0.50**  \n"
            "Main balanced operating point for routine review."
        )

    with threshold_col2:
        st.warning(
            "**Additional screening cutoff — 0.45**  \n"
            "Lower cutoff designed to identify more encounters for review."
        )

    st.caption(
        "The application is an academic decision-support prototype. "
        "Predictions are not diagnoses and must not replace clinical judgment."
    )


def render_dataset_summary() -> None:
    """Render the redesigned dataset summary page."""

    render_page_hero(
        "Dataset Summary",
        (
            "Review the cleaned modeling population, target balance, "
            "predictor count, and identifier-handling decisions used by "
            "the finalized readmission-risk pipeline."
        ),
        eyebrow="Data Foundation",
        icon="▦",
    )

    if not DATASET_PATH.exists():
        st.error(
            "The cleaned modeling dataset could not be found at: "
            f"`{DATASET_PATH}`"
        )
        return

    try:
        summary = load_dataset_summary(str(DATASET_PATH))

        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

        with metric_col1:
            render_metric_card(
                "Historical Encounters",
                f"{summary['total_encounters']:,}",
                note="Cleaned hospital encounters",
                icon="▦",
            )

        with metric_col2:
            render_metric_card(
                "Unique Patients",
                (
                    f"{summary['unique_patients']:,}"
                    if summary["unique_patients"] is not None
                    else "Unavailable"
                ),
                note="Used for patient-level grouping",
                icon="◎",
            )

        with metric_col3:
            render_metric_card(
                "Modeling Predictors",
                f"{summary['predictor_count']:,}",
                note="8 numeric and 35 categorical",
                icon="◆",
            )

        with metric_col4:
            rate = summary["readmitted_rate"]
            render_metric_card(
                "30-Day Readmission Rate",
                f"{rate:.2f}%" if rate is not None else "Unavailable",
                note="Positive target class",
                icon="↗",
            )

        st.markdown(
            '<div class="hr-section-title">Target class distribution</div>',
            unsafe_allow_html=True,
        )

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
                    "Target": [
                        "Not readmitted within 30 days",
                        "Readmitted within 30 days",
                    ],
                    "Encounters": [
                        summary["not_readmitted_count"],
                        summary["readmitted_count"],
                    ],
                    "Percentage": [
                        (summary["not_readmitted_count"] / total) * 100,
                        (summary["readmitted_count"] / total) * 100,
                    ],
                }
            )

            chart_col, table_col = st.columns([1.05, 1])

            with chart_col:
                with st.container(border=True):
                    st.markdown("#### Class balance")
                    target_chart_data = class_distribution.copy()
                    target_chart_data["Target Label"] = [
                        "Not readmitted",
                        "Readmitted within 30 days",
                    ]

                    base_chart = (
                        alt.Chart(target_chart_data)
                        .encode(
                            y=alt.Y(
                                "Target Label:N",
                                title=None,
                                sort=[
                                    "Not readmitted",
                                    "Readmitted within 30 days",
                                ],
                                axis=alt.Axis(
                                    labelLimit=230,
                                    labelPadding=8,
                                ),
                            ),
                            x=alt.X(
                                "Encounters:Q",
                                title="Number of encounters",
                                scale=alt.Scale(
                                    domain=[0, 95000],
                                    nice=False,
                                ),
                                axis=alt.Axis(
                                    values=[
                                        0,
                                        10000,
                                        20000,
                                        30000,
                                        40000,
                                        50000,
                                        60000,
                                        70000,
                                        80000,
                                        90000,
                                    ],
                                    labelExpr=(
                                        "datum.value === 0 ? '0' : "
                                        "(datum.value / 1000) + ',000'"
                                    ),
                                    labelFlush=False,
                                ),
                            ),
                            tooltip=[
                                alt.Tooltip(
                                    "Target Label:N",
                                    title="Target",
                                ),
                                alt.Tooltip(
                                    "Encounters:Q",
                                    title="Encounters",
                                    format=",",
                                ),
                                alt.Tooltip(
                                    "Percentage:Q",
                                    title="Percentage",
                                    format=".2f",
                                ),
                            ],
                        )
                    )

                    target_bars = base_chart.mark_bar(
                        cornerRadiusTopRight=6,
                        cornerRadiusBottomRight=6,
                    ).encode(
                        color=alt.Color(
                            "Target Label:N",
                            legend=None,
                            scale=alt.Scale(
                                domain=[
                                    "Not readmitted",
                                    "Readmitted within 30 days",
                                ],
                                range=[
                                    "#2878D0",
                                    "#0F8F8D",
                                ],
                            ),
                        ),
                    )

                    target_labels = base_chart.mark_text(
                        align="right",
                        baseline="middle",
                        dx=-10,
                        color="white",
                        fontWeight="bold",
                        fontSize=13,
                    ).encode(
                        text=alt.Text(
                            "Encounters:Q",
                            format=",",
                        )
                    )

                    target_chart = (
                        target_bars
                        + target_labels
                    ).properties(
                        height=260,
                    )

                    st.altair_chart(
                        target_chart,
                        use_container_width=True,
                    )

                    st.caption(
                        "The positive class represents 11.39% of encounters, "
                        "so accuracy alone is not sufficient for evaluation."
                    )

            with table_col:
                with st.container(border=True):
                    st.markdown("#### Distribution details")
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

                    render_key_message(
                        "Why patient-level grouping matters",
                        (
                            "The same patient must not appear in both model "
                            "development and evaluation groups because that "
                            "would create data leakage and overstate performance."
                        ),
                        icon="i",
                        tone="blue",
                    )

        info_col1, info_col2 = st.columns(2)

        with info_col1:
            render_info_card(
                "Identifiers",
                (
                    "encounter_id is retained only for encounter tracking. "
                    "patient_nbr is retained only for patient-level splitting "
                    "and grouping. Neither identifier is used as a predictor."
                ),
                icon="#",
            )

        with info_col2:
            render_info_card(
                "Cleaned modeling table",
                (
                    f"The final table contains {summary['total_columns']} "
                    "columns, no missing values in the audited modeling data, "
                    "and the binary target readmitted_30."
                ),
                icon="✓",
            )

        st.caption(
            "Source: data/processed/diabetic_modeling_data_final.csv"
        )

    except Exception as error:
        st.error("The dataset summary could not be calculated.")
        st.exception(error)


def render_model_development() -> None:
    """Render the redesigned model-development page."""

    render_page_hero(
        "Model Development",
        (
            "Compare baseline, candidate, tuned, and threshold-analysis "
            "configurations used to select the finalized Tuned XGBoost model."
        ),
        eyebrow="Model Selection",
        icon="◫",
    )

    if not MODEL_COMPARISON_PATH.exists():
        st.error(
            "The model-comparison file could not be found at: "
            f"`{MODEL_COMPARISON_PATH}`"
        )
        return

    try:
        comparison = load_model_comparison(str(MODEL_COMPARISON_PATH))

        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

        with metric_col1:
            render_metric_card(
                "Configurations Compared",
                f"{len(comparison):,}",
                note="Development-stage evaluations",
                icon="▤",
            )

        with metric_col2:
            render_metric_card(
                "Highest Development Recall",
                f"{comparison['Recall (%)'].max():.2f}%",
                note="Not selected using recall alone",
                icon="↗",
            )

        with metric_col3:
            render_metric_card(
                "Highest Development Accuracy",
                f"{comparison['Accuracy (%)'].max():.2f}%",
                note="Accuracy interpreted cautiously",
                icon="◎",
            )

        with metric_col4:
            render_metric_card(
                "Final Model",
                "Tuned XGBoost",
                note="Selected for overall balance and PR-AUC",
                icon="◆",
            )

        render_key_message(
            "Selection principle",
            (
                "The strongest recall and strongest accuracy came from "
                "different configurations. Final selection considered "
                "recall, precision, specificity, balanced accuracy, F1, "
                "ROC-AUC, PR-AUC, false positives, and false negatives."
            ),
            icon="i",
            tone="teal",
        )

        tab1, tab2, tab3 = st.tabs(
            [
                "Key Metrics",
                "Confusion Counts",
                "Modeling Notes",
            ]
        )

        with tab1:
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
                column: st.column_config.NumberColumn(
                    column,
                    format="%.2f",
                )
                for column in key_columns
                if column not in ["Analysis Stage", "Model"]
            }

            st.dataframe(
                comparison[key_columns],
                hide_index=True,
                width="stretch",
                height=590,
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

        with tab2:
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
                height=520,
            )

        with tab3:
            note_col1, note_col2, note_col3 = st.columns(3)

            with note_col1:
                render_info_card(
                    "Baseline stage",
                    (
                        "Dummy and baseline models established reference "
                        "performance and demonstrated that majority-class "
                        "accuracy was not clinically useful."
                    ),
                    icon="1",
                )

            with note_col2:
                render_info_card(
                    "Candidate and tuning stage",
                    (
                        "Logistic regression, tree-based ensembles, boosting "
                        "models, and class-imbalance strategies were compared "
                        "using validation metrics."
                    ),
                    icon="2",
                )

            with note_col3:
                render_info_card(
                    "Threshold stage",
                    (
                        "The finalized model was evaluated at multiple "
                        "operating thresholds to balance additional recall "
                        "against increased false-positive review volume."
                    ),
                    icon="3",
                )

        st.caption(
            "Source: outputs/metrics/"
            "dynamic_all_model_comparison_summary.csv"
        )

    except Exception as error:
        st.error("The development comparison table could not be loaded.")
        st.exception(error)


def render_final_evaluation() -> None:
    """Render the redesigned final evaluation page."""

    render_page_hero(
        "Final Model Evaluation",
        (
            "Review the one-time untouched test-set performance of the "
            "finalized Tuned XGBoost model at the two selected screening "
            "cutoffs."
        ),
        eyebrow="Untouched Test Set",
        icon="✓",
    )

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

        main_row = find_threshold_row(final_results, 0.50)
        recall_row = find_threshold_row(final_results, 0.45)

        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

        with metric_col1:
            render_metric_card(
                "Final Model",
                "Tuned XGBoost",
                note="One-time untouched test evaluation",
                icon="◆",
            )

        with metric_col2:
            render_metric_card(
                "Test Encounters",
                "14,976",
                note="Previously unseen patient groups",
                icon="▦",
            )

        with metric_col3:
            render_metric_card(
                "ROC-AUC",
                "66.39%",
                note="Threshold-independent discrimination",
                icon="↗",
            )

        with metric_col4:
            render_metric_card(
                "PR-AUC",
                "22.38%",
                note="Important for the imbalanced target",
                icon="◎",
            )

        st.markdown(
            '<div class="hr-section-title">Final threshold comparison</div>',
            unsafe_allow_html=True,
        )

        threshold_col1, threshold_col2 = st.columns(2)

        with threshold_col1:
            render_threshold_card(
                "Standard review cutoff",
                "0.50",
                recall=metric_value(main_row, "Recall (%)"),
                precision=metric_value(main_row, "Precision (%)"),
                specificity=metric_value(main_row, "Specificity (%)"),
                caught=integer_value(main_row, "Readmissions Caught"),
                missed=integer_value(main_row, "Readmissions Missed"),
                false_positives=integer_value(main_row, "False Positives"),
                tone="teal",
            )

        with threshold_col2:
            render_threshold_card(
                "Additional screening cutoff",
                "0.45",
                recall=metric_value(recall_row, "Recall (%)"),
                precision=metric_value(recall_row, "Precision (%)"),
                specificity=metric_value(recall_row, "Specificity (%)"),
                caught=integer_value(recall_row, "Readmissions Caught"),
                missed=integer_value(recall_row, "Readmissions Missed"),
                false_positives=integer_value(recall_row, "False Positives"),
                tone="blue",
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

            render_key_message(
                "Operational trade-off",
                (
                    f"Lowering the cutoff from 0.50 to 0.45 caught "
                    f"{additional_caught:,} additional readmissions but "
                    f"generated {additional_false_positives:,} additional "
                    "false-positive review alerts."
                ),
                icon="!",
                tone="amber",
            )

        with st.expander("View complete untouched test-set table"):
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

        st.caption(
            "Source: outputs/metrics/"
            "notebook_7_final_threshold_comparison_table.csv"
        )

    except Exception as error:
        st.error("The final test-set results could not be loaded.")
        st.exception(error)


def render_saved_figures() -> None:
    """Render the redesigned saved-figures gallery."""

    render_page_hero(
        "Saved Figures",
        (
            "Browse approved visualizations from baseline modeling, candidate "
            "comparison, threshold analysis, final evaluation, and model "
            "explainability."
        ),
        eyebrow="Visual Evidence",
        icon="▧",
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

    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

    with metric_col1:
        render_metric_card(
            "Approved Figures",
            str(len(available_figures)),
            note="Validated application visuals",
            icon="▧",
        )

    with metric_col2:
        render_metric_card(
            "Missing Figures",
            str(len(missing_figures)),
            note="Expected to remain zero",
            icon="!",
        )

    with metric_col3:
        render_metric_card(
            "Standard Cutoff",
            "0.50",
            note="Balanced operating point",
            icon="◎",
        )

    with metric_col4:
        render_metric_card(
            "Additional Cutoff",
            "0.45",
            note="Recall-focused screening",
            icon="↗",
        )

    categories = []
    for information in available_figures.values():
        category = information["category"]
        if category not in categories:
            categories.append(category)

    filter_col1, filter_col2 = st.columns(2)

    with filter_col1:
        selected_category = st.selectbox(
            "Analysis stage",
            options=categories,
            key="figure_category",
        )

    category_figures = {
        label: information
        for label, information in available_figures.items()
        if information["category"] == selected_category
    }

    with filter_col2:
        selected_label = st.selectbox(
            "Saved figure",
            options=list(category_figures.keys()),
            key="figure_selection",
        )

    selected_figure = category_figures[selected_label]

    with st.container(border=True):
        st.markdown(f"### {selected_label}")
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
    """Render the redesigned explainability page."""

    render_page_hero(
        "Risk Insights",
        (
            "Understand the strongest global drivers of the finalized model "
            "and how those global patterns differ from record-level "
            "prediction explanations."
        ),
        eyebrow="Model Explainability",
        icon="◆",
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

        metric_col1, metric_col2, metric_col3 = st.columns(3)

        with metric_col1:
            render_metric_card(
                "Top Global Driver",
                str(top_features.iloc[0]["Feature"]),
                note="Highest grouped mean absolute SHAP",
                icon="1",
            )

        with metric_col2:
            render_metric_card(
                "Original Predictors",
                "43",
                note="Grouped from transformed features",
                icon="◆",
            )

        with metric_col3:
            render_metric_card(
                "Transformed Features",
                "179",
                note="Used by the final XGBoost model",
                icon="▦",
            )

        render_key_message(
            "Global importance is not causality",
            (
                "A high global SHAP importance means the model relied on a "
                "feature frequently across the evaluation data. It does not "
                "prove that the feature medically caused readmission."
            ),
            icon="i",
            tone="blue",
        )

        chart_col, table_col = st.columns([1, 1.1])

        with chart_col:
            with st.container(border=True):
                st.markdown("#### Top grouped SHAP drivers")
                chart_data = top_features[
                    ["Feature", "total_mean_absolute_shap"]
                ].rename(
                    columns={
                        "total_mean_absolute_shap": (
                            "Global SHAP Importance"
                        )
                    }
                )

                shap_chart = (
                    alt.Chart(chart_data)
                    .mark_bar(
                        color="#0F8F8D",
                        cornerRadiusTopRight=6,
                        cornerRadiusBottomRight=6,
                    )
                    .encode(
                        y=alt.Y(
                            "Feature:N",
                            title=None,
                            sort="-x",
                            axis=alt.Axis(
                                labelLimit=245,
                                labelPadding=8,
                            ),
                        ),
                        x=alt.X(
                            "Global SHAP Importance:Q",
                            title="Mean absolute SHAP value",
                        ),
                        tooltip=[
                            alt.Tooltip(
                                "Feature:N",
                                title="Feature",
                            ),
                            alt.Tooltip(
                                "Global SHAP Importance:Q",
                                title="Global SHAP Importance",
                                format=".4f",
                            ),
                        ],
                    )
                    .properties(height=430)
                )

                st.altair_chart(
                    shap_chart,
                    use_container_width=True,
                )

        with table_col:
            with st.container(border=True):
                st.markdown("#### Global driver details")
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
                        "total_mean_absolute_shap": (
                            "Global SHAP Importance"
                        ),
                        "mean_shap": "Average SHAP Direction",
                        "number_transformed_features": (
                            "Transformed Features"
                        ),
                    }
                )

                st.dataframe(
                    display_table,
                    hide_index=True,
                    width="stretch",
                    height=430,
                    column_config={
                        "Global SHAP Importance": (
                            st.column_config.NumberColumn(
                                "Global SHAP Importance",
                                format="%.4f",
                            )
                        ),
                        "Average SHAP Direction": (
                            st.column_config.NumberColumn(
                                "Average SHAP Direction",
                                format="%.4f",
                            )
                        ),
                    },
                )

        insight_col1, insight_col2 = st.columns(2)

        with insight_col1:
            render_info_card(
                "Global explanation",
                (
                    "Summarizes the features the model relied on most across "
                    "many encounters. It describes overall model behavior."
                ),
                icon="G",
            )

        with insight_col2:
            render_info_card(
                "Record-level explanation",
                (
                    "Shows the strongest factors increasing or reducing the "
                    "estimated risk for one uploaded or manually entered "
                    "encounter."
                ),
                icon="R",
            )

        st.caption(
            "Source: outputs/metrics/"
            "notebook_8_grouped_original_shap_importance.csv"
        )

    except Exception as error:
        st.error("The explainability results could not be loaded.")
        st.exception(error)

def render_prediction() -> None:
    """Render the prediction page and its available input methods."""

    render_page_hero(
        "New Readmission Assessment",
        (
            "Enter one de-identified encounter, upload multiple records, "
            "or load a synthetic sample. Every method uses the same 43 "
            "predictors and finalized Tuned XGBoost pipeline."
        ),
        icon="✚",
    )

    st.info(
        "Use only synthetic or appropriately de-identified records. "
        "Do not enter patient names, medical record numbers, addresses, "
        "dates of birth, or other direct identifiers."
    )

    input_mode = st.radio(
        "Choose an input method",
        options=[
            "Enter One Patient",
            "Upload Multiple Records",
            "Use Sample Record",
        ],
        horizontal=True,
        key="prediction_input_mode",
    )

    st.divider()

    if input_mode == "Enter One Patient":
        st.subheader("Enter One Patient")

        if st.session_state.pop("sample_load_success", False):
            st.success(
                "Synthetic sample loaded successfully. Review the values "
                "below, then calculate the readmission-risk estimate."
            )

        st.write(
            """
            Complete the guided workflow to enter one de-identified
            hospital encounter, review all values, and calculate a
            30-day readmission-risk estimate.
            """
        )
        render_single_patient_form()

    elif input_mode == "Upload Multiple Records":
        render_batch_prediction()

    elif input_mode == "Use Sample Record":
        initialize_single_patient_state()
        schema = load_guided_form_schema()

        st.subheader("Use a Synthetic Sample Record")
        st.write(
            """
            Load a synthetic demonstration record into the guided form,
            review all 43 values, and calculate a prediction without using
            real patient information.
            """
        )

        sample_col1, sample_col2 = st.columns(2)
        with sample_col1:
            st.metric("Sample Predictors", schema["feature_count"])
        with sample_col2:
            st.metric("Sample Type", "Synthetic")

        if SAMPLE_PATIENT_PATH.exists():
            try:
                sample_data = pd.read_csv(SAMPLE_PATIENT_PATH)
                validated_sample = validate_batch_input(sample_data)

                st.success(
                    f"Sample file validated: "
                    f"{len(validated_sample):,} record(s) and "
                    f"{len(validated_sample.columns):,} columns."
                )

                preview_record = validated_sample.head(1).copy()
                preview_record.columns = [
                    get_feature_label(column)
                    for column in preview_record.columns
                ]

                with st.expander(
                    "Preview the synthetic sample values",
                    expanded=False,
                ):
                    st.dataframe(
                        preview_record,
                        hide_index=True,
                        width="stretch",
                    )

                st.button(
                    "Load Sample and Review",
                    type="primary",
                    use_container_width=True,
                    on_click=load_sample_record_into_form,
                    key="load_sample_record_button",
                )

                st.caption(
                    "After loading, the app opens Step 5 so you can review "
                    "the sample before calculating its readmission-risk "
                    "estimate."
                )

            except Exception as error:
                st.error(
                    "The synthetic sample record could not be validated."
                )
                st.exception(error)
        else:
            st.error(
                "The synthetic sample file could not be found at: "
                f"`{SAMPLE_PATIENT_PATH}`"
            )

        sample_error = st.session_state.pop(
            "sample_load_error",
            None,
        )
        if sample_error:
            st.error(
                "The sample could not be loaded into the guided form: "
                f"{sample_error}"
            )


def render_batch_prediction() -> None:
    """Render the existing CSV batch-prediction workflow."""

    st.subheader("Upload Multiple Records")
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
            render_metric_card(
                "Records Reviewed",
                f"{total_records:,}",
                note="Validated uploaded encounters",
                icon="▦",
            )

        with col2:
            render_metric_card(
                "Standard Review Flags",
                f"{main_high_risk_count:,}",
                note="Probability at or above 50%",
                icon="!",
            )

        with col3:
            render_metric_card(
                "Additional Screening Flags",
                f"{recall_flagged_count:,}",
                note="Probability at or above 45%",
                icon="+",
            )

        with col4:
            render_metric_card(
                "Average Estimated Risk",
                f"{average_probability:.2f}%",
                note="Mean across uploaded records",
                icon="◎",
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

            selected_probability = float(
                selected_prediction["Readmission Probability (%)"]
            )
            selected_standard_flagged = (
                selected_prediction["Main Classification"]
                == "Flagged at Main Threshold"
            )
            selected_additional_flagged = (
                selected_prediction[
                    "Recall-Focused Classification"
                ]
                == "Flagged for Screening"
            )

            explanation_col1, explanation_col2 = st.columns(2)

            with explanation_col1:
                render_screening_status_card(
                    "Standard Review Result",
                    (
                        "Review Recommended"
                        if selected_standard_flagged
                        else "Standard Review Not Triggered"
                    ),
                    note="Uses the finalized 50% cutoff.",
                    tone=(
                        "amber"
                        if selected_standard_flagged
                        else "green"
                    ),
                    icon="!" if selected_standard_flagged else "✓",
                )

            with explanation_col2:
                render_screening_status_card(
                    "Additional Screening Result",
                    (
                        "Additional Screening Recommended"
                        if selected_additional_flagged
                        else "No Additional Screening Flag"
                    ),
                    note="Uses the lower 45% cutoff.",
                    tone=(
                        "blue"
                        if selected_additional_flagged
                        else "green"
                    ),
                    icon="+" if selected_additional_flagged else "✓",
                )

            render_probability_scale(
                selected_probability,
                additional_cutoff=45.0,
                standard_cutoff=50.0,
            )

            increasing_factors = selected_explanation[
                selected_explanation["Direction"]
                == "Increases estimated readmission risk"
            ].sort_values("Factor Rank")

            reducing_factors = selected_explanation[
                selected_explanation["Direction"]
                == "Reduces estimated readmission risk"
            ].sort_values("Factor Rank")

            increasing_items = [
                (
                    str(factor["Feature"]),
                    format_patient_value(
                        factor["Original Feature"],
                        factor["Patient Value"],
                    ),
                )
                for _, factor in increasing_factors.iterrows()
            ]

            reducing_items = [
                (
                    str(factor["Feature"]),
                    format_patient_value(
                        factor["Original Feature"],
                        factor["Patient Value"],
                    ),
                )
                for _, factor in reducing_factors.iterrows()
            ]

            factors_col1, factors_col2 = st.columns(2)

            with factors_col1:
                render_factor_panel(
                    "Factors increasing the estimated risk",
                    increasing_items,
                    direction="increasing",
                )

            with factors_col2:
                render_factor_panel(
                    "Factors reducing the estimated risk",
                    reducing_items,
                    direction="reducing",
                )

            render_key_message(
                "Interpret factors in context",
                (
                    "A factor can influence another record differently "
                    "because the prediction depends on all entered values "
                    "and their interactions."
                ),
                icon="i",
                tone="blue",
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
    st.markdown(
        """
        <div class="hr-sidebar-brand">
            <div class="hr-sidebar-logo">✚</div>
            <div>
                <div class="hr-sidebar-title">Readmission Risk Portal</div>
                <div class="hr-sidebar-subtitle">ASDS 6306 Capstone</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    selected_page = st.radio(
        "Go to",
        options=[
            "Overview",
            "Data Explorer",
            "Model Development",
            "Model Performance",
            "Saved Figures",
            "Risk Insights",
            "New Prediction",
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
if selected_page == "Overview":
    render_project_overview()
elif selected_page == "Data Explorer":
    render_dataset_summary()
elif selected_page == "Model Development":
    render_model_development()
elif selected_page == "Model Performance":
    render_final_evaluation()
elif selected_page == "Saved Figures":
    render_saved_figures()
elif selected_page == "Risk Insights":
    render_explainability()
elif selected_page == "New Prediction":
    render_prediction()

st.divider()
st.caption(
    "Academic decision-support prototype. The model output is not a medical "
    "diagnosis and must not be used as the sole basis for patient-care "
    "decisions."
)
