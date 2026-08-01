# AI-Powered Hospital Readmission Risk Prediction

[![Project Status](https://img.shields.io/badge/Status-Completed-brightgreen)](#project-status)
[![Course](https://img.shields.io/badge/Course-ASDS%206306-blue)](#project-overview)
[![Final Model](https://img.shields.io/badge/Final%20Model-Tuned%20XGBoost-orange)](#final-model)
[![Application](https://img.shields.io/badge/Application-Streamlit-ff4b4b)](#streamlit-application)
[![Explainability](https://img.shields.io/badge/Explainability-SHAP-purple)](#model-explainability)

A complete machine-learning capstone project for estimating the probability of **30-day hospital readmission** among patients with diabetes. The project covers data auditing, leakage-safe patient-level splitting, preprocessing, baseline and advanced model comparison, hyperparameter tuning, threshold analysis, final untouched test-set evaluation, explainable AI, and a professional Streamlit application with guided single-record entry, batch CSV prediction, synthetic demonstration data, and record-level explanations.

> **Important:** This repository is an academic decision-support prototype. It is not a medical device, does not provide a diagnosis, and must not be used as the sole basis for patient-care decisions.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Project Status](#project-status)
3. [Key Results](#key-results)
4. [Business Problem](#business-problem)
5. [Dataset](#dataset)
6. [Target Definition](#target-definition)
7. [Methodology](#methodology)
8. [Leakage Prevention](#leakage-prevention)
9. [Preprocessing Pipeline](#preprocessing-pipeline)
10. [Model Development](#model-development)
11. [Final Model](#final-model)
12. [Final Test Results](#final-test-results)
13. [Threshold Strategy](#threshold-strategy)
14. [Model Explainability](#model-explainability)
15. [Streamlit Application](#streamlit-application)
16. [Prediction Workflows](#prediction-workflows)
17. [Installation and Local Execution](#installation-and-local-execution)
18. [Online Deployment](#online-deployment)
19. [Regenerating Deployment Assets](#regenerating-deployment-assets)
20. [Project Structure](#project-structure)
21. [Notebook-by-Notebook Summary](#notebook-by-notebook-summary)
22. [Important Artifacts](#important-artifacts)
23. [Reproducibility and Validation](#reproducibility-and-validation)
24. [Limitations](#limitations)
25. [Responsible Use](#responsible-use)
26. [Future Enhancements](#future-enhancements)
27. [Final Conclusion](#final-conclusion)

## Project Overview

**Course:** ASDS 6306 Capstone  
**Project:** Hospital Readmission Risk Prediction  
**Prediction point:** At or near hospital discharge  
**Prediction target:** Readmission within 30 days  
**Final model:** Tuned XGBoost  
**Application:** Eight-page Streamlit dashboard with a redesigned professional Overview page, guided direct entry, batch CSV upload, synthetic sample workflows, and a formal application-validation dashboard  
**Explainability:** Global grouped SHAP analysis and dynamic record-level prediction explanations  
**Deployed application:** [Hospital Readmission Risk Prediction](https://hospital-readmission-risk-prediction.streamlit.app/)

The project was designed to answer the following question:

> Can routinely available hospital encounter information be used to identify encounters that may require additional post-discharge review because of an elevated model-estimated probability of readmission within 30 days?

The project does not optimize for accuracy alone. Because only about 11% of encounters belong to the positive class, the analysis emphasizes recall, precision, F1-score, balanced accuracy, ROC-AUC, PR-AUC, confusion-matrix counts, and the operational cost of false-positive and false-negative decisions.

## Project Status

| Component | Status |
|---|---|
| Data audit and cleaning | Completed |
| Exploratory data analysis | Completed |
| Patient-level splitting | Completed |
| Preprocessing definition and validation | Completed |
| Baseline model evaluation | Completed |
| Candidate model evaluation | Completed |
| Hyperparameter tuning | Completed |
| Threshold analysis | Completed |
| Final model and threshold selection | Completed |
| Untouched test-set evaluation | Completed |
| Explainable AI analysis | Completed |
| Eight-page Streamlit dashboard | Completed |
| Guided five-step patient-entry form | Completed |
| Batch CSV workflow | Completed |
| Synthetic sample workflow | Completed |
| Dynamic record-level explanations | Completed |
| Comprehensive application validation | Completed — 108 of 108 checks passed |
| Streamlit Community Cloud deployment | Completed |
| GitHub repository | Completed |

## Key Results

- Final cleaned dataset: **99,343 encounters × 46 columns**
- Unique patients: **69,990**
- Positive class rate: **11.39%**
- Modeling predictors: **43**
  - 8 numeric
  - 35 categorical
- Transformed model features: **179**
- Patient overlap across train, validation, and test: **0**
- Final model: **Tuned XGBoost**
- Main operating threshold: **0.50**
- Recall-focused screening threshold: **0.45**
- Final test encounters: **14,976**
- Final test readmissions: **1,698**
- Main threshold recall: **55.54%**
- Recall-focused threshold recall: **67.20%**
- Lowering the threshold from 0.50 to 0.45:
  - caught **198 additional readmissions**
  - reduced false negatives by **198**
  - produced **1,624 additional false-positive alerts**
- Streamlit interface:
  - **8 pages**
  - redesigned professional Overview page
  - hospital and analytics illustration
  - four factual project-summary cards
  - five-stage project pipeline
  - six working Overview navigation actions
  - **3 input methods**
  - **5-step guided form**
  - explicit confirmation before prediction
  - dynamic record-level explanations
  - readable downloadable screening and factor files
  - dedicated Application Validation dashboard
- Notebook 09 application validation:
  - **108 checks**
  - **108 passed**
  - **0 failed**
  - **100.00% pass rate**
  - **22 approved figures found**
  - **18 invalid-input tests passed**

## Business Problem

Hospital readmissions may increase healthcare costs and can indicate that a patient requires additional follow-up, medication review, discharge support, or care coordination.

The objective is not to replace clinical decision-making. The model is intended to support prioritization by estimating readmission probability and flagging encounters for possible additional review.

A useful screening model must balance two competing goals:

1. Detect as many actual readmissions as reasonably possible.
2. Avoid creating an unmanageable number of false-positive alerts.

This trade-off is why the final application presents two operating thresholds rather than a single universal classification rule.

---

## Dataset

**Dataset:** Diabetes 130-US Hospitals for Years 1999–2008  
**Source organization:** UCI Machine Learning Repository  
**Unit of analysis:** One hospital encounter  

### Original data

| Characteristic | Value |
|---|---:|
| Encounters | 101,766 |
| Columns | 50 |
| Unique patients | 71,518 |
| Exact duplicate rows | 0 |
| Maximum encounters for one patient | 40 |

### Final audited modeling data

| Characteristic | Value |
|---|---:|
| Encounters | 99,343 |
| Columns | 46 |
| Unique patients | 69,990 |
| Patients with multiple encounters | 16,341 |
| Missing values | 0 |
| Positive encounters | 11,314 |
| Negative encounters | 88,029 |
| Positive class rate | 11.39% |

### Exclusions

A total of **2,423 encounters** associated with expired or hospice discharge dispositions were removed because they were not suitable candidates for standard 30-day readmission prediction.

The excluded discharge disposition codes were:

- 11: Expired
- 13: Hospice/home
- 14: Hospice/medical facility
- 19: Expired at home
- 20: Expired in a medical facility
- 21: Expired, place unknown

---

## Target Definition

The original `readmitted` field contained:

- `NO`
- `>30`
- `<30`

A binary target named `readmitted_30` was created:

| Original value | Binary target |
|---|---:|
| `<30` | 1 |
| `>30` | 0 |
| `NO` | 0 |

The positive class therefore represents an encounter followed by readmission within 30 days.

The following fields were excluded from model predictors:

- `encounter_id`
- `patient_nbr`
- `readmitted_30`

`encounter_id` is used only for tracking. `patient_nbr` is used only for patient-level grouping and leakage prevention.

---

## Methodology

The end-to-end workflow was:

```text
Raw data
   ↓
Data audit and cleaning
   ↓
Target creation and feature engineering
   ↓
Exploratory data analysis
   ↓
Patient-level train / validation / test split
   ↓
Training-only preprocessing fit
   ↓
Baseline model comparison
   ↓
Candidate and advanced model comparison
   ↓
Hyperparameter tuning
   ↓
Validation-based threshold analysis
   ↓
Final model and threshold selection
   ↓
One-time untouched test evaluation
   ↓
SHAP explainability
   ↓
Guided and CSV Streamlit prediction workflows
   ↓
Comprehensive application validation and deployment
```

### Evaluation priorities

Because of class imbalance, the following metrics were reviewed together:

- Recall / sensitivity
- Precision
- F1-score
- Specificity
- Balanced accuracy
- ROC-AUC
- PR-AUC
- True positives
- False positives
- False negatives
- True negatives

Accuracy was retained as a descriptive metric but was never used alone for model selection.

---

## Leakage Prevention

Repeated encounters from the same patient created a major leakage risk.

### Repeated-patient audit

- Unique patients: **69,990**
- Patients with multiple encounters: **16,341**
- Percentage of patients with repeated encounters: **23.35%**
- Encounters belonging to repeat patients: **45,694**
- Percentage of encounters from repeat patients: **46.00%**
- Maximum encounters for one patient: **40**

A random row-level split could place one encounter from a patient in training and another encounter from the same patient in validation or test. This could produce overly optimistic performance.

### Patient-level split

| Split | Encounters | Patients | Positive cases | Positive rate |
|---|---:|---:|---:|---:|
| Train | 69,467 | 48,993 | 7,936 | 11.424% |
| Validation | 14,900 | 10,498 | 1,680 | 11.275% |
| Test | 14,976 | 10,499 | 1,698 | 11.338% |

### Leakage audit

```text
Train vs. validation patient overlap: 0
Train vs. test patient overlap: 0
Validation vs. test patient overlap: 0
```

The exact split assignments were saved and reused throughout the remaining notebooks. The test set was reserved until the final model and threshold strategy were approved.

---

## Preprocessing Pipeline

### Numeric predictors

The eight numeric predictors are:

- `time_in_hospital`
- `num_lab_procedures`
- `num_procedures`
- `num_medications`
- `number_outpatient`
- `number_emergency`
- `number_inpatient`
- `number_diagnoses`

Numeric preprocessing:

1. Median imputation
2. Standard scaling

### Categorical predictors

Thirty-five categorical predictors were processed using:

1. Most-frequent imputation
2. Conversion to strings for consistent encoding
3. Rare-category grouping
4. One-hot encoding
5. Safe handling of previously unseen categories

### Rare-category rule

```text
Minimum frequency: 10 training observations
```

Rare-category decisions were learned using training data only.

### Feature expansion

| Stage | Feature count |
|---|---:|
| Raw predictors | 43 |
| Numeric transformed features | 8 |
| One-hot categorical features | 171 |
| Final transformed features | 179 |

The transformed matrices contained no missing, infinite, or invalid values.

### Custom transformer

`custom_transformers.py` contains the deployment-safe `RareCategoryGrouper` class required to load and reuse the serialized preprocessing pipeline.

---

## Model Development

### Baseline models

- Dummy Classifier
- Logistic Regression without class weighting
- Logistic Regression with balanced class weights
- Decision Tree with balanced class weights

The dummy model demonstrated the accuracy trap:

| Metric | Dummy result |
|---|---:|
| Accuracy | 88.72% |
| Recall | 0.00% |
| True positives | 0 |
| False negatives | 1,680 |

The model predicted every encounter as not readmitted. This established why accuracy alone was inappropriate.

The provisional baseline leader was class-weighted Logistic Regression:

| Metric | Validation result |
|---|---:|
| Accuracy | 66.98% |
| Balanced accuracy | 62.01% |
| Precision | 18.29% |
| Recall | 55.60% |
| F1-score | 27.52% |
| ROC-AUC | 66.94% |
| PR-AUC | 22.59% |

### Candidate models

The candidate stage evaluated stronger nonlinear and ensemble approaches, including:

- Random Forest
- Extra Trees
- HistGradientBoosting
- XGBoost
- CatBoost

These models were trained using the fixed training partition and evaluated on the validation partition. The reserved test set was not used for model comparison.

### Tuning and threshold analysis

Tuning was performed for the strongest candidate families. Thresholds were evaluated using validation probabilities rather than changing the underlying ranking model.

The selected tuned validation candidate was:

```text
Best Tuned XGBoost
Configuration: XGB_03_Deeper_Trees
Validation threshold: 0.50
```

Validation performance:

| Metric | Result |
|---|---:|
| Accuracy | 66.56% |
| Balanced accuracy | 63.15% |
| Precision | 18.70% |
| Recall | 58.75% |
| Specificity | 67.55% |
| F1-score | 28.37% |
| ROC-AUC | 68.07% |
| PR-AUC | 24.11% |
| True positives | 987 |
| False negatives | 693 |
| False positives | 4,290 |

### Advanced modeling

An additional advanced-modeling stage evaluated ensemble combinations as a robustness check. This work remained validation-only and did not access the test set.

Tuned XGBoost was selected as the final model because it provided a strong overall metric balance and the leading validation PR-AUC among the compared final candidates.

---

## Final Model

```text
Tuned XGBoost
```

The final production assets are:

```text
models/final_preprocessor.joblib
models/final_xgboost_model.joblib
artifacts/final_deployment_config.json
artifacts/streamlit_input_schema.json
```

The finalized prediction pipeline:

1. Accepts 43 raw predictors.
2. Applies the saved training-fitted preprocessor.
3. Produces 179 transformed features.
4. Generates a probability using `predict_proba`.
5. Applies the 0.50 and 0.45 operating thresholds.

No preprocessing rule is relearned inside the Streamlit application.

---

## Final Test Results

The final model was evaluated once on the previously untouched test set.

### Test-set characteristics

| Characteristic | Value |
|---|---:|
| Encounters | 14,976 |
| Positive cases | 1,698 |
| Negative cases | 13,278 |
| Positive rate | 11.338% |

### Final operating points

| Metric | Main balanced threshold | Recall-focused threshold |
|---|---:|---:|
| Threshold | 0.50 | 0.45 |
| Accuracy | 65.37% | 55.85% |
| Balanced accuracy | 61.08% | 60.80% |
| Precision | 17.55% | 15.86% |
| Recall | 55.54% | 67.20% |
| Specificity | 66.63% | 54.40% |
| F1-score | 26.67% | 25.66% |
| ROC-AUC | 66.39% | 66.39% |
| PR-AUC | 22.38% | 22.38% |
| Readmissions caught | 943 | 1,141 |
| Readmissions missed | 755 | 557 |
| False positives | 4,431 | 6,055 |
| True negatives | 8,847 | 7,223 |

### Final confusion matrices

Threshold 0.50:

```text
True negatives:  8,847
False positives: 4,431
False negatives:   755
True positives:    943
```

Threshold 0.45:

```text
True negatives:  7,223
False positives: 6,055
False negatives:   557
True positives:  1,141
```

![Final threshold comparison](outputs/figures/notebook_7_final_threshold_comparison_table.png)

---

## Threshold Strategy

The project intentionally presents two operating points.

### Main balanced threshold: 0.50

Use when the objective is a more balanced compromise between sensitivity and specificity.

- Recall: 55.54%
- Specificity: 66.63%
- Readmissions caught: 943
- False positives: 4,431

### Recall-focused screening threshold: 0.45

Use when missing a potential readmission is considered more costly and the operational setting can tolerate more follow-up alerts.

- Recall: 67.20%
- Specificity: 54.40%
- Readmissions caught: 1,141
- False positives: 6,055

### Trade-off

Lowering the threshold from 0.50 to 0.45:

- catches 198 additional readmissions
- reduces missed readmissions by 198
- creates 1,624 additional false-positive alerts

The two thresholds do not change ROC-AUC or PR-AUC because those metrics evaluate probability ranking across thresholds.

---

## Model Explainability

Explainability was completed after final test evaluation.

### Methods

- XGBoost feature importance
- Global SHAP importance
- Grouping transformed one-hot features back to original predictors
- Example local SHAP explanations for selected encounters

### Strongest global SHAP drivers

The leading original predictor groups included:

1. Discharge disposition
2. Medical specialty
3. Primary diagnosis group
4. Secondary diagnosis group
5. Additional diagnosis group
6. Age
7. Previous inpatient visits
8. Race
9. Glyburide status
10. Acarbose status

![Grouped SHAP importance](outputs/figures/notebook_8_top_15_grouped_original_shap_importance.png)

### Interpretation rules

- Global importance describes overall model behavior.
- A high global importance value does not imply causality.
- The sign and magnitude of a factor can differ between encounters.
- Demographic and clinical-category effects must be reviewed carefully for fairness and context.
- Saved local SHAP plots are examples and do not automatically explain a newly uploaded CSV row.

Explainability files are stored under:

```text
outputs/metrics/
outputs/figures/
```

---

## Streamlit Application

The final application is implemented in:

```text
app.py
```

Supporting interface modules are stored in:

```text
ui/form_config.py
ui/components.py
ui/styles.py
.streamlit/config.toml
```

The public deployment is available at:

[https://hospital-readmission-risk-prediction.streamlit.app/](https://hospital-readmission-risk-prediction.streamlit.app/)

### Application pages

The final sidebar contains eight pages:

1. **Overview**
2. **Data Explorer**
3. **Model Development**
4. **Model Performance**
5. **Risk Insights**
6. **Application Validation**
7. **Saved Figures**
8. **New Prediction**

### Professional Overview page

The Overview page was redesigned to present the finalized project in a clearer, more professional format. It now includes:

- a large healthcare-themed hero section
- an embedded hospital and analytics illustration
- the project title, academic capstone identity, and responsible-use wording
- direct actions for starting a prediction and viewing final model performance
- four factual project cards:
  - 99,343 hospital encounters
  - Tuned XGBoost
  - SHAP explainability
  - 108 of 108 validation checks passed
- a five-stage project pipeline:
  - data preparation
  - patient-level splitting
  - model development
  - dual thresholds
  - risk prediction and SHAP explanation
- horizontal Quick Access actions for:
  - New Prediction
  - Model Performance
  - Risk Insights
  - Application Validation
- updated sidebar branding and project-at-a-glance details
- responsive styling for smaller screens

The Overview values are based on saved project outputs. The validation count is loaded from the saved Notebook 09 summary rather than being fixed to an outdated value.

### Overview implementation fixes

The final interface update also corrected:

- raw SVG and HTML appearing as visible text
- Markdown code-block rendering inside project cards and the pipeline
- duplicated Overview disclaimer text
- outdated 98-of-98 validation text
- inconsistent spacing and alignment in the hero, cards, pipeline, and Quick Access section
- Overview navigation buttons so they open the correct existing application pages

The model, preprocessing pipeline, thresholds, prediction service, SHAP logic, downloads, and remaining seven pages were not retrained or functionally changed by the visual redesign.

### Main application features

- Professional light interface with a navy sidebar
- Responsive page heroes, metric cards, information cards, and threshold cards
- Professional Overview hero with embedded hospital illustration
- Factual project-summary cards and five-stage pipeline
- Working Overview navigation and Quick Access actions
- Cleaned-dataset summary and target-class visualization
- Development-stage model comparison
- Final untouched test-set results
- Threshold trade-off interpretation
- Saved model-development, final-evaluation, and explainability figures
- Global grouped SHAP driver table and chart
- Application Validation dashboard backed by Notebook 09 evidence files
- Guided five-step single-record form
- Explicit review confirmation before prediction
- Automatic clearing of confirmation and prior results after input changes
- Batch CSV upload
- Synthetic sample-record workflow
- Standard review cutoff at 0.50
- Additional screening cutoff at 0.45
- Probability scale with both cutoffs and the current prediction marker
- Dynamic top-five increasing and top-five reducing factors
- Downloadable screening results
- Downloadable prediction-factor results with readable values and retained original feature names
- De-identification guidance
- Academic decision-support disclaimer

### Approved visualizations

The application includes approved figures from:

- Overall comparison
- Baseline models
- Candidate models
- Threshold analysis
- Final evaluation
- Model explainability

Notebook 09 confirmed that the application defines **22 approved figures** and that **all 22 files are present**.

## Prediction Workflows

The **New Prediction** page provides three ways to submit the same finalized 43 predictors. Every method uses the same saved preprocessor, Tuned XGBoost model, probability calculation, thresholds, and explanation logic.

### Input method 1: Enter One Patient

The guided form collects all 43 predictors in five steps:

1. **Patient Profile**
2. **Hospital Encounter**
3. **Healthcare Use**
4. **Diabetes Management**
5. **Review**

The form is pre-filled with validated demonstration defaults because the model requires all 43 predictors. The user must review or replace every value, select the confirmation checkbox on the Review step, and then choose **Calculate Readmission Risk**. Changing any field clears the confirmation and previously calculated results.

The result includes:

- Estimated 30-day readmission risk
- Standard Review Result using the 0.50 cutoff
- Additional Screening Result using the 0.45 cutoff
- Five factors increasing the estimated risk
- Five factors reducing the estimated risk
- Downloadable screening result
- Downloadable prediction factors

### Input method 2: Upload Multiple Records

The application accepts a CSV containing one or more hospital encounter rows.

Input files:

```text
outputs/patient_input_template.csv
outputs/sample_patient_input.csv
```

- `patient_input_template.csv` contains the 43 required headers and no completed record.
- `sample_patient_input.csv` contains a synthetic demonstration record.
- The sample is not a real patient and is not drawn from the final test set.

The CSV must contain all 43 model predictors and must not contain:

- `encounter_id`
- `patient_nbr`
- `readmitted_30`

The prediction service checks:

- non-DataFrame or unreadable input
- empty files
- duplicate columns
- missing required columns
- unexpected columns
- surrounding spaces in column names
- shuffled column order
- missing or invalid numeric values
- numeric values outside validated ranges
- missing or blank categorical values
- transformed feature count

### Input method 3: Use Sample Record

The synthetic sample can be loaded directly into the guided form. This allows the complete direct-entry workflow to be demonstrated without entering real patient information.

### User-facing screening wording

Standard review at 0.50:

```text
Review Recommended
Standard Review Not Triggered
```

Additional screening at 0.45:

```text
Additional Screening Recommended
No Additional Screening Flag
```

A record can trigger additional screening at 0.45 without triggering standard review at 0.50. This is expected because the thresholds represent different operating priorities.

### Downloadable outputs

**Single-patient screening result**

- 1 row
- 48 columns
- 5 screening-result columns
- all 43 entered predictors

**Batch screening results**

- one row per uploaded record
- 6 user-facing result columns

**Prediction-factor results**

- 10 rows per explained record
- 5 increasing factors
- 5 reducing factors
- 7 output columns
- readable categorical values such as `70–79 years` and `Discharged to Home`
- original internal feature names retained for traceability

Notebook 09 verified that the direct-entry and CSV workflows return identical probabilities, threshold decisions, and explanation-factor rankings for identical input values.

## Installation and Local Execution

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd hospital-readmission-project
```

### 2. Create or activate an environment

Using the existing Conda environment:

```bash
conda activate readmission_project
```

Or create a standard virtual environment:

```bash
python -m venv .venv
```

Windows activation:

```bash
.venv\Scripts\activate
```

macOS/Linux activation:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Core technologies include:

- Python
- pandas
- NumPy
- scikit-learn
- XGBoost
- joblib
- SHAP
- Matplotlib
- Altair
- Streamlit

### 4. Validate the application files

```bash
python -m py_compile app.py
python -m py_compile prediction_service.py
python -m py_compile custom_transformers.py
python -m py_compile ui/form_config.py
python -m py_compile ui/components.py
python -m py_compile ui/styles.py
```

Successful syntax checks return no output.

### 5. Start Streamlit

```bash
python -m streamlit run app.py
```

The local application normally opens at:

```text
http://localhost:8501
```

### 6. Test the three prediction workflows

Open **New Prediction** and test:

1. **Enter One Patient**
2. **Upload Multiple Records**
3. **Use Sample Record**

For the validated synthetic sample, the estimated probability is approximately:

```text
46.39%
```

Expected threshold results:

```text
Standard Review Not Triggered
Additional Screening Recommended
```

### 7. Review formal validation evidence

Open and run:

```text
notebooks/09_streamlit_application_validation.ipynb
```

The completed notebook reports:

```text
108 checks passed
0 checks failed
100.00% pass rate
8 application pages validated
```

## Online Deployment

The application is deployed through Streamlit Community Cloud.

### Public application

[Hospital Readmission Risk Prediction](https://hospital-readmission-risk-prediction.streamlit.app/)

### Deployment coordinates

```text
Repository: hospital-readmission-project
Branch: main
Entrypoint: app.py
```

### Required preparation

Before deployment:

1. Confirm that `requirements.txt` contains compatible package versions.
2. Confirm that the final model and preprocessor are committed and available through Git or Git LFS.
3. Confirm that the application assets, CSV files, JSON files, metrics, and figures are present.
4. Run the Python syntax checks.
5. Run Notebook 09 and confirm 108 of 108 checks pass.
6. Push the final repository to GitHub.

### Community Cloud setup

1. Connect Streamlit Community Cloud to the GitHub account that owns the repository.
2. Create a new app from the existing repository.
3. Select branch `main`.
4. Set the entrypoint to `app.py`.
5. Select the Python version compatible with the serialized model environment.
6. Deploy and monitor the build logs.
7. Validate all eight pages and all three input methods.

The application does not require secrets or external credentials.

### Updating the deployed application

For normal code, documentation, figure, model, or artifact updates:

```text
Edit locally → test locally → commit → push
```

Streamlit Community Cloud rebuilds the app from the connected GitHub branch. Dependency changes in `requirements.txt` trigger a fuller rebuild. A manual reboot can be used when a deployment appears stale.

The application walkthrough is available in:

```text
STREAMLIT_APP_USER_GUIDE.md
```

## Regenerating Deployment Assets

The committed deployment assets can be regenerated using:

```bash
python prepare_deployment_assets.py
python prepare_streamlit_input_schema.py
python create_sample_input_csv.py
```

These scripts create:

```text
models/final_preprocessor.joblib
models/final_xgboost_model.joblib
artifacts/final_deployment_config.json
artifacts/streamlit_input_schema.json
outputs/patient_input_template.csv
outputs/sample_patient_input.csv
```

Regeneration does not retrain the model. It prepares deployment-safe copies and schemas from the finalized artifacts.

---

## Project Structure

```text
hospital-readmission-project/
│
├── app.py
├── prediction_service.py
├── custom_transformers.py
├── prepare_deployment_assets.py
├── prepare_streamlit_input_schema.py
├── create_sample_input_csv.py
├── README.md
├── STREAMLIT_APP_USER_GUIDE.md
├── requirements.txt
├── .gitignore
├── .gitattributes
│
├── .streamlit/
│   └── config.toml
│
├── ui/
│   ├── __init__.py
│   ├── form_config.py
│   ├── components.py
│   └── styles.py
│
├── data/
│   ├── raw/
│   └── processed/
│       ├── diabetic_modeling_data_final.csv
│       ├── model_feature_schema.json
│       └── patient_split_assignments.csv
│
├── notebooks/
│   ├── 01_data_audit.ipynb
│   ├── 02_eda.ipynb
│   ├── 03_data_splitting_preprocessing.ipynb
│   ├── 04_baseline_models.ipynb
│   ├── 05_candidate_models.ipynb
│   ├── 06_model_tuning_threshold_selection.ipynb
│   ├── 06.2_advanced_modeling.ipynb
│   ├── 07_final_test_evaluation.ipynb
│   ├── 08_model_explainability.ipynb
│   └── 09_streamlit_application_validation.ipynb
│
├── models/
│   ├── final_preprocessor.joblib
│   ├── final_xgboost_model.joblib
│   └── notebook-specific model artifacts
│
├── artifacts/
│   ├── preprocessing_metadata.json
│   ├── final_deployment_config.json
│   ├── streamlit_input_schema.json
│   ├── notebook_7_final_test_evaluation_summary.json
│   └── notebook_9_streamlit_validation_summary.json
│
├── outputs/
│   ├── metrics/
│   │   ├── notebook_7_final_threshold_comparison_table.csv
│   │   ├── notebook_8_grouped_original_shap_importance.csv
│   │   ├── notebook_9_streamlit_validation_checks.csv
│   │   ├── notebook_9_streamlit_validation_step_summary.csv
│   │   ├── notebook_9_streamlit_validation_overall_summary.csv
│   │   ├── notebook_9_direct_csv_parity_results.csv
│   │   ├── notebook_9_invalid_input_test_results.csv
│   │   ├── notebook_9_download_validation_results.csv
│   │   └── notebook_9_approved_figure_validation.csv
│   ├── figures/
│   ├── patient_input_template.csv
│   └── sample_patient_input.csv
│
└── reports/
    ├── eda/
    └── modeling/
```

## Notebook-by-Notebook Summary

<details>
<summary><strong>Notebook 1 — Data Audit and Initial Preparation</strong></summary>

### Objective

Audit the raw dataset, create the binary target, address missing-value representations, remove unsuitable records and non-informative fields, engineer readable clinical groups, and save a clean modeling dataset.

### Major actions

- Converted `"?"` values to missing values.
- Created `readmitted_30`.
- Removed `weight` because 96.86% was missing.
- Removed `payer_code` because of high missingness and limited modeling usefulness.
- Removed constant columns `examide` and `citoglipton`.
- Retained missing A1C and glucose testing as `Unknown`.
- Grouped admission type and admission source.
- Grouped hundreds of diagnosis codes into clinical categories.
- Grouped medical specialties.
- Removed 2,423 expired/hospice encounters.
- Retained `patient_nbr` for patient-level splitting.
- Retained `encounter_id` for tracking only.

### Main output

```text
data/processed/diabetic_modeling_data_final.csv
```

Final shape:

```text
99,343 rows × 46 columns
0 missing values
11.39% positive class rate
```

</details>

<details>
<summary><strong>Notebook 2 — Exploratory Data Analysis</strong></summary>

### Objective

Understand distributions, class imbalance, repeated-patient structure, predictor relationships, categorical cardinality, and leakage risks before modeling.

### Selected findings

- Class imbalance ratio: approximately 7.78 negatives per positive.
- `number_inpatient` was the strongest numeric association with the target.
- `discharge_disposition_id` had the strongest categorical association.
- Previous inpatient, emergency, and outpatient counts were highly right-skewed and zero-inflated.
- No numeric feature pair had absolute Spearman correlation of at least 0.70.
- Approximately 46% of encounters belonged to repeat patients.
- Most predictors had weak individual associations, supporting the use of multivariable nonlinear models.

### Final feature contract

```text
8 numeric predictors
35 categorical predictors
43 total predictors
```

Main schema:

```text
data/processed/model_feature_schema.json
```

</details>

<details>
<summary><strong>Notebook 3 — Patient-Level Splitting and Preprocessing</strong></summary>

### Objective

Create leakage-free train, validation, and test sets and validate the complete preprocessing workflow.

### Major actions

- Split patients rather than rows.
- Preserved similar positive rates across partitions.
- Confirmed zero patient overlap.
- Saved fixed encounter-level split assignments.
- Defined numeric and categorical preprocessing.
- Fitted preprocessing using training data only.
- Validated transformation on validation and reserved test data.
- Confirmed 179 transformed features and no non-finite values.

### Main outputs

```text
data/processed/patient_split_assignments.csv
artifacts/preprocessing_metadata.json
reports/modeling/transformed_feature_names.csv
reports/modeling/rare_category_summary.csv
reports/modeling/preprocessing_validation_summary.csv
```

</details>

<details>
<summary><strong>Notebook 4 — Baseline Models</strong></summary>

### Objective

Establish baseline performance and demonstrate why class imbalance requires more than accuracy.

### Models

- Dummy Classifier
- Unweighted Logistic Regression
- Class-weighted Logistic Regression
- Class-weighted Decision Tree

### Main conclusion

The dummy model achieved 88.72% accuracy but 0% recall. Class weighting substantially improved readmission detection. Class-weighted Logistic Regression was the strongest overall baseline.

### Main outputs

```text
models/notebook_4_fitted_preprocessor.joblib
outputs/metrics/notebook_4_baseline_model_comparison.csv
outputs/figures/notebook_4_baseline_metric_comparison.png
outputs/figures/notebook_4_baseline_roc_curves.png
outputs/figures/notebook_4_baseline_precision_recall_curves.png
```

</details>

<details>
<summary><strong>Notebook 5 — Candidate Models</strong></summary>

### Objective

Compare stronger nonlinear and ensemble classifiers using the fixed validation set.

### Candidate families

- Random Forest
- Extra Trees
- HistGradientBoosting
- XGBoost
- CatBoost

### Main conclusion

Boosting models produced the strongest overall validation performance. Candidate results informed the tuning stage, while the test set remained untouched.

### Main outputs

```text
outputs/metrics/notebook_5_candidate_model_comparison.csv
outputs/figures/notebook_5_candidate_metric_comparison.png
outputs/figures/notebook_5_candidate_roc_curves.png
outputs/figures/notebook_5_candidate_precision_recall_curves.png
artifacts/notebook_5_candidate_model_metadata.json
```

</details>

<details>
<summary><strong>Notebook 6 — Tuning and Threshold Selection</strong></summary>

### Objective

Tune the strongest model families, compare imbalance strategies, and evaluate threshold trade-offs using validation data only.

### Main conclusion

Best Tuned XGBoost was selected as the final validation candidate at threshold 0.50. It produced the strongest overall validation balance and PR-AUC among the final candidate models.

### Saved candidate

```text
models/notebook_6_selected_final_candidate_model.joblib
models/notebook_6_best_tuned_xgboost.joblib
models/notebook_6_best_tuned_xgboost.json
```

### Key outputs

```text
outputs/metrics/notebook_6_tuned_model_comparison.csv
outputs/metrics/notebook_6_threshold_tuning_results.csv
outputs/metrics/notebook_6_top_threshold_combinations.csv
outputs/figures/notebook_6_threshold_balanced_accuracy.png
outputs/figures/notebook_6_threshold_recall_precision_f1.png
outputs/figures/notebook_6_threshold_false_positive_false_negative_tradeoff.png
```

</details>

<details>
<summary><strong>Notebook 6B — Advanced Modeling</strong></summary>

### Objective

Evaluate advanced ensemble combinations and confirm whether they materially improved the validation trade-off.

### Main conclusion

The advanced ensemble stage served as a robustness check. It used training and validation data only. The test set remained untouched, and Tuned XGBoost remained the final selected model.

### Main outputs

```text
outputs/metrics/notebook_6b_advanced_model_comparison.csv
artifacts/notebook_6b_advanced_modeling_metadata.json
models/notebook_6b_selected_advanced_ensemble.joblib
```

</details>

<details>
<summary><strong>Notebook 7 — Final Untouched Test Evaluation</strong></summary>

### Objective

Evaluate the finalized Tuned XGBoost model exactly once on the reserved test set.

### Operating points

- Main balanced threshold: 0.50
- Recall-focused threshold: 0.45

### Main outputs

```text
outputs/metrics/notebook_7_final_xgboost_test_metrics.csv
outputs/metrics/notebook_7_final_threshold_comparison_table.csv
artifacts/notebook_7_final_test_evaluation_summary.json
outputs/figures/notebook_7_final_confusion_matrix_threshold_050.png
outputs/figures/notebook_7_final_confusion_matrix_threshold_045.png
outputs/figures/notebook_7_final_threshold_comparison_table.png
outputs/figures/notebook_7_final_xgboost_roc_curve.png
outputs/figures/notebook_7_final_xgboost_precision_recall_curve.png
```

### Main conclusion

Threshold 0.50 provided the main balanced result. Threshold 0.45 increased recall and caught 198 additional readmissions, with the expected cost of 1,624 additional false-positive alerts.

</details>

<details>
<summary><strong>Notebook 8 — Model Explainability</strong></summary>

### Objective

Explain global model behavior and provide example patient-level explanations.

### Methods

- XGBoost feature importance
- Global SHAP importance
- Grouped original-feature importance
- Example local SHAP explanations

### Main outputs

```text
outputs/metrics/notebook_8_grouped_original_feature_importance.csv
outputs/metrics/notebook_8_grouped_original_shap_importance.csv
outputs/metrics/notebook_8_xgboost_feature_importance.csv
outputs/metrics/notebook_8_xgboost_shap_transformed_feature_importance.csv
outputs/figures/notebook_8_top_15_grouped_original_feature_importance.png
outputs/figures/notebook_8_top_15_grouped_original_shap_importance.png
outputs/figures/notebook_8_selected_high_risk_patient_shap_explanation.png
outputs/figures/notebook_8_true_positive_patient_shap_explanation.png
```

### Main conclusion

Discharge disposition, medical specialty, diagnosis groups, age, and previous inpatient utilization were among the strongest global drivers. These findings describe model behavior and must not be interpreted as causal clinical effects.

</details>

---

<details>
<summary><strong>Notebook 9 — Streamlit Application Validation</strong></summary>

### Objective

Validate the finalized Streamlit application without retraining the model or changing preprocessing or thresholds.

### Validation areas

1. Deployment assets
2. Guided-form configuration
3. Direct-entry and CSV prediction parity
4. Invalid-input handling
5. Downloadable outputs
6. Application structure and saved assets

### Final validation result

```text
Validation steps completed: 6
Total validation checks: 108
Passed validation checks: 108
Failed validation checks: 0
Overall pass rate: 100.00%
Application pages: 8
Prediction input methods: 3
Approved figures: 22
Invalid-input tests: 18
```

Validation-area totals:

```text
Deployment Assets: 12 of 12 passed
Guided Form Configuration: 18 of 18 passed
Prediction Parity: 7 of 7 passed
Invalid-Input Handling: 18 of 18 passed
Downloadable Outputs: 28 of 28 passed
Application Structure: 25 of 25 passed
```

### Main outputs

```text
artifacts/notebook_9_streamlit_validation_summary.json
outputs/metrics/notebook_9_streamlit_validation_checks.csv
outputs/metrics/notebook_9_streamlit_validation_step_summary.csv
outputs/metrics/notebook_9_streamlit_validation_overall_summary.csv
outputs/metrics/notebook_9_direct_csv_parity_results.csv
outputs/metrics/notebook_9_invalid_input_test_results.csv
outputs/metrics/notebook_9_download_validation_results.csv
outputs/metrics/notebook_9_approved_figure_validation.csv
```

### Main conclusion

The finalized application passed all structural, prediction, explanation, input-validation, download, theme, validation-dashboard, and deployment-asset checks. Direct entry and CSV upload produced identical outputs for identical values. The refreshed checks also confirmed the professional Overview hero, factual project cards, five-stage pipeline, six Overview navigation actions, responsive Overview styling, eight-page navigation, confirmation workflow, readable factor downloads, and Application Validation dashboard.

</details>

## Important Artifacts

### Final deployment

```text
models/final_preprocessor.joblib
models/final_xgboost_model.joblib
artifacts/final_deployment_config.json
artifacts/streamlit_input_schema.json
```

### Final evaluation

```text
outputs/metrics/notebook_7_final_xgboost_test_metrics.csv
outputs/metrics/notebook_7_final_threshold_comparison_table.csv
artifacts/notebook_7_final_test_evaluation_summary.json
```

### Explainability

```text
outputs/metrics/notebook_8_grouped_original_shap_importance.csv
outputs/metrics/notebook_8_grouped_original_feature_importance.csv
outputs/figures/notebook_8_top_15_grouped_original_shap_importance.png
```

### Application interface

```text
app.py
.streamlit/config.toml
ui/form_config.py
ui/components.py
ui/styles.py
```

### Application inputs

```text
outputs/patient_input_template.csv
outputs/sample_patient_input.csv
```

### Application validation

```text
notebooks/09_streamlit_application_validation.ipynb
artifacts/notebook_9_streamlit_validation_summary.json
outputs/metrics/notebook_9_streamlit_validation_checks.csv
outputs/metrics/notebook_9_streamlit_validation_step_summary.csv
outputs/metrics/notebook_9_streamlit_validation_overall_summary.csv
outputs/metrics/notebook_9_direct_csv_parity_results.csv
outputs/metrics/notebook_9_invalid_input_test_results.csv
outputs/metrics/notebook_9_download_validation_results.csv
outputs/metrics/notebook_9_approved_figure_validation.csv
```

## Reproducibility and Validation

The project follows these safeguards:

1. Fixed random seed and saved split assignments.
2. Patient-level splitting with zero overlap.
3. Training-only preprocessing fit.
4. Validation-only model selection and threshold analysis.
5. Test set reserved until final evaluation.
6. Saved feature schema and exact feature order.
7. Saved preprocessor and final model.
8. Deployment checks for 43 raw and 179 transformed features.
9. Validation before direct-entry or CSV prediction.
10. Dynamic explanation reconstruction checks.
11. Direct-entry and CSV parity testing.
12. Download export-and-reload testing.
13. Static application structure and syntax testing.
14. Saved evidence from Notebook 09.

### Deployment validation

The final deployment assets were verified as:

```text
Preprocessor type: ColumnTransformer
Raw input features: 43
Model type: XGBClassifier
Transformed input features: 179
predict_proba available: True
```

### Application Validation dashboard

The eighth application page reads the saved Notebook 09 evidence files and displays:

- total, passed, and failed check counts
- overall pass rate
- validation coverage by area
- prediction-consistency results
- valid- and invalid-input tests
- download validation
- application-structure checks
- approved-figure validation
- all 108 detailed checks with validation-area filtering

### Guided-form validation

Notebook 09 confirmed:

```text
4 data-entry sections
43 configured predictors
43 unique predictors
0 missing predictors
0 unexpected predictors
0 duplicate predictors
All defaults, ranges, options, and labels valid
```

The guided workflow adds a fifth **Review** step before prediction.

### Prediction parity validation

For the synthetic sample:

```text
Direct-entry probability: 46.38500810%
CSV probability:          46.38500810%
Difference:               0.000000000000
```

The threshold classifications and top-five increasing and reducing factors also matched.

### Invalid-input validation

Notebook 09 ran 18 tests:

```text
Accepted valid-input tests: 4
Rejected invalid-input tests: 14
Failed tests: 0
```

### Download validation

The validated outputs were:

```text
Single-patient screening result: 1 row × 48 columns
Batch screening results:        1 row × 6 columns
Prediction-factor results:     10 rows × 7 columns
```

All CSV payloads were exported and reloaded successfully.

### Final application-validation result

```text
Validation steps: 6
Total checks: 108
Passed: 108
Failed: 0
Pass rate: 100.00%
Pages validated: 8
Input methods validated: 3
Approved figures validated: 22
```

## Limitations

- The source data covers hospital encounters from 1999–2008 and may not represent current clinical practice.
- The model uses structured encounter data and does not include free-text notes, imaging, longitudinal laboratory trends, social determinants, or post-discharge information.
- Predictive performance is moderate; the system should be viewed as a screening prototype rather than a definitive clinical tool.
- The positive class is imbalanced, producing low precision and many false-positive alerts at the recall-focused cutoff.
- Some predictors may reflect hospital workflows or documentation patterns rather than direct clinical risk.
- The dataset includes demographic variables, so fairness and subgroup performance should be reviewed before real-world use.
- Global and record-level SHAP-style contributions describe model behavior and do not establish causality.
- The direct-entry workflow requires all 43 predictors; no reduced-input clinical model was trained.
- The application does not connect to an electronic health record, store patient histories, authenticate users, or create clinical care plans.
- Notebook 09 validates software behavior and internal consistency; it does not replace external clinical validation, calibration review, security assessment, or regulatory evaluation.

## Responsible Use

This project is intended for:

- academic demonstration
- model-development education
- threshold trade-off analysis
- explainable-AI demonstration
- portfolio and capstone review

It is not intended for:

- diagnosis
- treatment selection
- automated discharge decisions
- denial of care
- unsupervised clinical deployment
- use without validation on a current local population

Any future clinical use would require external validation, calibration assessment, fairness analysis, privacy review, security review, workflow testing, clinician oversight, and regulatory evaluation.

---

## Future Enhancements

Potential next steps include:

1. Add probability calibration and calibration plots.
2. Evaluate subgroup performance and fairness.
3. Validate on a newer external dataset.
4. Add hospital-specific recalibration.
5. Train and compare a smaller-input model for faster manual entry.
6. Integrate secure electronic health record data ingestion.
7. Add role-based access, authentication, logging, and audit trails.
8. Add drift monitoring and scheduled revalidation.
9. Compare cost-sensitive learning using explicit operational cost assumptions.
10. Add automated unit tests and continuous-integration workflows based on Notebook 09 checks.
11. Add secure report generation and authorized patient-record persistence.
12. Evaluate alternative deployment environments for controlled organizational use.

## Final Conclusion

This capstone demonstrates a complete, leakage-aware machine-learning lifecycle:

- rigorous data cleaning
- clinically motivated feature engineering
- patient-level leakage prevention
- reproducible preprocessing
- imbalanced-class evaluation
- baseline and advanced modeling
- hyperparameter tuning
- threshold-based decision analysis
- one-time untouched test evaluation
- global and record-level explainability
- guided single-record prediction
- batch CSV prediction
- professional eight-page Streamlit deployment
- comprehensive application validation

The final Tuned XGBoost model provides moderate but meaningful predictive signal. The project’s strongest contribution is not a single accuracy value; it is the disciplined methodology used to protect the test set, prevent patient-level leakage, quantify threshold trade-offs, explain model behavior, provide consistent predictions across input methods, and validate the complete application through 108 successful checks.

The deployed system remains an academic decision-support prototype and must not be interpreted as a medical diagnosis or used as the sole basis for patient-care decisions.
