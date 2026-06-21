# MLflow Final Evidence

## Experiment Details
- **Experiment Name:** `ICU_Real_Readmission_Enhanced`
- **Experiment ID:** `1`
- **Number of Successful Runs:** 6 (5 classifier training runs, 1 best model registration run)
- **Tracking URI:** `http://localhost:5000` (internal: `http://mlflow:5000`)
- **Storage:** MinIO (`http://localhost:9001`, internal bucket: `mlflow`)

## Model Performance Metrics

| Run / Model Name | Accuracy | Precision | Recall | F1 Score | ROC-AUC | PR-AUC | Best Threshold |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **GradientBoosting** (Best) | 0.8765 | 0.1492 | 0.2401 | **0.1841** | **0.6930** | 0.1427 | 0.10 |
| **RandomForest** | 0.8848 | 0.1543 | 0.2202 | 0.1815 | 0.6676 | 0.1456 | 0.14 |
| **LogisticRegression** | 0.7847 | 0.1110 | 0.3869 | 0.1725 | 0.6659 | 0.1089 | 0.58 |
| **DecisionTree** | 0.8967 | 0.1239 | 0.1284 | 0.1261 | 0.5362 | 0.0663 | 0.10 |
| **GaussianNB** | 0.0918 | 0.0594 | 0.9878 | 0.1121 | 0.5152 | 0.0597 | 0.87 |

## Registered Model Status
- **Registered Model Name:** `ICU_Readmission_Real_Model`
- **Latest Version:** `1`
- **Status:** Registered and ready for deployment.
- **Save Path for Production Model:** `E:/Z5008_Readmission_Project/models/best_readmission_model.joblib`

## Presentation Screenshot Instructions
To display MLflow during the live demonstration:
1. Open your browser and navigate to `http://localhost:5000`.
2. Select the experiment **`ICU_Real_Readmission_Enhanced`** from the left pane.
3. Show the runs list comparing the five algorithms with their metrics (Accuracy, F1, ROC-AUC).
4. Click on **Models** in the top navigation bar to display the registered model **`ICU_Readmission_Real_Model`** with Version 1.
