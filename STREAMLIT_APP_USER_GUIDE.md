# Streamlit Application User Guide

## Hospital Readmission Risk Prediction

This guide explains how to review the completed capstone dashboard and run the CSV-based prediction workflow.

> **Academic-use notice:** This application is a decision-support prototype. It does not provide a medical diagnosis and must not be used as the sole basis for patient-care decisions. Use only synthetic or properly de-identified records.

---

## 1. Open the Application

Open the deployed Streamlit link in a web browser.

The left sidebar contains the main navigation:

- **Project Overview**
- **Dataset Summary**
- **Model Development**
- **Final Evaluation**
- **Saved Figures**
- **Model Explainability**
- **Patient Risk Prediction**

---

## 2. Review the Project

### Project Overview

Shows the completed workflow, final model, and the two operating thresholds:

- Main threshold: **0.50**
- Recall-focused threshold: **0.45**

### Dataset Summary

Shows:

- 99,343 hospital encounters
- 69,990 unique patients
- 43 modeling predictors
- 11.39% 30-day readmission rate

### Model Development

Displays development and validation results used to compare baseline, candidate, tuned, and threshold configurations.

### Final Evaluation

Displays the one-time untouched test-set results for the finalized Tuned XGBoost model.

### Saved Figures

Use the two dropdown menus to select an analysis stage and a saved visualization.

### Model Explainability

Shows the strongest global model drivers based on grouped SHAP importance. Global importance describes overall model behavior and does not explain a newly uploaded record by itself.

---

## 3. Run a Prediction

1. Select **Patient Risk Prediction** from the sidebar.
2. Download either:
   - **Blank CSV Template** for preparing new records, or
   - **Sample Test CSV** for demonstration.
3. Upload the completed CSV.
4. Confirm that the application reports the expected number of rows and **43 columns**.
5. Review the uploaded-data preview.
6. Select **Generate Readmission Predictions**.
7. Review the probability and threshold classifications.
8. Select **Download Prediction Results** to save the output.

The application supports one record or multiple records in the same CSV.

---

## 4. Interpret the Results

### Readmission Probability

The probability is the model-estimated likelihood of readmission within 30 days.

### Main Threshold: 0.50

- **Flagged at Main Threshold:** Probability is at least 0.50.
- **Not Flagged at Main Threshold:** Probability is below 0.50.

This is the main balanced operating point.

### Recall-Focused Threshold: 0.45

- **Flagged for Screening:** Probability is at least 0.45.
- **Not Flagged:** Probability is below 0.45.

This threshold identifies more possible readmissions but also produces more false-positive alerts.

A record can be below the 0.50 threshold and still be flagged at 0.45. This is expected because the thresholds represent different operating priorities.

---

## 5. Downloaded Prediction File

The downloaded output contains:

- Record number
- Readmission probability
- Readmission probability percentage
- Main threshold
- Main classification
- Recall-focused threshold
- Recall-focused classification
- All 43 original input fields

---

## 6. Suggested Demonstration Sequence

A short demonstration can follow this order:

1. Open **Project Overview** and identify the final model.
2. Open **Final Evaluation** and compare thresholds 0.50 and 0.45.
3. Open **Model Explainability** and identify the strongest global drivers.
4. Open **Patient Risk Prediction**.
5. Upload the three-record sample CSV.
6. Generate predictions.
7. Explain why the two threshold classifications may differ.
8. Download the prediction results.

---

## 7. Troubleshooting

### The file is rejected

Confirm that the CSV:

- contains exactly the required 43 predictor columns
- uses the same column names as the template
- does not contain duplicate columns
- contains no blank required values
- does not include identifiers or the target variable

### The application does not open

Confirm that the deployment is active and refresh the page.

### The prediction page reports a missing model or artifact

Confirm that the final model, preprocessor, schema, and required output files were committed to the GitHub repository.

---

## Final Reminder

The application demonstrates a complete machine-learning workflow, including leakage-safe patient-level splitting, imbalanced-class evaluation, threshold analysis, final test evaluation, explainability, and deployment. Model outputs should be interpreted as screening support rather than clinical conclusions.
