from __future__ import annotations

from typing import Any


# ------------------------------------------------------------------
# Guided form organization
# ------------------------------------------------------------------
FORM_STEPS = [
    {
        "key": "patient_profile",
        "title": "Patient Profile",
        "description": "Enter the patient demographic information.",
        "fields": [
            "race",
            "gender",
            "age",
        ],
    },
    {
        "key": "hospital_encounter",
        "title": "Hospital Encounter",
        "description": (
            "Enter information about the current hospital stay, "
            "diagnoses, and discharge."
        ),
        "fields": [
            "admission_type_group",
            "admission_source_group",
            "discharge_disposition_id",
            "medical_specialty_group",
            "time_in_hospital",
            "num_lab_procedures",
            "num_procedures",
            "num_medications",
            "number_diagnoses",
            "diag_1_group",
            "diag_2_group",
            "diag_3_group",
        ],
    },
    {
        "key": "previous_healthcare_use",
        "title": "Previous Healthcare Use",
        "description": (
            "Enter prior outpatient, emergency, and inpatient utilization."
        ),
        "fields": [
            "number_outpatient",
            "number_emergency",
            "number_inpatient",
        ],
    },
    {
        "key": "diabetes_management",
        "title": "Diabetes Management",
        "description": (
            "Enter diabetes test results and medication information."
        ),
        "fields": [
            "max_glu_serum",
            "A1Cresult",
            "change",
            "diabetesMed",
            "insulin",
            "metformin",
            "repaglinide",
            "nateglinide",
            "chlorpropamide",
            "glimepiride",
            "acetohexamide",
            "glipizide",
            "glyburide",
            "tolbutamide",
            "pioglitazone",
            "rosiglitazone",
            "acarbose",
            "miglitol",
            "troglitazone",
            "tolazamide",
            "glyburide-metformin",
            "glipizide-metformin",
            "glimepiride-pioglitazone",
            "metformin-rosiglitazone",
            "metformin-pioglitazone",
        ],
    },
]

PRIMARY_DIABETES_FIELDS = [
    "max_glu_serum",
    "A1Cresult",
    "change",
    "diabetesMed",
    "insulin",
]

ADDITIONAL_MEDICATION_FIELDS = [
    "metformin",
    "repaglinide",
    "nateglinide",
    "chlorpropamide",
    "glimepiride",
    "acetohexamide",
    "glipizide",
    "glyburide",
    "tolbutamide",
    "pioglitazone",
    "rosiglitazone",
    "acarbose",
    "miglitol",
    "troglitazone",
    "tolazamide",
    "glyburide-metformin",
    "glipizide-metformin",
    "glimepiride-pioglitazone",
    "metformin-rosiglitazone",
    "metformin-pioglitazone",
]


# ------------------------------------------------------------------
# User-friendly field labels
# ------------------------------------------------------------------
FIELD_LABELS = {
    "time_in_hospital": "Time in Hospital (days)",
    "num_lab_procedures": "Laboratory Procedures",
    "num_procedures": "Non-Laboratory Procedures",
    "num_medications": "Number of Medications",
    "number_outpatient": "Previous Outpatient Visits",
    "number_emergency": "Previous Emergency Visits",
    "number_inpatient": "Previous Inpatient Visits",
    "number_diagnoses": "Number of Diagnoses",
    "race": "Race / Ethnicity",
    "gender": "Gender",
    "age": "Age Group",
    "discharge_disposition_id": "Discharge Disposition",
    "max_glu_serum": "Maximum Glucose Serum Result",
    "A1Cresult": "A1C Test Result",
    "metformin": "Metformin",
    "repaglinide": "Repaglinide",
    "nateglinide": "Nateglinide",
    "chlorpropamide": "Chlorpropamide",
    "glimepiride": "Glimepiride",
    "acetohexamide": "Acetohexamide",
    "glipizide": "Glipizide",
    "glyburide": "Glyburide",
    "tolbutamide": "Tolbutamide",
    "pioglitazone": "Pioglitazone",
    "rosiglitazone": "Rosiglitazone",
    "acarbose": "Acarbose",
    "miglitol": "Miglitol",
    "troglitazone": "Troglitazone",
    "tolazamide": "Tolazamide",
    "insulin": "Insulin",
    "glyburide-metformin": "Glyburide–Metformin",
    "glipizide-metformin": "Glipizide–Metformin",
    "glimepiride-pioglitazone": "Glimepiride–Pioglitazone",
    "metformin-rosiglitazone": "Metformin–Rosiglitazone",
    "metformin-pioglitazone": "Metformin–Pioglitazone",
    "change": "Diabetes Medication Change",
    "diabetesMed": "Diabetes Medication Prescribed",
    "admission_source_group": "Admission Source",
    "admission_type_group": "Admission Type",
    "diag_1_group": "Primary Diagnosis Group",
    "diag_2_group": "Secondary Diagnosis Group",
    "diag_3_group": "Additional Diagnosis Group",
    "medical_specialty_group": "Medical Specialty",
}


# ------------------------------------------------------------------
# Help text
# ------------------------------------------------------------------
FIELD_HELP = {
    "time_in_hospital": "Number of days for the current hospital encounter.",
    "num_lab_procedures": (
        "Number of laboratory procedures performed during the encounter."
    ),
    "num_procedures": (
        "Number of non-laboratory procedures performed during the encounter."
    ),
    "num_medications": (
        "Number of distinct medications recorded during the encounter."
    ),
    "number_outpatient": (
        "Number of outpatient visits recorded during the preceding year."
    ),
    "number_emergency": (
        "Number of emergency visits recorded during the preceding year."
    ),
    "number_inpatient": (
        "Number of inpatient visits recorded during the preceding year."
    ),
    "number_diagnoses": (
        "Number of diagnoses recorded for the current encounter."
    ),
    "discharge_disposition_id": (
        "Select where the patient was discharged or transferred."
    ),
    "max_glu_serum": (
        "Maximum glucose serum test result. Select Unknown when the test "
        "was not performed or the result is unavailable."
    ),
    "A1Cresult": (
        "A1C test result. Select Unknown when the test was not performed "
        "or the result is unavailable."
    ),
    "change": (
        "Indicates whether the diabetes medication regimen changed "
        "during the encounter."
    ),
    "diabetesMed": (
        "Indicates whether a diabetes medication was prescribed."
    ),
    "insulin": (
        "Insulin status: not prescribed, steady dose, increased dose, "
        "or decreased dose."
    ),
    "diag_1_group": "Grouped primary diagnosis for the encounter.",
    "diag_2_group": "Grouped secondary diagnosis for the encounter.",
    "diag_3_group": "Grouped additional diagnosis for the encounter.",
    "medical_specialty_group": (
        "Grouped specialty of the admitting or attending clinical service."
    ),
}


# ------------------------------------------------------------------
# Readable option mappings
# ------------------------------------------------------------------
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

AGE_LABELS = {
    "[0-10)": "0–9 years",
    "[10-20)": "10–19 years",
    "[20-30)": "20–29 years",
    "[30-40)": "30–39 years",
    "[40-50)": "40–49 years",
    "[50-60)": "50–59 years",
    "[60-70)": "60–69 years",
    "[70-80)": "70–79 years",
    "[80-90)": "80–89 years",
    "[90-100)": "90–99 years",
}

RACE_LABELS = {
    "AfricanAmerican": "African American",
    "Asian": "Asian",
    "Caucasian": "Caucasian",
    "Hispanic": "Hispanic",
    "Other": "Other",
    "Unknown": "Unknown",
}

GENDER_LABELS = {
    "Female": "Female",
    "Male": "Male",
    "Unknown/Invalid": "Unknown / Invalid",
}

TEST_RESULT_LABELS = {
    ">200": "Above 200",
    ">300": "Above 300",
    ">7": "Above 7%",
    ">8": "Above 8%",
    "Norm": "Normal",
    "Unknown": "Not Measured / Unknown",
}

MEDICATION_STATUS_LABELS = {
    "No": "Not Prescribed",
    "Steady": "Steady Dose",
    "Up": "Dose Increased",
    "Down": "Dose Decreased",
}

MEDICATION_FEATURES = set(ADDITIONAL_MEDICATION_FIELDS + ["insulin"])

OPTION_LABELS = {
    "age": AGE_LABELS,
    "race": RACE_LABELS,
    "gender": GENDER_LABELS,
    "discharge_disposition_id": DISCHARGE_DISPOSITION_LABELS,
    "max_glu_serum": TEST_RESULT_LABELS,
    "A1Cresult": TEST_RESULT_LABELS,
    "change": {
        "Ch": "Medication Changed",
        "No": "No Medication Change",
    },
    "diabetesMed": {
        "Yes": "Yes",
        "No": "No",
    },
    "medical_specialty_group": {
        "Family/GeneralPractice": "Family / General Practice",
        "ObstetricsandGynecology": "Obstetrics and Gynecology",
        "Orthopedics-Reconstructive": "Orthopedics – Reconstructive",
        "Surgery-Cardiovascular/Thoracic": (
            "Cardiovascular / Thoracic Surgery"
        ),
        "Surgery-General": "General Surgery",
        "Surgery-Vascular": "Vascular Surgery",
    },
}


def get_feature_label(feature: str) -> str:
    """Return the user-facing label for a model feature."""

    return FIELD_LABELS.get(
        feature,
        str(feature).replace("_", " ").replace("-", " ").title(),
    )


def get_feature_help(feature: str) -> str | None:
    """Return optional help text for a model feature."""

    return FIELD_HELP.get(feature)


def get_option_label(feature: str, value: Any) -> str:
    """Convert an internal categorical value into readable text."""

    value_text = str(value)

    if feature in MEDICATION_FEATURES:
        return MEDICATION_STATUS_LABELS.get(value_text, value_text)

    feature_mapping = OPTION_LABELS.get(feature, {})
    return feature_mapping.get(value_text, value_text)


def get_all_configured_features() -> list[str]:
    """Return every configured input field exactly once."""

    return [
        feature
        for section in FORM_STEPS
        for feature in section["fields"]
    ]


def validate_form_configuration(
    expected_feature_order: list[str],
) -> dict[str, list[str]]:
    """Compare the form configuration with the deployment schema."""

    configured_features = get_all_configured_features()

    duplicate_features = sorted(
        {
            feature
            for feature in configured_features
            if configured_features.count(feature) > 1
        }
    )

    missing_features = [
        feature
        for feature in expected_feature_order
        if feature not in configured_features
    ]

    unexpected_features = [
        feature
        for feature in configured_features
        if feature not in expected_feature_order
    ]

    return {
        "missing_features": missing_features,
        "unexpected_features": unexpected_features,
        "duplicate_features": duplicate_features,
    }
