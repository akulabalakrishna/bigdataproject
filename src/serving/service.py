import bentoml
from bentoml.io import JSON
import pandas as pd
import numpy as np
import joblib
import os
import traceback

# Configuration
MODEL_PATH = "E:/Z5008_Readmission_Project/models/best_readmission_model.joblib"

# Load model package safely
print(f"Loading model from {MODEL_PATH}...")
try:
    package = joblib.load(MODEL_PATH)
    if isinstance(package, dict):
        model = package.get("model") or package.get("pipeline") or package.get("best_model")
        threshold = package.get("threshold", 0.5)
        model_name = package.get("model_name", "XGBoost")
    else:
        model = package
        threshold = 0.5
        model_name = "XGBoost"
    
    if model is None:
        raise ValueError("Could not find a valid model or pipeline in the joblib package.")
        
    print(f"Model '{model_name}' loaded successfully with threshold {threshold}")
except Exception as e:
    print(f"CRITICAL ERROR loading model: {e}")
    traceback.print_exc()
    model = None

svc = bentoml.Service("icu_readmission_service")

@svc.api(input=JSON(), output=JSON())
async def predict(input_data):
    """
    Predict 30-day readmission probability using real MIMIC-III trained model.
    """
    if model is None:
        return {
            "status": "error",
            "message": "Model not loaded on server."
        }

    try:
        # Convert input JSON to DataFrame
        df = pd.DataFrame([input_data])
        
        # Required fields check and pre-processing
        required_numeric = [
            "AGE", "DIAG_COUNT", "PROC_COUNT", "AVG_ICU_LOS", "ICU_STAY_COUNT"
        ]
        required_categorical = [
            "GENDER", "ADMISSION_TYPE", "INSURANCE", "RELIGION", "MARITAL_STATUS", "ETHNICITY"
        ]
        
        # Fill missing values
        for col in required_numeric:
            if col not in df.columns:
                df[col] = 0
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
        for col in required_categorical:
            if col not in df.columns:
                df[col] = "UNKNOWN"
            df[col] = df[col].astype(str).fillna("UNKNOWN")

        # Keep only required columns in the expected order if the pipeline requires it
        # (Though scikit-learn pipelines usually handle column selection if configured)
        
        # Run prediction
        risk_score = float(model.predict_proba(df)[0][1])
        prediction = int(risk_score >= threshold)
        
        return {
            "risk_score": risk_score,
            "prediction": prediction,
            "threshold": float(threshold),
            "model_name": model_name,
            "status": "success"
        }
        
    except Exception as e:
        print(f"Error during prediction: {e}")
        traceback.print_exc()
        return {
            "status": "error",
            "message": str(e),
            "traceback": traceback.format_exc() if os.environ.get("DEBUG") else "Internal Server Error"
        }


