from pathlib import Path
import json

import joblib
import pandas as pd

from custom_transformers import RareCategoryGrouper


PROJECT_ROOT = Path(__file__).resolve().parent

PREPROCESSOR_PATH = (
    PROJECT_ROOT
    / "models"
    / "final_preprocessor.joblib"
)

DATASET_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "diabetic_modeling_data_final.csv"
)

OUTPUT_PATH = (
    PROJECT_ROOT
    / "artifacts"
    / "streamlit_input_schema.json"
)


def convert_number(value):
    """Convert NumPy or pandas numeric values to normal Python numbers."""

    numeric_value = float(value)

    if numeric_value.is_integer():
        return int(numeric_value)

    return round(numeric_value, 4)


def main() -> None:
    """Create the patient-input configuration used by Streamlit."""

    if not PREPROCESSOR_PATH.exists():
        raise FileNotFoundError(
            f"Final preprocessor not found: {PREPROCESSOR_PATH}"
        )

    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Cleaned modeling dataset not found: {DATASET_PATH}"
        )

    preprocessor = joblib.load(PREPROCESSOR_PATH)

    feature_names = [
        str(feature)
        for feature in preprocessor.feature_names_in_
    ]

    if len(feature_names) != 43:
        raise ValueError(
            f"Expected 43 raw predictors, found {len(feature_names)}."
        )

    numeric_features = []
    categorical_features = []

    for transformer_name, transformer, columns in preprocessor.transformers_:
        column_names = [
            str(column)
            for column in columns
        ]

        if transformer_name == "numeric":
            numeric_features.extend(column_names)

        elif transformer_name == "categorical":
            categorical_features.extend(column_names)

    if len(numeric_features) != 8:
        raise ValueError(
            f"Expected 8 numeric predictors, found {len(numeric_features)}."
        )

    if len(categorical_features) != 35:
        raise ValueError(
            "Expected 35 categorical predictors, "
            f"found {len(categorical_features)}."
        )

    input_data = pd.read_csv(
        DATASET_PATH,
        usecols=feature_names,
    )

    numeric_schema = {}

    for feature in numeric_features:
        values = pd.to_numeric(
            input_data[feature],
            errors="coerce",
        ).dropna()

        if values.empty:
            raise ValueError(
                f"No usable numeric values found for {feature}."
            )

        numeric_schema[feature] = {
            "minimum": convert_number(values.min()),
            "maximum": convert_number(values.max()),
            "default": convert_number(values.median()),
            "step": 1,
        }

    categorical_schema = {}

    for feature in categorical_features:
        values = (
            input_data[feature]
            .dropna()
            .astype(str)
            .str.strip()
        )

        values = values[
            (values != "")
            & (values.str.lower() != "nan")
        ]

        if values.empty:
            raise ValueError(
                f"No usable categorical values found for {feature}."
            )

        category_counts = values.value_counts()

        categorical_schema[feature] = {
            "options": sorted(
                category_counts.index.tolist()
            ),
            "default": str(category_counts.index[0]),
        }

    schema = {
        "schema_version": 1,
        "model_name": "Tuned XGBoost",
        "prediction_target": "readmitted_30",
        "positive_class": 1,
        "main_threshold": 0.50,
        "recall_focused_threshold": 0.45,
        "feature_count": len(feature_names),
        "numeric_feature_count": len(numeric_features),
        "categorical_feature_count": len(categorical_features),
        "feature_order": feature_names,
        "numeric_features": numeric_schema,
        "categorical_features": categorical_schema,
    }

    with open(
        OUTPUT_PATH,
        "w",
        encoding="utf-8",
    ) as output_file:
        json.dump(
            schema,
            output_file,
            indent=2,
        )

    print("Streamlit input schema created successfully.")
    print(f"Output: {OUTPUT_PATH}")
    print(f"Total predictors: {len(feature_names)}")
    print(f"Numeric predictors: {len(numeric_features)}")
    print(f"Categorical predictors: {len(categorical_features)}")


if __name__ == "__main__":
    main()
    