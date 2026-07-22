from pathlib import Path
import json

import joblib

# This import allows the old notebook-created preprocessor to load.
from custom_transformers import RareCategoryGrouper


PROJECT_ROOT = Path(__file__).resolve().parent

SOURCE_PREPROCESSOR = (
    PROJECT_ROOT
    / "models"
    / "notebook_4_fitted_preprocessor.joblib"
)

SOURCE_MODEL = (
    PROJECT_ROOT
    / "models"
    / "notebook_6_best_tuned_xgboost.joblib"
)

FINAL_PREPROCESSOR = (
    PROJECT_ROOT
    / "models"
    / "final_preprocessor.joblib"
)

FINAL_MODEL = (
    PROJECT_ROOT
    / "models"
    / "final_xgboost_model.joblib"
)

DEPLOYMENT_CONFIG = (
    PROJECT_ROOT
    / "artifacts"
    / "final_deployment_config.json"
)


def main() -> None:
    """Create clean deployment copies of the final project assets."""

    if not SOURCE_PREPROCESSOR.exists():
        raise FileNotFoundError(
            f"Preprocessor not found: {SOURCE_PREPROCESSOR}"
        )

    if not SOURCE_MODEL.exists():
        raise FileNotFoundError(
            f"Final model not found: {SOURCE_MODEL}"
        )

    preprocessor = joblib.load(SOURCE_PREPROCESSOR)
    model = joblib.load(SOURCE_MODEL)

    raw_feature_count = getattr(
        preprocessor,
        "n_features_in_",
        None,
    )

    transformed_feature_count = getattr(
        model,
        "n_features_in_",
        None,
    )

    if raw_feature_count != 43:
        raise ValueError(
            f"Expected 43 raw features, found {raw_feature_count}."
        )

    if transformed_feature_count != 179:
        raise ValueError(
            "Expected 179 transformed features, "
            f"found {transformed_feature_count}."
        )

    if not hasattr(model, "predict_proba"):
        raise ValueError(
            "The final model does not support probability prediction."
        )

    # Re-saving the preprocessor records RareCategoryGrouper
    # under custom_transformers.py instead of the notebook session.
    joblib.dump(
        preprocessor,
        FINAL_PREPROCESSOR,
    )

    joblib.dump(
        model,
        FINAL_MODEL,
    )

    raw_feature_names = [
        str(feature)
        for feature in getattr(
            preprocessor,
            "feature_names_in_",
            [],
        )
    ]

    deployment_config = {
        "project_status": "completed",
        "final_model_name": "Tuned XGBoost",
        "final_model_file": str(
            FINAL_MODEL.relative_to(PROJECT_ROOT)
        ),
        "final_preprocessor_file": str(
            FINAL_PREPROCESSOR.relative_to(PROJECT_ROOT)
        ),
        "main_threshold": 0.50,
        "recall_focused_threshold": 0.45,
        "raw_feature_count": raw_feature_count,
        "transformed_feature_count": transformed_feature_count,
        "raw_feature_names": raw_feature_names,
        "prediction_target": "readmitted_30",
        "positive_class": 1,
    }

    with open(
        DEPLOYMENT_CONFIG,
        "w",
        encoding="utf-8",
    ) as config_file:
        json.dump(
            deployment_config,
            config_file,
            indent=2,
        )

    print("Deployment assets created successfully.")
    print(f"Final preprocessor: {FINAL_PREPROCESSOR}")
    print(f"Final model: {FINAL_MODEL}")
    print(f"Deployment config: {DEPLOYMENT_CONFIG}")
    print(f"Raw features: {raw_feature_count}")
    print(f"Transformed features: {transformed_feature_count}")


if __name__ == "__main__":
    main()
    