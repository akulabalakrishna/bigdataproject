import pandas as pd
import numpy as np
import mlflow
import mlflow.sklearn
import mlflow.xgboost
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import os
import joblib
import pyarrow.parquet as pq
import sys

import pandas as pd
import numpy as np
import mlflow
import mlflow.sklearn
import mlflow.xgboost
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, 
    roc_auc_score, confusion_matrix, average_precision_score
)
import matplotlib.pyplot as plt
import seaborn as sns
import os
import joblib
import pyarrow.parquet as pq
import sys

def train():
    # Configuration
    MLFLOW_URI = "http://localhost:5000"
    GOLD_DATA_PATH = "E:/Z5008_Readmission_Project/data/gold/mimiciii/READMISSION_FEATURES"
    MODELS_DIR = "E:/Z5008_Readmission_Project/models"
    
    os.makedirs(MODELS_DIR, exist_ok=True)

    # Set MLflow tracking URI and check availability
    mlflow_enabled = False
    try:
        mlflow.set_tracking_uri(MLFLOW_URI)
        mlflow.set_experiment("ICU_Real_Readmission_Enhanced")
        mlflow_enabled = True
        print(f"MLflow connected at {MLFLOW_URI}. Logging enabled.")
    except Exception as e:
        print("="*60)
        print(f"WARNING: MLflow unavailable. Training will continue locally.")
        print("="*60)

    # Load Gold Data
    if not os.path.exists(GOLD_DATA_PATH):
        print(f"CRITICAL ERROR: Gold data not found at {GOLD_DATA_PATH}")
        sys.exit(1)

    print(f"Loading REAL Gold data from {GOLD_DATA_PATH}...")
    df = pq.read_table(GOLD_DATA_PATH).to_pandas()
    
    if len(df) == 0:
        print("ERROR: Gold dataset is empty.")
        sys.exit(1)

    # Preprocessing
    X = df.drop(['READMISSION_30', 'SUBJECT_ID', 'HADM_ID'], axis=1, errors='ignore')
    y = df['READMISSION_30']

    # Imbalance calculation for XGBoost
    neg_count = (y == 0).sum()
    pos_count = (y == 1).sum()
    scale_pos_weight = neg_count / pos_count if pos_count > 0 else 1.0

    print(f"Class imbalance: {neg_count} neg / {pos_count} pos (Ratio: {scale_pos_weight:.2f})")

    categorical_cols = X.select_dtypes(include=['object']).columns.tolist()
    numerical_cols = X.select_dtypes(include=['int32', 'int64', 'float32', 'float64']).columns.tolist()

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_cols),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
        ])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # Models definition
    models_config = {
        "LogisticRegression": {
            "model": LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42),
            "params": {}
        },
        "RandomForest": {
            "model": RandomForestClassifier(n_estimators=100, class_weight="balanced", random_state=42),
            "params": {}
        },
        "XGBoost": {
            "model": xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss', scale_pos_weight=scale_pos_weight, random_state=42),
            "params": {
                "classifier__n_estimators": [100, 200],
                "classifier__max_depth": [3, 5],
                "classifier__learning_rate": [0.05, 0.1],
                "classifier__subsample": [0.8, 1.0]
            }
        }
    }

    results = []
    best_overall_f1 = 0
    best_model_data = None

    for name, config in models_config.items():
        print(f"\n--- Training {name} ---")
        
        pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                                  ('classifier', config['model'])])
        
        # Hyperparameter Tuning for XGBoost (or others if params provided)
        if config['params']:
            print(f"Running GridSearchCV for {name}...")
            search = GridSearchCV(pipeline, config['params'], cv=3, scoring='f1', n_jobs=-1)
            search.fit(X_train, y_train)
            best_pipeline = search.best_estimator_
            best_params = search.best_params_
            print(f"Best Params: {best_params}")
        else:
            best_pipeline = pipeline.fit(X_train, y_train)
            best_params = config['model'].get_params()

        # Predictions
        y_prob = best_pipeline.predict_proba(X_test)[:, 1]
        
        # Threshold Tuning
        thresholds = np.linspace(0.1, 0.9, 81)
        best_threshold = 0.5
        max_f1 = 0
        
        for t in thresholds:
            y_temp = (y_prob >= t).astype(int)
            f1 = f1_score(y_test, y_temp, zero_division=0)
            if f1 > max_f1:
                max_f1 = f1
                best_threshold = t
        
        y_pred = (y_prob >= best_threshold).astype(int)
        
        # Metrics
        metrics = {
            "accuracy": accuracy_score(y_test, y_pred),
            "precision": precision_score(y_test, y_pred, zero_division=0),
            "recall": recall_score(y_test, y_pred, zero_division=0),
            "f1": f1_score(y_test, y_pred, zero_division=0),
            "roc_auc": roc_auc_score(y_test, y_prob),
            "pr_auc": average_precision_score(y_test, y_prob)
        }
        
        metrics["best_threshold"] = best_threshold
        results.append({"model": name, **metrics})

        # MLflow Logging
        if mlflow_enabled:
            with mlflow.start_run(run_name=f"Enhanced_{name}"):
                mlflow.log_params(best_params)
                mlflow.log_param("best_threshold", best_threshold)
                mlflow.log_metrics(metrics)
                mlflow.sklearn.log_model(best_pipeline, "model")

        # Update best overall
        if metrics["f1"] > best_overall_f1:
            best_overall_f1 = metrics["f1"]
            best_model_data = {
                "name": name,
                "pipeline": best_pipeline,
                "threshold": best_threshold,
                "metrics": metrics
            }

        print(f"Best Threshold: {best_threshold:.2f} | F1: {metrics['f1']:.4f} | ROC-AUC: {metrics['roc_auc']:.4f}")

    # Display Comparison Table
    print("\n" + "="*85)
    print(f"{'Model':<20} | {'Acc':<6} | {'Prec':<6} | {'Rec':<6} | {'F1':<6} | {'AUC':<6} | {'PR-AUC':<6} | {'Thresh':<6}")
    print("-" * 85)
    for res in results:
        print(f"{res['model']:<20} | {res['accuracy']:<6.3f} | {res['precision']:<6.3f} | {res['recall']:<6.3f} | {res['f1']:<6.3f} | {res['roc_auc']:<6.3f} | {res['pr_auc']:<6.3f} | {res['best_threshold']:<6.2f}")
    print("="*85)

    # Save Best Model Package
    if best_model_data:
        model_save_path = os.path.join(MODELS_DIR, "best_readmission_model.joblib")
        joblib.dump({
            "pipeline": best_model_data["pipeline"],
            "threshold": best_model_data["threshold"],
            "model_name": best_model_data["name"]
        }, model_save_path)
        print(f"\nFINAL BEST MODEL: {best_model_data['name']}")
        print(f"Saved to: {model_save_path}")

        # Register model in MLflow if enabled
        if mlflow_enabled:
            print(f"Registering model '{best_model_data['name']}' in MLflow Registry...")
            try:
                # We need to start a run to register the model if not using log_model(..., registered_model_name=...)
                with mlflow.start_run(run_name="Register_Best_Model"):
                    mlflow.log_params(best_model_data["metrics"])
                    mlflow.sklearn.log_model(
                        sk_model=best_model_data["pipeline"],
                        artifact_path="model",
                        registered_model_name="ICU_Readmission_XGBoost_Real"
                    )
                print("Successfully registered model: ICU_Readmission_XGBoost_Real")
            except Exception as e:
                print(f"Warning: Model registration failed: {e}")

if __name__ == "__main__":
    train()




