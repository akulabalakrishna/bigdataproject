# MLflow 5-Runs Evidence

The MLflow tracking server successfully tracked training for 5 unique models:
- LogisticRegression
- RandomForest
- DecisionTree
- GaussianNB
- GradientBoosting

**Tracking Server URL:**
`http://localhost:5000`

**Experiment:**
`ICU_Real_Readmission_Enhanced`

**Best Model Results:**
The `LogisticRegression` model proved best according to the hyperparameter grid search (threshold 0.60):
- F1: 0.1767
- ROC-AUC: 0.6680

**Registry and Artifacts:**
- The best pipeline was registered into the MLflow model registry as `ICU_Readmission_Real_Model`.
- The physical artifact was cleanly exported to: `models/best_readmission_model.joblib`.
