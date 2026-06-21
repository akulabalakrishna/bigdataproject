# Spark MLlib Compliance Training Evidence

This report documents the execution and verification details of the Spark MLlib training pipeline as required by strict grading guidelines.

## 1. Spark MLlib Training Runs in MLflow

**Experiment Name:** `ICU_Readmission_SparkML_Compliance` (Experiment ID: `2`)
**MLflow Tracking URI:** `http://mlflow:5000`

### Training Runs Logged

| Run Name | Run ID | Status | Key Metrics |
| :--- | :--- | :--- | :--- |
| **SparkML_LogisticRegression** | `9ad47caa3e13470fb72717356d36f4a8` | FINISHED | Accuracy: `0.7885`<br>Precision: `0.0987`<br>Recall: `0.3190`<br>F1 Score: `0.1507` (threshold 0.07)<br>ROC-AUC: `0.6305`<br>PR-AUC: `0.0959`<br>Duration: `37.83s` |
| **SparkML_RandomForest** | `806a1ecac1014638a0c5b454b9ab294b` | FINISHED | Accuracy: `0.8551`<br>Precision: `0.1312`<br>Recall: `0.2604`<br>F1 Score: `0.1745` (threshold 0.07)<br>ROC-AUC: `0.6617`<br>PR-AUC: `0.1459`<br>Duration: `28.32s` |
| **Register_Best_SparkML** | `9a5faf0908d7456fb58ceac16c768123` | FINISHED | Registers best model (**RandomForest**) into MLflow registry |

---

## 2. MLflow Model Registry Details

- **Registered Model Name:** `ICU_Readmission_SparkML_Model`
- **Latest Version:** Version `1`
- **Source Artifact Path:** Registered dynamically via `mlflow.spark.log_model()`

---

## 3. Saved Models on Local Filesystem

The models have been saved locally in Spark ML writeable format:

* **Logistic Regression:** `models/spark_mllib/logisticregression`
* **Random Forest (Best model):** `models/spark_mllib/randomforest`

---

## 4. Verification Command & Verification Outputs

To verify the runs, the following command was executed in the `airflow-scheduler` container:
```powershell
docker exec airflow-scheduler python -c "import mlflow; mlflow.set_tracking_uri('http://mlflow:5000'); e=[x for x in mlflow.search_experiments() if x.name=='ICU_Readmission_SparkML_Compliance'][0]; d=mlflow.search_runs(experiment_ids=[e.experiment_id]); print(d[['run_id','status','tags.mlflow.runName']].to_string())"
```

Output:
```text
                             run_id    status         tags.mlflow.runName
0  9a5faf0908d7456fb58ceac16c768123  FINISHED       Register_Best_SparkML
1  806a1ecac1014638a0c5b454b9ab294b  FINISHED        SparkML_RandomForest
2  9ad47caa3e13470fb72717356d36f4a8  FINISHED  SparkML_LogisticRegression
```

To verify the Model Registry:
```powershell
docker exec airflow-scheduler python -c "import mlflow; mlflow.set_tracking_uri('http://mlflow:5000'); c=mlflow.tracking.MlflowClient(); print([(m.name,[v.version for v in m.latest_versions]) for m in c.search_registered_models()])"
```

Output:
```text
[('ICU_Readmission_Real_Model', ['1']), ('ICU_Readmission_SparkML_Model', ['1'])]
```
