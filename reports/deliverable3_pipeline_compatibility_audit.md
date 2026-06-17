# Deliverable 3 Pipeline Compatibility Audit

This document summarizes the pipeline compatibility following the fast-run optimizations for the local MIMIC-III dataset.

## 1. Bronze Fast-Run Design
To accommodate the strict performance constraints, the Bronze job has been configured to write out 23 fast tables using `inferSchema=false`. This configuration stores all column data uniformly as strings, bypassing Spark's schema inference step. This substantially reduces memory overhead and processing time during the initial data ingestion into the MinIO lakehouse bucket.

## 2. Deferred Large-Table Explanation
The largest MIMIC-III tables (`CHARTEVENTS`, `NOTEEVENTS`, `PROCEDUREEVENTS_MV`) have been intentionally deferred. These files consist of tens of millions of rows, which would artificially bottleneck the Bronze execution during local demonstrations. By deferring them, the pipeline completes rapidly while still allowing for robust predictive modeling on standard clinical dimensions.

## 3. Silver/Gold Compatibility with String Schemas
Because the Bronze layer saves columns as strings, downstream pipelines required patching to ensure numeric and date properties remain mathematically valid:
* **Silver Job (`silver_job.py`)**: Dynamically iterates through all available tables in the `lakehouse/bronze/mimiciii` bucket. Key temporal columns (e.g., `ADMITTIME`, `DISCHTIME`, `DOB`, `DOD`) are explicitly cast to timestamps using `to_timestamp()` before saving to Silver. It gracefully ignores deferred tables that are absent.
* **Gold Job (`gold_job.py`)**: Explicitly casts string metrics (such as the `LOS` column in `ICUSTAYS`) to `float` prior to numerical aggregations (e.g., `avg()`). Optional feature blocks (`PRESCRIPTIONS` and `LABEVENTS`) dynamically integrate count metrics if the tables are found in the Silver layer, seamlessly handling missing datasets without failing. The job ensures a clean machine-learning-ready dataset is exported to `lakehouse/gold/readmission_features`.

## 4. MLflow 5-Run Requirement
The final machine learning pipeline (`train.py`) executes 5 distinct model runs to satisfy Deliverable 3 requirements:
1. Logistic Regression
2. Random Forest
3. XGBoost
4. Decision Tree
5. GaussianNB

The preprocessing steps use dynamic schema detection (`X.select_dtypes`) and `handle_unknown='ignore'` via `OneHotEncoder`. This ensures model training remains robust, irrespective of whether the upstream optional tables (like `LABEVENTS` or `PRESCRIPTIONS`) are populated in the feature matrix.

## 5. Raw Data Privacy Note
Strict adherence to raw data privacy is maintained. The complete dataset remains safely located at `E:\Z5008_Readmission_Project\data\raw\mimiciii` and is strictly ignored by Git via `.gitignore`. The data is neither copied unnecessarily nor checked into version control.
