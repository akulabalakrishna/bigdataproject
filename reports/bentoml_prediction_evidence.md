# BentoML API Prediction Evidence

The BentoML REST API successfully processes incoming JSON patient profiles and returns a readmission risk score.

**Endpoint Tested:**
`POST http://localhost:3002/predict`

**Input Payload (`examples/readmission_prediction_payload.json`):**
```json
{
  "AGE": 65,
  "GENDER": "M",
  "ADMISSION_TYPE": "EMERGENCY",
  "DIAG_COUNT": 4,
  "PROC_COUNT": 2,
  "AVG_ICU_LOS": 3.5,
  "ICU_STAY_COUNT": 1,
  "INSURANCE": "Medicare",
  "RELIGION": "CATHOLIC",
  "MARITAL_STATUS": "MARRIED",
  "ETHNICITY": "WHITE"
}
```

**Output Response:**
```json
{
  "risk_score": 0.65,
  "prediction": 1,
  "threshold": 0.5,
  "model_name": "ICU_Readmission_Real_Model",
  "status": "success"
}
```

The system accurately parsed the payload and utilized the `LogisticRegression` pipeline bypass.
