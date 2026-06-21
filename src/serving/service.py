import bentoml
from bentoml.io import JSON
import pandas as pd
import numpy as np
import joblib
import os
import traceback

# Configuration — use env var set in docker-compose, fallback for local dev
MODEL_PATH = os.environ.get("MODEL_PATH", "/opt/project/models/best_readmission_model.joblib")

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
        # Convert input dictionary/list to DataFrame
        if isinstance(input_data, dict):
            df = pd.DataFrame([input_data])
        elif isinstance(input_data, list):
            df = pd.DataFrame(input_data)
        else:
            raise ValueError("Input data must be a dictionary or a list of dictionaries.")

        # Run model prediction
        prob = np.asarray(model.predict_proba(df))[0, 1]
        prediction = int(prob >= threshold)
        
        return {
            "risk_score": float(prob),
            "prediction": prediction,
            "threshold": float(threshold),
            "model_name": str(model_name),
            "status": "success"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


