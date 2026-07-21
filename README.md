# Notebook 1: Data Audit and Initial Data Preparation

## Objective

The purpose of this notebook was to understand the hospital readmission dataset, identify data-quality issues, create the prediction target, prevent data leakage, perform initial feature engineering, and prepare a clean dataset for exploratory data analysis and model development.

## Dataset Overview

* Dataset: Diabetes 130-US Hospitals for Years 1999–2008
* Original number of rows: 101,766
* Original number of columns: 50
* Unit of analysis: One hospital encounter
* Number of unique patients: 71,518
* The dataset contains repeated hospital encounters for some patients.

## Target Variable Creation

The original target column contained three categories:

* `NO`: Patient was not readmitted
* `>30`: Patient was readmitted after 30 days
* `<30`: Patient was readmitted within 30 days

A binary target named `readmitted_30` was created:

* `<30` → 1
* `>30` → 0
* `NO` → 0

### Original target distribution

* Not readmitted within 30 days: 90,409 encounters
* Readmitted within 30 days: 11,357 encounters
* Positive class percentage: 11.16%

### Insight

The target is highly imbalanced. Therefore, accuracy alone will not be sufficient for model evaluation. Recall, precision, F1-score, ROC-AUC, PR-AUC, and the confusion matrix will be used later.

## Missing-Value Analysis

The dataset used `"?"` to represent missing values. These values were converted to proper null values.

### Major missing-value findings

* `weight`: 96.86% missing
* `max_glu_serum`: 94.75% missing
* `A1Cresult`: 83.28% missing
* `medical_specialty`: 49.08% missing
* `payer_code`: 39.56% missing
* `race`: 2.23% missing
* `diag_3`: 1.40% missing
* `diag_2`: 0.35% missing
* `diag_1`: 0.02% missing

### Decisions

* `weight` was removed because almost all values were missing.
* `payer_code` was removed because of high missingness and limited clinical usefulness.
* Missing values in `A1Cresult` and `max_glu_serum` were retained as an `Unknown` category because the absence of testing may itself contain useful information.
* Missing values in `race` and diagnosis columns were replaced with `Unknown`.
* `medical_specialty` was cleaned and grouped into common specialties, `Unknown`, and `Other`.

## Duplicate and Patient-Level Analysis

* Exact duplicate rows: 0
* Unique encounter IDs: 101,766
* Patients with more than one encounter: 16,773
* Maximum encounters for one patient: 40

### Insight

The same patient may appear multiple times in the dataset. A random row-level train-test split could place encounters from the same patient in both training and testing data.

### Decision

A patient-level split using `patient_nbr` will be used later to prevent patient-level data leakage.

## Constant Columns

Two columns contained only one value:

* `examide`
* `citoglipton`

### Decision

Both columns were removed because they provide no predictive information.

## Demographic Analysis

### Gender

* Female: 54,708
* Male: 47,055
* Unknown/Invalid: 3

### Race

* Caucasian: 76,099
* African American: 19,210
* Hispanic: 2,037
* Other: 1,506
* Asian: 641
* Missing: 2,273

### Age

Most encounters were for patients between 50 and 90 years old.

Largest age groups:

* `[70–80)`: 26,068
* `[60–70)`: 22,483
* `[50–60)`: 17,256
* `[80–90)`: 17,197

### Insight

The dataset mainly represents older diabetic patients, which is reasonable for a hospital readmission study.

## Numerical Feature Analysis

The following numerical variables were reviewed:

* `time_in_hospital`
* `num_lab_procedures`
* `num_procedures`
* `num_medications`
* `number_outpatient`
* `number_emergency`
* `number_inpatient`
* `number_diagnoses`

### Important findings

* Median hospital stay: 4 days
* Maximum hospital stay: 14 days
* Maximum number of medications: 81
* Maximum previous outpatient visits: 42
* Maximum previous emergency visits: 76
* Maximum previous inpatient visits: 21

### Utilization-feature findings

* 83.55% of encounters had zero previous outpatient visits.
* 88.81% had zero previous emergency visits.
* 66.46% had zero previous inpatient visits.

### Insight

Healthcare utilization features are strongly right-skewed. Extreme values were not removed because they may represent clinically important high-risk patients.

## Discharge Disposition Analysis

The `IDs_mapping.csv` file was used to interpret discharge disposition codes.

The following categories were identified as expired or hospice cases:

* 11: Expired
* 13: Hospice/home
* 14: Hospice/medical facility
* 19: Expired at home
* 20: Expired in a medical facility
* 21: Expired, place unknown

### Decision

A total of 2,423 encounters were removed because these patients were not appropriate candidates for standard 30-day readmission prediction.

### Dataset after exclusion

* Rows remaining: 99,343
* Unique patients remaining: 69,990
* Patients with multiple encounters: 16,341
* Maximum encounters for one patient: 40

### Updated target distribution

* Not readmitted within 30 days: 88,029 encounters
* Readmitted within 30 days: 11,314 encounters
* Positive class percentage: 11.39%

## Admission Type Feature Engineering

Original admission-type IDs were grouped into readable categories:

* Emergency
* Urgent
* Elective
* Unknown
* Other

### Final distribution

* Emergency: 52,371
* Elective: 18,668
* Urgent: 18,132
* Unknown: 10,144
* Other: 28

## Admission Source Feature Engineering

Original admission-source IDs were converted into readable descriptions and grouped into:

* Emergency Room
* Referral
* Transfer
* Unknown
* Other

### Final distribution

* Emergency Room: 55,850
* Referral: 30,434
* Unknown: 6,854
* Transfer: 6,185
* Other: 20

## Diagnosis Feature Engineering

The original diagnosis columns contained hundreds of ICD codes:

* `diag_1`: 716 unique codes
* `diag_2`: 748 unique codes
* `diag_3`: 789 unique codes

The codes were grouped into broader clinical categories:

* Circulatory
* Diabetes
* Digestive
* Genitourinary
* Injury
* Musculoskeletal
* Neoplasms
* Respiratory
* Other
* Unknown

### Insight

Circulatory conditions were the most common diagnosis category across all three diagnosis columns.

The original diagnosis-code columns were removed after creating:

* `diag_1_group`
* `diag_2_group`
* `diag_3_group`

## Medical Specialty Feature Engineering

The original `medical_specialty` column had:

* 72 unique specialties
* 49,949 missing values
* 56 specialties with fewer than 500 encounters

### Decision

* Missing values were replaced with `Unknown`.
* Common specialties were retained.
* Rare specialties were grouped into `Other`.

The grouped column was saved as:

* `medical_specialty_group`

## Medication Feature Review

The individual medication columns were analyzed.

Commonly used medication features included:

* metformin
* glimepiride
* glipizide
* glyburide
* pioglitazone
* rosiglitazone
* insulin

Several medication features were extremely rare, while `examide` and `citoglipton` were constant.

The summary variables `change` and `diabetesMed` were retained because they contain useful variation.

### Distribution of diabetes medication

* Yes: 78,363
* No: 23,403

### Distribution of medication change

* No change: 54,755
* Changed: 47,011

## Columns Removed

The following columns were removed:

* `weight`
* `payer_code`
* `examide`
* `citoglipton`
* `medical_specialty`
* `medical_specialty_clean`
* `admission_type_id`
* `admission_source_id`
* `admission_source_desc`
* `diag_1`
* `diag_2`
* `diag_3`
* `readmitted`

## Columns Retained for Special Purposes

* `patient_nbr`: retained only for patient-level splitting
* `encounter_id`: retained temporarily for encounter tracking
* `readmitted_30`: retained as the binary target variable

## Final Dataset

The final audited dataset was saved as:

`data/processed/diabetic_modeling_data_final.csv`

### Final dataset characteristics

* Rows: 99,343
* Columns: 46
* Missing values: 0
* Positive class rate: 11.39%

## Files Generated

* `data/processed/diabetic_modeling_data_final.csv`
* `outputs/metrics/column_decisions.csv`

## Main Insights

1. The dataset is large enough for machine-learning model development.
2. The target variable is strongly imbalanced.
3. Repeated patients create a meaningful data-leakage risk.
4. A patient-level split is required.
5. Several columns had extreme missingness.
6. Constant and clinically unsuitable columns were removed.
7. Diagnosis codes required grouping because of high cardinality.
8. Admission type and admission source were converted into readable categories.
9. Most patients were older adults.
10. Previous inpatient, emergency, and outpatient utilization features were highly skewed but potentially important.
11. The final dataset contains no missing values and is ready for exploratory data analysis.

## Next Steps

The next notebook will be:

`02_eda.ipynb`

The next phase will include:

* readmission rate by age
* readmission rate by race and gender
* readmission rate by admission type
* readmission rate by admission source
* readmission rate by diagnosis group
* readmission rate by previous inpatient visits
* readmission rate by emergency visits
* readmission rate by number of medications
* readmission rate by time in hospital
* correlation and distribution analysis
* creation of visualizations for the progress presentation
* identification of features that may be useful for model training


# Notebook 2: Exploratory Data Analysis Summary

## Objective

Notebook 2 was used to explore the cleaned hospital readmission dataset, understand the target distribution, analyze numeric and categorical predictors, identify possible leakage risks, and finalize the features for model development.

---

## 1. Dataset Validation

### What We Did

- Loaded the cleaned dataset from:

```text
data/processed/diabetic_modeling_data_final.csv
```

- Verified the dataset dimensions.
- Checked for missing values.
- Checked for duplicate rows.
- Confirmed that the target variable `readmitted_30` was present.

### Output

- Rows: **99,343**
- Columns: **46**
- Missing values: **0**
- Duplicate rows: **0**
- Target column present: **Yes**

---

## 2. Column and Data-Type Inspection

### What We Did

- Reviewed all column names and data types.
- Separated numeric and categorical columns.
- Identified identifier and target columns.
- Checked for constant columns.

### Output

- Numeric columns in the complete dataset: **12**
- Categorical/string columns: **34**
- Constant columns: **None**

### Special-Purpose Columns

- `encounter_id`: encounter identifier
- `patient_nbr`: patient identifier
- `readmitted_30`: target variable

---

## 3. Target Variable Distribution

### What We Did

- Calculated the number and percentage of readmitted and non-readmitted encounters.
- Created a target distribution chart.
- Calculated the class imbalance ratio.

### Output

| Target Class | Count | Percentage |
|---|---:|---:|
| Not readmitted within 30 days | 88,029 | 88.61% |
| Readmitted within 30 days | 11,314 | 11.39% |

### Main Finding

The dataset is imbalanced, with approximately:

```text
7.78 non-readmitted encounters for every 1 readmitted encounter
```

Because of this imbalance, model evaluation should not rely only on accuracy. Recall, precision, F1-score, ROC-AUC, and PR-AUC will be more useful.

---

## 4. Numeric Feature Summary

### What We Did

Analyzed the following numeric clinical predictors:

- `time_in_hospital`
- `num_lab_procedures`
- `num_procedures`
- `num_medications`
- `number_outpatient`
- `number_emergency`
- `number_inpatient`
- `number_diagnoses`

For each variable, we calculated:

- Mean
- Standard deviation
- Minimum
- Median
- Maximum
- Skewness
- Number of unique values
- Number and percentage of zero values

### Main Findings

- Median hospital stay: **4 days**
- Median laboratory procedures: **44**
- Median procedures: **1**
- Median medications: **15**
- Median diagnoses: **8**
- `number_outpatient`, `number_emergency`, and `number_inpatient` were highly right-skewed.
- `num_procedures` contained approximately **45.98% zero values**.
- Previous healthcare-utilization variables contained many zero values.

---

## 5. Numeric Feature Distributions

### What We Did

- Created histograms for all eight numeric clinical predictors.
- Added median reference lines.
- Used the 99th percentile only as a chart display limit.

### Main Findings

- Prior inpatient, outpatient, and emergency visits were zero-inflated.
- Hospital stay and medication count were right-skewed.
- No observations were deleted or modified during visualization.

---

## 6. Numeric Features Compared With Readmission

### What We Did

- Compared the mean and median values of numeric features between readmitted and non-readmitted encounters.
- Calculated correlations between each numeric predictor and the target.

### Main Findings

The strongest numeric association with readmission was:

```text
number_inpatient
```

- Mean for non-readmitted encounters: **0.56**
- Mean for readmitted encounters: **1.22**
- Correlation with target: approximately **0.17**

Readmitted encounters also had higher average values for:

- Emergency visits
- Number of diagnoses
- Time in hospital
- Number of medications
- Laboratory procedures
- Outpatient visits

These results show association only and do not establish causation.

---

## 7. Categorical Feature Audit

### What We Did

- Calculated the number of unique categories for each categorical feature.
- Identified the most common category.
- Measured dominant-category percentages.
- Identified rare categories representing less than 1% of encounters.

### Output

- Total categorical modeling features: **35**

### Highest-Cardinality Features

- `discharge_disposition_id`: **21 categories**
- `medical_specialty_group`: **18 categories**
- `age`: **10 categories**
- Diagnosis groups: **10 categories each**

### Main Findings

- Several medication variables were dominated by `"No"`.
- Some medication categories appeared in only a few encounters.
- Rare-category grouping may be required during preprocessing.

---

## 8. Demographic Analysis

### What We Did

Compared readmission rates across:

- Race
- Gender
- Age group

### Race Results

| Race | Readmission Rate |
|---|---:|
| Caucasian | 11.53% |
| African American | 11.45% |
| Hispanic | 10.51% |
| Asian | 10.35% |
| Other | 9.78% |
| Unknown | 8.41% |

### Gender Results

| Gender | Readmission Rate |
|---|---:|
| Female | 11.46% |
| Male | 11.30% |

The major gender groups had almost identical readmission rates.

### Age Results

Notable age-group readmission rates included:

- Age 20–30: **14.31%**
- Age 70–80: **12.06%**
- Age 80–90: **12.56%**
- Age 90–100: **11.90%**
- Age 50–60: **9.77%**

Very small demographic groups were treated cautiously because their rates may be unstable.

---

## 9. Clinical Group Analysis

### What We Did

Compared readmission rates across:

- Admission type
- Admission source
- Medical specialty
- Primary diagnosis group

### Admission Type Results

| Admission Type | Readmission Rate |
|---|---:|
| Emergency | 11.83% |
| Urgent | 11.35% |
| Unknown | 10.87% |
| Elective | 10.49% |

### Admission Source Results

| Admission Source | Readmission Rate |
|---|---:|
| Emergency Room | 11.98% |
| Unknown | 10.78% |
| Referral | 10.71% |
| Transfer | 10.07% |

### Medical Specialty Results

Higher observed readmission rates included:

- Nephrology: **16.11%**
- Surgery-Vascular: **14.10%**
- Psychiatry: **12.19%**
- Family/General Practice: **12.12%**

Lower observed rates included:

- Cardiology: **8.03%**
- Orthopedics-Reconstructive: **7.48%**
- Surgery-Cardiovascular/Thoracic: **6.70%**
- Obstetrics and Gynecology: **4.78%**

### Primary Diagnosis Results

| Primary Diagnosis Group | Readmission Rate |
|---|---:|
| Diabetes | 13.11% |
| Injury | 12.40% |
| Circulatory | 11.69% |
| Other | 11.68% |
| Genitourinary | 11.04% |
| Respiratory | 10.06% |
| Musculoskeletal | 9.54% |

---

## 10. Diabetes Management Feature Analysis

### What We Did

Compared readmission rates across:

- Maximum glucose serum result
- A1C result
- Medication change
- Diabetes medication use
- Insulin status
- Metformin status

### Maximum Glucose Serum

| Category | Readmission Rate |
|---|---:|
| Unknown | 11.31% |
| Normal | 11.55% |
| Above 200 | 12.97% |
| Above 300 | 15.07% |

### A1C Result

| Category | Readmission Rate |
|---|---:|
| Unknown | 11.69% |
| Normal | 9.77% |
| Above 7 | 10.15% |
| Above 8 | 9.94% |

### Medication Change

| Category | Readmission Rate |
|---|---:|
| No change | 10.84% |
| Changed | 12.02% |

### Diabetes Medication

| Category | Readmission Rate |
|---|---:|
| No | 9.87% |
| Yes | 11.84% |

### Insulin

| Category | Readmission Rate |
|---|---:|
| No | 10.21% |
| Steady | 11.37% |
| Up | 13.33% |
| Down | 14.22% |

### Metformin

| Category | Readmission Rate |
|---|---:|
| No | 11.79% |
| Steady | 9.78% |
| Up | 8.28% |
| Down | 12.02% |

These differences may reflect illness severity and should not be interpreted as direct medication effects.

---

## 11. Repeated-Patient and Leakage Audit

### What We Did

- Counted unique patients.
- Measured how many patients had multiple encounters.
- Examined readmission rates by the number of encounters per patient.
- Evaluated the risk of patient-level data leakage.

### Output

- Total encounters: **99,343**
- Unique patients: **69,990**
- Patients with more than one encounter: **16,341**
- Repeat-patient percentage: **23.35%**
- Encounters belonging to repeat patients: **45,694**
- Percentage of encounters from repeat patients: **46.00%**
- Maximum encounters for one patient: **40**
- Median encounters per patient: **1**

### Main Finding

A normal random row split could place encounters from the same patient into both training and testing data.

Therefore, future splitting must use:

```text
patient_nbr
```

All encounters from the same patient must remain in only one dataset partition.

---

## 12. Categorical Association Ranking

### What We Did

- Calculated bias-corrected Cramér’s V for every categorical predictor.
- Ranked categorical features by their association with `readmitted_30`.

### Strongest Associations

| Feature | Cramér’s V |
|---|---:|
| discharge_disposition_id | 0.114 |
| insulin | 0.044 |
| medical_specialty_group | 0.041 |
| age | 0.035 |
| diag_3_group | 0.035 |
| diag_1_group | 0.028 |
| metformin | 0.026 |
| diabetesMed | 0.026 |

### Main Finding

Most categorical variables had weak individual associations with readmission. The model will likely require combinations of several predictors.

---

## 13. Numeric Correlation and Redundancy Audit

### What We Did

- Calculated Spearman correlations among numeric clinical predictors.
- Ranked numeric feature pairs by absolute correlation.
- Checked for strong correlations above `0.70`.

### Highest Correlations

| Feature Pair | Spearman Correlation |
|---|---:|
| time_in_hospital and num_medications | 0.46 |
| num_procedures and num_medications | 0.35 |
| time_in_hospital and num_lab_procedures | 0.34 |
| num_medications and number_diagnoses | 0.29 |

### Main Finding

No numeric feature pair had an absolute correlation of at least `0.70`.

Therefore, no severe numeric multicollinearity or redundancy was identified.

---

## 14. Final Modeling Feature Audit

### What We Did

- Removed identifiers and the target from the predictor list.
- Separated numeric and categorical modeling features.
- Created the final modeling objects:
  - `X`
  - `y`
  - `groups`
- Checked for suspicious target-related column names.

### Columns Excluded From Modeling

- `encounter_id`
- `patient_nbr`
- `readmitted_30`

### Final Feature Structure

- Numeric modeling features: **8**
- Categorical modeling features: **35**
- Total modeling features: **43**

### Modeling Object Shapes

```text
X shape: (99,343, 43)
y shape: (99,343,)
groups shape: (99,343,)
```

### Leakage Audit Result

- Target included in predictors: **No**
- Encounter identifier included: **No**
- Patient identifier included: **No**
- Suspicious outcome-related predictors: **None**

---

## 15. Files Saved

### Feature Schema

The final modeling feature schema was saved as:

```text
data/processed/model_feature_schema.json
```

The schema contains:

- Dataset path
- Target column
- Positive class
- Patient grouping column
- Identifier columns
- Numeric features
- Categorical features
- All 43 modeling predictors
- Class counts
- Positive-class rate
- Prediction timing

### EDA Reports

EDA summary tables were saved in:

```text
reports/eda/
```

The saved outputs include:

- Target distribution
- Numeric feature summary
- Numeric feature comparison
- Categorical feature summary
- Categorical association ranking
- Demographic summaries
- Clinical group summaries
- Diabetes management summaries
- Repeated-patient audit

---

## Main Conclusions

1. The target is imbalanced, with only **11.39%** readmitted cases.
2. `number_inpatient` was the strongest numeric predictor identified during EDA.
3. `discharge_disposition_id` had the strongest categorical association with readmission.
4. Nephrology, vascular surgery, diabetes diagnosis, high glucose values, and insulin changes showed higher observed readmission rates.
5. Approximately **46% of encounters** belonged to repeat patients.
6. Patient-level splitting is required to prevent data leakage.
7. Most predictors had weak individual relationships with the target.
8. The model will likely depend on interactions and combinations of multiple features.
9. No severe correlation or multicollinearity was found among numeric features.
10. The final approved modeling dataset contains **43 predictors**.

---

## Notebook 2 Status

```text
Completed
```

## Next Step

Proceed to Notebook 3 for:

```text
Patient-level data splitting, preprocessing, model training, tuning, and evaluation
```


# Notebook 3: Patient-Level Splitting and Preprocessing Summary

## Objective

Notebook 3 created leakage-free train, validation, and test partitions, defined the preprocessing workflow, validated transformed features, and saved all split and preprocessing information required for model development.

---

## 1. Modeling Inputs Loaded and Validated

### What We Did

- Loaded the audited dataset:

```text
data/processed/diabetic_modeling_data_final.csv
```

- Loaded the feature schema:

```text
data/processed/model_feature_schema.json
```

- Created:
  - `X`: predictor matrix
  - `y`: target variable
  - `groups`: patient identifiers
  - `tracking_ids`: encounter identifiers
- Verified dataset dimensions, feature counts, and leakage exclusions.

### Output

- Dataset shape: **99,343 × 46**
- Predictor matrix shape: **99,343 × 43**
- Unique patients: **69,990**
- Numeric predictors: **8**
- Categorical predictors: **35**
- Total predictors: **43**
- Positive-class rate: **11.3888%**

### Leakage Validation

The following columns were excluded from the predictor matrix:

- `encounter_id`
- `patient_nbr`
- `readmitted_30`

---

## 2. Patient-Level Train, Validation, and Test Splits

### What We Did

- Created one summary row per patient.
- Stratified patients using:
  - Whether the patient had any 30-day readmission
  - Patient encounter frequency
- Split patients into:
  - 70% training
  - 15% validation
  - 15% test
- Assigned every encounter from the same patient to one partition only.

### Split Results

| Split | Encounters | Encounter % | Patients | Patient % | Positive Cases | Positive Rate |
|---|---:|---:|---:|---:|---:|---:|
| Train | 69,467 | 69.93% | 48,993 | 70.00% | 7,936 | 11.424% |
| Validation | 14,900 | 15.00% | 10,498 | 15.00% | 1,680 | 11.275% |
| Test | 14,976 | 15.08% | 10,499 | 15.00% | 1,698 | 11.338% |

### Main Finding

The positive-class rate remained very similar across all three partitions.

---

## 3. Patient Leakage Audit

### Output

```text
Train vs. validation overlap: 0
Train vs. test overlap: 0
Validation vs. test overlap: 0
```

### Main Finding

No patient appeared in more than one partition. This prevents patient-level leakage.

---

## 4. Split Assignment Files Saved

### Files

```text
data/processed/patient_split_assignments.csv
```

```text
reports/modeling/split_summary.csv
```

### Validation Results

- Saved rows: **99,343**
- Unique encounters: **99,343**
- Unique patients: **69,990**
- Maximum number of splits per patient: **1**
- Unassigned encounters: **0**

The exact train, validation, and test partitions can now be reused in later notebooks without regenerating the split.

---

## 5. Feature Consistency Audit

### What We Did

Verified that train, validation, and test partitions contained:

- The same 43 feature names
- The same feature order
- No missing values
- Correct numeric and categorical feature assignments

### Output

| Split | Rows | Columns | Missing Values |
|---|---:|---:|---:|
| Train | 69,467 | 43 | 0 |
| Validation | 14,900 | 43 | 0 |
| Test | 14,976 | 43 | 0 |

### Additional Findings

- `discharge_disposition_id` was correctly treated as categorical.
- No validation categories were absent from training.
- No test categories were absent from training.

---

## 6. Duplicate Predictor Pattern Audit

### What We Did

The training predictor matrix contained one duplicated feature pattern, so the matching rows were inspected.

### Output

- Rows involved: **2**
- Unique encounters: **2**
- Unique patients: **2**
- Target values: both `0`
- Exact duplicate complete rows: **0**

### Main Finding

The two rows belonged to different patients and different encounters but happened to share identical predictor values. Both records were retained.

---

## 7. Preprocessing Pipeline Defined

### Numeric Preprocessing

Applied to the eight numeric predictors:

1. Median imputation
2. Standard scaling

### Categorical Preprocessing

Applied to the 35 categorical predictors:

1. Most-frequent imputation
2. Rare-category grouping
3. One-hot encoding
4. Safe handling of unseen categories

### Configuration

```text
Rare-category minimum frequency: 10
```

Categories appearing fewer than 10 times in the training data were grouped as infrequent.

---

## 8. Preprocessing Fitted and Validated

### What We Did

- Fitted a temporary preprocessing copy using only `X_train`.
- Transformed validation and test data without refitting.
- Checked matrix dimensions, sparsity, and invalid values.

### Output

| Split | Rows | Transformed Features | Sparse Matrix | Non-Finite Values |
|---|---:|---:|---|---|
| Train | 69,467 | 179 | Yes | No |
| Validation | 14,900 | 179 | Yes | No |
| Test | 14,976 | 179 | Yes | No |

### Feature Expansion

- Raw predictors: **43**
- Numeric transformed features: **8**
- One-hot categorical features: **171**
- Total transformed predictors: **179**

### Sparse Matrix Density

```text
Approximately 24.02%
```

Sparse storage was retained because the one-hot encoded matrix contains many zero values.

---

## 9. Rare-Category Handling

### Output

- Features containing grouped infrequent categories: **14**
- Total infrequent category levels grouped: **22**

### Examples

| Feature | Categories Grouped |
|---|---:|
| discharge_disposition_id | 5 |
| chlorpropamide | 2 |
| acarbose | 2 |
| miglitol | 2 |
| glyburide-metformin | 2 |
| gender | 1 |

Rare categories were grouped based only on training data.

---

## 10. Preprocessing Metadata and Reports Saved

### Preprocessing Metadata

```text
artifacts/preprocessing_metadata.json
```

Stores:

- Random seed
- Target and patient-group columns
- Numeric and categorical feature lists
- Preprocessing configuration
- Rare-category threshold
- Split sizes
- Target rates
- Prediction timing
- Important modeling rules

### Transformed Feature Names

```text
reports/modeling/transformed_feature_names.csv
```

Contains all **179 transformed feature names**.

### Rare-Category Summary

```text
reports/modeling/rare_category_summary.csv
```

Contains the category counts and grouped infrequent levels for all **35 categorical predictors**.

### Preprocessing Validation Summary

```text
reports/modeling/preprocessing_validation_summary.csv
```

Contains transformed shapes, sparsity, density, and invalid-value checks.

---

## 11. Final Notebook 3 Validation

### Final Results

| Check | Result |
|---|---:|
| Full dataset rows | 99,343 |
| Unique patients | 69,990 |
| Raw predictors | 43 |
| Numeric predictors | 8 |
| Categorical predictors | 35 |
| Transformed predictors | 179 |
| Train encounters | 69,467 |
| Validation encounters | 14,900 |
| Test encounters | 14,976 |
| Train patients | 48,993 |
| Validation patients | 10,498 |
| Test patients | 10,499 |
| Patient overlap | 0 |
| Missing raw values | 0 |
| Non-finite transformed values | 0 |
| Saved output files | 6 |

All final checks passed.

### Completion Summary File

```text
reports/modeling/notebook_3_completion_summary.csv
```

---

## Key Findings

1. The dataset was successfully divided into leakage-free patient-level train, validation, and test sets.
2. No patient appeared in more than one partition.
3. The target distribution remained stable across all three partitions.
4. The exact split assignments were saved and should not be regenerated.
5. The approved 43 predictors were preserved:
   - 8 numeric
   - 35 categorical
6. The preprocessing workflow was fitted using training data only.
7. The 43 raw predictors expanded to 179 transformed predictors.
8. Validation and test data produced the same 179-column structure.
9. No missing, infinite, or invalid transformed values were found.
10. Fourteen categorical features contained rare levels that were grouped using the minimum-frequency rule.
11. `discharge_disposition_id` remained categorical because prediction timing is defined as hospital discharge.
12. The test set remains untouched and must not be used for model selection, tuning, or threshold selection.

---

## Important Rules for the Next Notebook

1. Use the saved patient-level split assignments.
2. Do not regenerate the train, validation, and test partitions.
3. Attach preprocessing directly to each classifier using a pipeline.
4. Fit preprocessing only within training workflows.
5. Use validation data for model comparison.
6. Keep test data untouched until final model evaluation.
7. Apply class weighting or resampling only to training data.
8. Do not use accuracy alone because the positive-class rate is approximately 11.39%.
9. Prioritize:
   - Recall
   - Precision
   - F1-score
   - PR-AUC
   - ROC-AUC
   - Balanced accuracy
   - Confusion matrix
10. Do not include `encounter_id` or `patient_nbr` as predictors.

---
# Notebook 4 Summary — Baseline Models

## Notebook Name

`04_baseline_models.ipynb`

## Objective

The objective of Notebook 4 was to establish baseline classification models for predicting 30-day hospital readmission using the fixed patient-level train, validation, and test partitions created in Notebook 3.

The notebook focused on:

- Reusing the saved patient-level splits without regenerating them.
- Rebuilding the preprocessing pipeline using training data only.
- Training simple and interpretable baseline models.
- Evaluating models on the validation set.
- Comparing performance using metrics appropriate for an imbalanced target.
- Keeping the test set completely untouched.

---

## 1. Loaded Saved Project Artifacts

The following files were loaded:

```text
data/processed/diabetic_modeling_data_final.csv
data/processed/model_feature_schema.json
data/processed/patient_split_assignments.csv
artifacts/preprocessing_metadata.json
```

### Results

- Dataset shape: **99,343 rows × 46 columns**
- Missing values: **0**
- Target variable: `readmitted_30`
- Split-assignment shape: **99,343 rows × 4 columns**
- All required project files were found successfully.
- The notebook automatically detected the project root because the working directory was the `notebooks` folder.

---

## 2. Validated the Saved Patient-Level Splits

The existing split assignments from Notebook 3 were reused. No new splits were generated.

| Partition | Encounters | Patients | Positive rate |
|---|---:|---:|---:|
| Training | 69,467 | 48,993 | 11.424% |
| Validation | 14,900 | 10,498 | 11.275% |
| Test | 14,976 | 10,499 | 11.338% |

### Validation checks completed

- Every encounter matched one saved split assignment.
- No duplicate `encounter_id` values were found.
- Patient and target values matched between the dataset and split file.
- Train-validation patient overlap: **0**
- Train-test patient overlap: **0**
- Validation-test patient overlap: **0**
- `encounter_id`, `patient_nbr`, and `readmitted_30` were excluded from predictors.
- The test set remained untouched.

---

## 3. Rebuilt the Preprocessing Pipeline

The preprocessing decisions from Notebook 3 were recreated.

### Numeric preprocessing

1. Median imputation
2. Standard scaling

### Categorical preprocessing

1. Most-frequent imputation
2. Conversion of categorical values to strings
3. Rare-category grouping
4. One-hot encoding
5. Safe handling of unseen categories

### Results

- Numeric predictors: **8**
- Categorical predictors: **35**
- Total raw predictors: **43**
- Transformed predictors: **179**
- Rare-category minimum frequency: **10**
- Training matrix shape: **69,467 × 179**
- Validation matrix shape: **14,900 × 179**
- No missing or infinite transformed values were found.
- The preprocessor was fitted only on the training set.
- Validation data used the fitted transformation rules only.
- Test data was not transformed.

### Issue corrected

Some categorical variables contained integer values, while rare categories were replaced with the string `__RARE__`. This caused a mixed integer/string encoding error.

The issue was fixed by converting all categorical values to strings before rare-category grouping and one-hot encoding.

---

## 4. Models Evaluated

Four baseline models were trained and evaluated:

1. Dummy Classifier
2. Unweighted Logistic Regression
3. Class-Weighted Logistic Regression
4. Class-Weighted Decision Tree

All models were trained on the training partition and evaluated on the validation partition only.

---

## 5. Dummy Classifier Results

The Dummy Classifier used:

```text
strategy = most_frequent
```

It predicted every encounter as not readmitted.

### Confusion matrix

```text
[[13220     0]
 [ 1680     0]]
```

| Result | Count |
|---|---:|
| True negatives | 13,220 |
| False positives | 0 |
| False negatives | 1,680 |
| True positives | 0 |

### Metrics

| Metric | Result |
|---|---:|
| Accuracy | 88.72% |
| Balanced accuracy | 50.00% |
| Precision | 0.00% |
| Recall | 0.00% |
| Specificity | 100.00% |
| F1 score | 0.00% |
| ROC-AUC | 50.00% |
| PR-AUC | 11.28% |

### Interpretation

The model achieved high accuracy only because most encounters were not readmitted. It failed to detect all **1,680 actual readmissions**.

This confirmed that accuracy alone is misleading for this imbalanced dataset.

---

## 6. Unweighted Logistic Regression Results

### Model configuration

- L2 regularization
- `C = 1.0`
- `class_weight = None`
- Solver: `liblinear`
- Decision threshold: `0.50`
- Iterations: **15**
- Training time: approximately **2.28 seconds**

### Confusion matrix

```text
[[13197    23]
 [ 1647    33]]
```

| Result | Count |
|---|---:|
| True negatives | 13,197 |
| False positives | 23 |
| False negatives | 1,647 |
| True positives | 33 |

### Metrics

| Metric | Result |
|---|---:|
| Accuracy | 88.79% |
| Balanced accuracy | 50.90% |
| Precision | 58.93% |
| Recall | 1.96% |
| Specificity | 99.83% |
| F1 score | 3.80% |
| ROC-AUC | 66.73% |
| PR-AUC | 22.59% |

### Interpretation

The model showed useful ranking ability through its ROC-AUC and PR-AUC, but the default threshold was too conservative.

It detected only **33 of 1,680 readmissions** and missed **1,647 readmissions**.

---

## 7. Class-Weighted Logistic Regression Results

### Model configuration

- L2 regularization
- `C = 1.0`
- `class_weight = balanced`
- Solver: `liblinear`
- Decision threshold: `0.50`
- Iterations: **8**
- Training time: approximately **5.13 seconds**

### Confusion matrix

```text
[[9046 4174]
 [ 746  934]]
```

| Result | Count |
|---|---:|
| True negatives | 9,046 |
| False positives | 4,174 |
| False negatives | 746 |
| True positives | 934 |

### Metrics

| Metric | Result |
|---|---:|
| Accuracy | 66.98% |
| Balanced accuracy | 62.01% |
| Precision | 18.29% |
| Recall | 55.60% |
| Specificity | 68.43% |
| F1 score | 27.52% |
| ROC-AUC | 66.94% |
| PR-AUC | 22.59% |

### Interpretation

Class weighting substantially improved the model’s ability to detect readmissions.

- True positives increased from **33 to 934**.
- False negatives decreased from **1,647 to 746**.
- Recall increased from **1.96% to 55.60%**.
- F1 score increased from **3.80% to 27.52%**.

The trade-off was an increase in false positives and a decrease in overall accuracy and precision.

---

## 8. Class-Weighted Decision Tree Results

### Model configuration

- Criterion: Gini
- Maximum depth: **6**
- Minimum samples per split: **100**
- Minimum samples per leaf: **50**
- `class_weight = balanced`
- Actual tree depth: **6**
- Number of leaves: **54**
- Training time: approximately **0.85 seconds**

### Confusion matrix

```text
[[8386 4834]
 [ 674 1006]]
```

| Result | Count |
|---|---:|
| True negatives | 8,386 |
| False positives | 4,834 |
| False negatives | 674 |
| True positives | 1,006 |

### Metrics

| Metric | Result |
|---|---:|
| Accuracy | 63.03% |
| Balanced accuracy | 61.66% |
| Precision | 17.23% |
| Recall | 59.88% |
| Specificity | 63.43% |
| F1 score | 26.76% |
| ROC-AUC | 65.69% |
| PR-AUC | 20.79% |

### Interpretation

The decision tree achieved the highest recall among the baseline models.

It detected **1,006 of 1,680 readmissions** and missed **674**.

However, it produced more false positives and had lower precision, F1 score, ROC-AUC, and PR-AUC than the class-weighted logistic regression.

---

## 9. Final Baseline Model Comparison

| Model | Accuracy | Balanced Accuracy | Precision | Recall | F1 | ROC-AUC | PR-AUC |
|---|---:|---:|---:|---:|---:|---:|---:|
| Class-Weighted Logistic Regression | 66.98% | **62.01%** | **18.29%** | 55.60% | **27.52%** | **66.94%** | **22.59%** |
| Class-Weighted Decision Tree | 63.03% | 61.66% | 17.23% | **59.88%** | 26.76% | 65.69% | 20.79% |
| Unweighted Logistic Regression | 88.79% | 50.90% | 58.93% | 1.96% | 3.80% | 66.73% | 22.59% |
| Dummy Classifier | 88.72% | 50.00% | 0.00% | 0.00% | 0.00% | 50.00% | 11.28% |

---

## 10. ROC and Precision-Recall Curve Findings

### ROC-AUC ranking

1. Class-Weighted Logistic Regression: **0.669**
2. Unweighted Logistic Regression: **0.667**
3. Class-Weighted Decision Tree: **0.657**
4. Dummy Classifier: **0.500**

### PR-AUC ranking

1. Class-Weighted Logistic Regression: **0.226**
2. Unweighted Logistic Regression: **0.226**
3. Class-Weighted Decision Tree: **0.208**
4. Dummy Classifier: **0.113**

The validation positive-class prevalence was **11.28%**.

Both logistic regression models achieved a PR-AUC of approximately **22.6%**, which was about twice the validation prevalence and showed useful predictive signal.

The weighted and unweighted logistic models had similar ROC-AUC and PR-AUC values because class weighting mainly changed the classification threshold behavior rather than patient-risk ranking.

---

## 11. Provisional Leading Baseline

The provisional leading baseline model was:

```text
Class-Weighted Logistic Regression
```

It was selected because it achieved the best overall combination of:

- Balanced accuracy
- F1 score
- ROC-AUC
- PR-AUC
- Recall
- Lower false-positive count than the decision tree

The decision tree had higher recall, but the weighted logistic regression provided the stronger overall balance.

This model is only the best baseline model and is not yet the final project model.

---

## 12. Saved Outputs

### Saved models

```text
models/notebook_4_fitted_preprocessor.joblib
models/notebook_4_dummy_classifier.joblib
models/notebook_4_logistic_unweighted.joblib
models/notebook_4_logistic_class_weighted.joblib
models/notebook_4_decision_tree_class_weighted.joblib
```

### Saved metrics and metadata

```text
outputs/metrics/notebook_4_baseline_model_comparison.csv
outputs/metrics/notebook_4_completion_summary.csv
artifacts/notebook_4_baseline_metadata.json
```

### Saved figures

```text
outputs/figures/notebook_4_baseline_roc_curves.png
outputs/figures/notebook_4_baseline_precision_recall_curves.png
outputs/figures/notebook_4_baseline_metric_comparison.png
```

---

## 13. Notebook 4 Final Conclusion

Notebook 4 successfully established the project’s baseline performance.

The results showed that:

- Accuracy alone was not appropriate because of the imbalanced target.
- The unweighted logistic model was too conservative at the default threshold.
- Class weighting greatly improved readmission detection.
- The decision tree provided higher recall but produced more false positives.
- The class-weighted logistic regression was the strongest overall baseline.
- The available predictors provided useful but moderate predictive signal.
- More advanced nonlinear and ensemble models should be evaluated next.
- The test set remained completely untouched.

## Notebook 4 Status

```text
Complete
```

## Next Notebook

```text
05_candidate_models.ipynb
```

Notebook 5 will evaluate stronger candidate models such as Random Forest, Extra Trees, and gradient-boosting models while continuing to keep the test set untouched.

