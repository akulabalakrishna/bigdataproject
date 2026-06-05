import pytest
import sys
import os
import asyncio
from unittest.mock import patch

# Ensure src can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@patch('joblib.load')
def test_bento_prediction_preprocessing(mock_load):
    # Setup mock
    class MockModel:
        def predict_proba(self, df):
            return [[0.1, 0.9]] # mock high risk
    
    mock_load.return_value = {"model": MockModel(), "threshold": 0.5, "model_name": "Mock"}
    
    # Import service after patching
    import src.serving.service as service_module
    
    # Overwrite the global model in module (in case it failed to load during import)
    service_module.model = MockModel()
    service_module.threshold = 0.5
    
    input_data = {
        "AGE": 45,
        "GENDER": "M"
    }
    
    # Run async function
    result = asyncio.run(service_module.predict(input_data))
    
    assert result["status"] == "success"
    assert "risk_score" in result
    assert result["prediction"] == 1
