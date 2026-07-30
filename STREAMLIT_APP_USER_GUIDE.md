# Streamlit Application User Guide

## Hospital Readmission Risk Prediction

This guide explains how to use the finalized seven-page capstone dashboard, enter one encounter through the guided form, upload multiple CSV records, load a synthetic sample, interpret both screening cutoffs, review record-level explanations, and download results.

> **Academic-use notice:** This application is a decision-support prototype. It does not provide a medical diagnosis and must not be used as the sole basis for patient-care decisions. Use only synthetic or appropriately de-identified records.

## 1. Open the Application

Public deployment:

[Hospital Readmission Risk Prediction](https://hospital-readmission-risk-prediction.streamlit.app/)

The left sidebar contains seven pages:

1. **Overview**
2. **Data Explorer**
3. **Model Development**
4. **Model Performance**
5. **Saved Figures**
6. **Risk Insights**
7. **New Prediction**

## 2. Review the Dashboard Pages

### Overview

Provides the project summary and key validated facts:

- 99,343 historical encounters
- 69,990 unique patients
- 11.39% 30-day readmission rate
- 43 raw predictors
- Tuned XGBoost final model
- standard review cutoff: 0.50
- additional screening cutoff: 0.45

### Data Explorer

Shows:

- target-class distribution
- 88,029 encounters not readmitted within 30 days
- 11,314 encounters readmitted within 30 days
- patient-level grouping and identifier handling
- cleaned modeling-table summary

`encounter_id` is used only for tracking. `patient_nbr` is used only for patient-level grouping. Neither identifier is a model input.

### Model Development

Displays baseline, candidate, tuned, and threshold-analysis configurations evaluated before the final untouched test assessment.

Use this page to compare:

- accuracy
- balanced accuracy
- precision
- recall
- specificity
- F1-score
- ROC-AUC
- PR-AUC
- confusion-matrix counts

### Model Performance

Shows the final Tuned XGBoost results on 14,976 untouched test encounters.

At 0.50:

- recall: 55.54%
- specificity: 66.63%
- readmissions caught: 943
- readmissions missed: 755
- false positives: 4,431

At 0.45:

- recall: 67.20%
- specificity: 54.40%
- readmissions caught: 1,141
- readmissions missed: 557
- false positives: 6,055

Lowering the cutoff caught 198 additional readmissions and generated 1,624 additional false-positive alerts.

### Saved Figures

Select an analysis stage and figure from the dropdown menus. The validated application contains 22 approved figures and no missing files.

### Risk Insights

Shows the strongest global grouped SHAP drivers.

Global importance summarizes model behavior across many encounters. It does not prove that a feature medically caused readmission and does not replace the explanation of an individual record.

### New Prediction

Provides three input methods:

- **Enter One Patient**
- **Upload Multiple Records**
- **Use Sample Record**

Every method uses the same 43 predictors, finalized preprocessor, Tuned XGBoost model, thresholds, and explanation logic.

## 3. Enter One Patient

Select:

```text
New Prediction → Enter One Patient
```

Complete the five-step workflow.

### Step 1 — Patient Profile

Enter:

- Race / Ethnicity
- Gender
- Age Group

### Step 2 — Hospital Encounter

Enter admission, discharge, specialty, utilization during the encounter, and diagnosis-group information.

### Step 3 — Healthcare Use

Enter previous:

- outpatient visits
- emergency visits
- inpatient visits

### Step 4 — Diabetes Management

Enter:

- glucose and A1C testing categories
- medication-change status
- diabetes-medication status
- insulin status
- individual diabetes-medication fields

### Step 5 — Review

Review all 43 values before selecting:

```text
Calculate Readmission Risk
```

Do not enter names, medical record numbers, addresses, dates of birth, or other direct identifiers.

## 4. Upload Multiple Records

Select:

```text
New Prediction → Upload Multiple Records
```

Available downloads:

- **Blank CSV Template**
- **Sample Test CSV**

The blank template contains the required 43 headers and no completed row. The sample contains synthetic demonstration data.

Upload a CSV containing one or more encounter rows. The file must contain all 43 predictors and must not contain:

- `encounter_id`
- `patient_nbr`
- `readmitted_30`

The application validates:

- empty input
- duplicate columns
- missing required columns
- unexpected columns
- invalid numeric text
- missing numeric values
- values outside allowed numeric ranges
- missing or blank categorical values
- final feature order and transformed feature count

After validation, generate predictions and select a record to review its explanation.

## 5. Use the Synthetic Sample

Select:

```text
New Prediction → Use Sample Record
```

Load the sample into the guided form and proceed through the five steps.

The validated sample produces approximately:

```text
Estimated 30-Day Readmission Risk: 46.39%
Standard Review Not Triggered
Additional Screening Recommended
```

The sample is synthetic, contains no real patient information, and is not taken from the final test set.

## 6. Interpret the Screening Result

### Estimated probability

The percentage is the model-estimated probability of readmission within 30 days.

The probability scale displays:

- the current estimate
- the 45% additional-screening cutoff
- the 50% standard-review cutoff

### Standard Review Result — 0.50

Possible results:

```text
Review Recommended
Standard Review Not Triggered
```

### Additional Screening Result — 0.45

Possible results:

```text
Additional Screening Recommended
No Additional Screening Flag
```

A probability between 45% and 50% triggers additional screening but not standard review. This is expected.

## 7. Review the Prediction Factors

Each explained record shows:

- five factors increasing the estimated risk
- five factors reducing the estimated risk

These factors explain the model calculation for that record. They do not prove that a factor caused or prevented readmission.

A feature can influence another record differently because the prediction depends on all values and their interactions.

## 8. Download Results

### Single-patient screening result

Contains:

- 1 row
- 5 screening-result columns
- all 43 entered predictors
- 48 columns total

### Batch screening results

Contains one row per uploaded record and six user-facing columns:

- Record
- Estimated 30-Day Readmission Risk (%)
- Standard Review Cutoff
- Standard Review Result
- Additional Screening Cutoff
- Additional Screening Result

### Prediction factors

Contains:

- record number
- readmission probability
- factor direction
- factor rank
- readable feature
- entered value
- original internal feature name

For each explained record, the file contains five increasing and five reducing factors.

## 9. Suggested Demonstration Sequence

1. Open **Overview** and identify the final model.
2. Open **Data Explorer** and explain the 11.39% positive class.
3. Open **Model Performance** and compare 0.50 with 0.45.
4. Open **Risk Insights** and identify the strongest global drivers.
5. Open **New Prediction**.
6. Select **Use Sample Record**.
7. Review the five guided steps.
8. Calculate the result.
9. Explain why 46.39% triggers additional screening but not standard review.
10. Review increasing and reducing factors.
11. Download the screening result and prediction factors.
12. Demonstrate **Upload Multiple Records** using the sample CSV.

## 10. Troubleshooting

### The CSV is rejected

Confirm that the file:

- contains exactly the required 43 predictor columns
- uses the template column names
- contains no duplicate columns
- contains no blank required values
- contains values within the displayed numeric ranges
- does not include identifiers or the target
- is saved as a readable CSV

### A probability is between the two cutoffs

This is valid. A value from 45% up to, but not including, 50% receives:

```text
Standard Review Not Triggered
Additional Screening Recommended
```

### The application does not open

Refresh the page and confirm that the Streamlit deployment is active.

### The app shows an import or artifact error

Open the Streamlit app management page and review the logs. Confirm that the model, preprocessor, schema, `custom_transformers.py`, `ui/` modules, and required output files are present in the deployed GitHub branch.

### The page looks stale after a GitHub update

Reboot the Streamlit application from the management controls. Dependency changes may require a full rebuild.

## 11. Formal Validation

The final application was validated in:

```text
notebooks/09_streamlit_application_validation.ipynb
```

Final result:

```text
Validation steps completed: 6
Total validation checks: 88
Passed validation checks: 88
Failed validation checks: 0
Overall validation rate: 100.00%
Application pages: 7
Prediction input methods: 3
Approved figures: 22
Invalid-input tests: 18
```

The validation confirmed that direct entry and CSV upload produce identical predictions, threshold decisions, and explanation-factor rankings for identical inputs.

## Final Reminder

The application demonstrates a complete machine-learning workflow including leakage-safe patient-level splitting, imbalanced-class evaluation, threshold analysis, final untouched test evaluation, explainability, guided prediction, CSV prediction, downloadable results, and formal application validation.

Model outputs are screening estimates, not clinical conclusions. Clinical judgment, local validation, privacy controls, security review, and regulatory assessment would be required before any real-world use.
