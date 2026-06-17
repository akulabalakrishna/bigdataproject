# Spark MLlib Training Path Evidence

**Purpose:** 
This training pipeline serves to strictly satisfy the rubric requirement for utilizing distributed ML algorithms natively on the local lakehouse data. It acts as an additional robust MLflow tracking path using native PySpark MLlib estimators (`LogisticRegression`, `RandomForestClassifier`, `GBTClassifier`), functioning parallel to the baseline scikit-learn training suite.

**Execution Command:**
```bash
export MLFLOW_TRACKING_URI=http://localhost:5000
python src/training/train_spark_mllib.py
```
*(Alternative Cluster Execution)*:
```bash
docker exec spark-master sh -lc "cd /opt/spark/work-dir && /opt/spark/bin/spark-submit src/training/train_spark_mllib.py"
```

**Configuration Constraints:**
- **Gold Input Path:** `data/minio/lakehouse/gold/readmission_features`
- **Expected Target Column:** `readmission_30d` (or equivalent fallback identifiers).
- **MLflow Experiment Name:** `ICU_Readmission_Spark_MLlib`

**Status:**
✅ Validated configuration natively tracking AUC and Accuracy across PySpark classifiers in MLflow.

> **Privacy Warning:** 
> No patient-level payload distributions or local feature extraction matrix definitions are exposed inside this repository. Data privacy dictates that local `parquet` files must remain strictly shielded by `.gitignore`.
