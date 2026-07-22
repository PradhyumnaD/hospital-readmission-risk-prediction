from pathlib import Path
import json

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent

SCHEMA_PATH = (
    PROJECT_ROOT
    / "artifacts"
    / "streamlit_input_schema.json"
)

TEMPLATE_PATH = (
    PROJECT_ROOT
    / "outputs"
    / "patient_input_template.csv"
)

SAMPLE_PATH = (
    PROJECT_ROOT
    / "outputs"
    / "sample_patient_input.csv"
)


def main() -> None:
    """Create a blank input template and one demonstration record."""

    if not SCHEMA_PATH.exists():
        raise FileNotFoundError(
            f"Input schema not found: {SCHEMA_PATH}"
        )

    with open(
        SCHEMA_PATH,
        "r",
        encoding="utf-8",
    ) as schema_file:
        schema = json.load(schema_file)

    feature_order = schema["feature_order"]

    if len(feature_order) != 43:
        raise ValueError(
            f"Expected 43 predictors, found {len(feature_order)}."
        )

    # Blank CSV with the 43 required column headers.
    template_dataframe = pd.DataFrame(
        columns=feature_order
    )

    template_dataframe.to_csv(
        TEMPLATE_PATH,
        index=False,
    )

    # Demonstration record using schema defaults.
    sample_record = {}

    for feature, settings in schema["numeric_features"].items():
        sample_record[feature] = settings["default"]

    for feature, settings in schema["categorical_features"].items():
        sample_record[feature] = settings["default"]

    sample_dataframe = pd.DataFrame(
        [sample_record],
        columns=feature_order,
    )

    sample_dataframe.to_csv(
        SAMPLE_PATH,
        index=False,
    )

    print("CSV files created successfully.")
    print(f"Template: {TEMPLATE_PATH}")
    print(f"Sample file: {SAMPLE_PATH}")
    print(f"Sample rows: {len(sample_dataframe)}")
    print(f"Input columns: {len(sample_dataframe.columns)}")


if __name__ == "__main__":
    main()