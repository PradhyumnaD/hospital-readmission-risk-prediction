from functools import lru_cache
from pathlib import Path
import json
from typing import Any

import joblib
import pandas as pd

# Required when loading the saved preprocessor.
from custom_transformers import RareCategoryGrouper


PROJECT_ROOT = Path(__file__).resolve().parent

PREPROCESSOR_PATH = (
    PROJECT_ROOT
    / "models"
    / "final_preprocessor.joblib"
)

MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "final_xgboost_model.joblib"
)

INPUT_SCHEMA_PATH = (
    PROJECT_ROOT
    / "artifacts"
    / "streamlit_input_schema.json"
)


@lru_cache(maxsize=1)
def load_input_schema() -> dict:
    """Load the Streamlit patient-input configuration."""

    if not INPUT_SCHEMA_PATH.exists():
        raise FileNotFoundError(
            f"Input schema not found: {INPUT_SCHEMA_PATH}"
        )

    with open(
        INPUT_SCHEMA_PATH,
        "r",
        encoding="utf-8",
    ) as schema_file:
        schema = json.load(schema_file)

    if schema.get("feature_count") != 43:
        raise ValueError(
            "The input schema must contain exactly 43 predictors."
        )

    return schema


@lru_cache(maxsize=1)
def load_prediction_assets():
    """Load the final preprocessor and Tuned XGBoost model."""

    if not PREPROCESSOR_PATH.exists():
        raise FileNotFoundError(
            f"Final preprocessor not found: {PREPROCESSOR_PATH}"
        )

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Final model not found: {MODEL_PATH}"
        )

    preprocessor = joblib.load(PREPROCESSOR_PATH)
    model = joblib.load(MODEL_PATH)

    if getattr(preprocessor, "n_features_in_", None) != 43:
        raise ValueError(
            "The final preprocessor does not expect 43 raw features."
        )

    if getattr(model, "n_features_in_", None) != 179:
        raise ValueError(
            "The final model does not expect 179 transformed features."
        )

    if not hasattr(model, "predict_proba"):
        raise ValueError(
            "The final model does not support predict_proba()."
        )

    return preprocessor, model


def build_default_input() -> dict[str, Any]:
    """
    Create a test record using numeric medians and categorical modes
    stored in the input schema.

    This is only for verifying the deployment pipeline.
    """

    schema = load_input_schema()
    default_values = {}

    for feature, settings in schema["numeric_features"].items():
        default_values[feature] = settings["default"]

    for feature, settings in schema["categorical_features"].items():
        default_values[feature] = settings["default"]

    return default_values


def create_input_dataframe(
    input_values: dict[str, Any],
) -> pd.DataFrame:
    """Validate and arrange the 43 predictors in the required order."""

    schema = load_input_schema()
    feature_order = schema["feature_order"]

    missing_features = [
        feature
        for feature in feature_order
        if feature not in input_values
    ]

    unexpected_features = [
        feature
        for feature in input_values
        if feature not in feature_order
    ]

    if missing_features:
        raise ValueError(
            "Missing required predictors: "
            + ", ".join(missing_features)
        )

    if unexpected_features:
        raise ValueError(
            "Unexpected predictors received: "
            + ", ".join(unexpected_features)
        )

    ordered_values = {
        feature: input_values[feature]
        for feature in feature_order
    }

    input_dataframe = pd.DataFrame(
        [ordered_values],
        columns=feature_order,
    )

    for feature in schema["numeric_features"]:
        input_dataframe[feature] = pd.to_numeric(
            input_dataframe[feature],
            errors="raise",
        )

    for feature in schema["categorical_features"]:
        input_dataframe[feature] = (
            input_dataframe[feature]
            .astype(str)
        )

    return input_dataframe


def predict_readmission(
    input_values: dict[str, Any],
) -> dict[str, Any]:
    """
    Generate the 30-day readmission probability and threshold results.
    """

    schema = load_input_schema()
    preprocessor, model = load_prediction_assets()

    input_dataframe = create_input_dataframe(
        input_values
    )

    transformed_input = preprocessor.transform(
        input_dataframe
    )

    if transformed_input.shape[1] != 179:
        raise ValueError(
            "Preprocessing did not produce the expected "
            "179 transformed features."
        )

    probability = float(
        model.predict_proba(transformed_input)[0, 1]
    )

    main_threshold = float(
        schema["main_threshold"]
    )

    recall_threshold = float(
        schema["recall_focused_threshold"]
    )

    return {
        "probability": probability,
        "probability_percentage": probability * 100,
        "main_threshold": main_threshold,
        "main_threshold_prediction": int(
            probability >= main_threshold
        ),
        "recall_focused_threshold": recall_threshold,
        "recall_focused_prediction": int(
            probability >= recall_threshold
        ),
    }

def validate_batch_input(
    input_dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Validate a CSV containing one or more patient encounter records.
    """

    if not isinstance(input_dataframe, pd.DataFrame):
        raise TypeError(
            "The uploaded input must be a pandas DataFrame."
        )

    if input_dataframe.empty:
        raise ValueError(
            "The uploaded CSV does not contain any patient records."
        )

    schema = load_input_schema()
    feature_order = schema["feature_order"]

    validated_data = input_dataframe.copy()

    # Remove accidental spaces around column names.
    validated_data.columns = [
        str(column).strip()
        for column in validated_data.columns
    ]

    duplicated_columns = (
        validated_data.columns[
            validated_data.columns.duplicated()
        ].tolist()
    )

    if duplicated_columns:
        raise ValueError(
            "Duplicate columns found: "
            + ", ".join(duplicated_columns)
        )

    missing_columns = [
        feature
        for feature in feature_order
        if feature not in validated_data.columns
    ]

    unexpected_columns = [
        column
        for column in validated_data.columns
        if column not in feature_order
    ]

    if missing_columns:
        raise ValueError(
            "The CSV is missing required columns: "
            + ", ".join(missing_columns)
        )

    if unexpected_columns:
        raise ValueError(
            "The CSV contains unexpected columns: "
            + ", ".join(unexpected_columns)
        )

    # Put the predictors in the exact order required by the preprocessor.
    validated_data = validated_data[
        feature_order
    ].copy()

    # Validate numeric predictors.
    for feature, settings in schema["numeric_features"].items():
        validated_data[feature] = pd.to_numeric(
            validated_data[feature],
            errors="coerce",
        )

        if validated_data[feature].isna().any():
            invalid_rows = (
                validated_data.index[
                    validated_data[feature].isna()
                ]
                + 2
            ).tolist()

            raise ValueError(
                f"Invalid or missing numeric value in '{feature}' "
                f"at CSV row(s): {invalid_rows}"
            )

        minimum = settings["minimum"]
        maximum = settings["maximum"]

        outside_range = (
            (validated_data[feature] < minimum)
            | (validated_data[feature] > maximum)
        )

        if outside_range.any():
            invalid_rows = (
                validated_data.index[outside_range]
                + 2
            ).tolist()

            raise ValueError(
                f"Values in '{feature}' must be between "
                f"{minimum} and {maximum}. "
                f"Check CSV row(s): {invalid_rows}"
            )

    # Validate categorical predictors.
    for feature in schema["categorical_features"]:
        validated_data[feature] = (
            validated_data[feature]
            .astype("string")
            .str.strip()
        )

        invalid_values = (
            validated_data[feature].isna()
            | validated_data[feature].isin(
                ["", "nan", "None", "<NA>"]
            )
        )

        if invalid_values.any():
            invalid_rows = (
                validated_data.index[invalid_values]
                + 2
            ).tolist()

            raise ValueError(
                f"Missing categorical value in '{feature}' "
                f"at CSV row(s): {invalid_rows}"
            )

        validated_data[feature] = (
            validated_data[feature].astype(str)
        )

    return validated_data


def predict_readmission_batch(
    input_dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """
    Generate readmission-risk predictions for one or more CSV records.
    """

    schema = load_input_schema()
    preprocessor, model = load_prediction_assets()

    validated_data = validate_batch_input(
        input_dataframe
    )

    transformed_data = preprocessor.transform(
        validated_data
    )

    if transformed_data.shape[1] != 179:
        raise ValueError(
            "Preprocessing did not produce the expected "
            "179 transformed features."
        )

    probabilities = model.predict_proba(
        transformed_data
    )[:, 1]

    main_threshold = float(
        schema["main_threshold"]
    )

    recall_threshold = float(
        schema["recall_focused_threshold"]
    )

    main_predictions = (
        probabilities >= main_threshold
    ).astype(int)

    recall_predictions = (
        probabilities >= recall_threshold
    ).astype(int)

    results = pd.DataFrame(
        {
            "Record Number": range(
                1,
                len(validated_data) + 1,
            ),
            "Readmission Probability": probabilities,
            "Readmission Probability (%)": (
                probabilities * 100
            ),
            "Main Threshold": main_threshold,
            "Main Classification": [
                (
                    "Higher Readmission Risk"
                    if prediction == 1
                    else "Lower Readmission Risk"
                )
                for prediction in main_predictions
            ],
            "Recall-Focused Threshold": recall_threshold,
            "Recall-Focused Classification": [
                (
                    "Flagged for Screening"
                    if prediction == 1
                    else "Not Flagged"
                )
                for prediction in recall_predictions
            ],
        }
    )

    return results