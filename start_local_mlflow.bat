@echo off
SET PROJECT_ROOT=E:\Z5008_Readmission_Project
SET SCRIPTS_PATH=C:\Users\HP\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\Scripts
SET PATH=%SCRIPTS_PATH%;%PATH%

SET DB_PATH=sqlite:///E:/Z5008_Readmission_Project/mlflow_data/mlflow_fresh.db
SET ARTIFACT_PATH=file:///E:/Z5008_Readmission_Project/mlflow_data/mlruns

echo ============================================================
echo Starting MLflow Local Server (Batch Mode)
echo Store: %DB_PATH%
echo Artifacts: %ARTIFACT_PATH%
echo URL: http://127.0.0.1:5000
echo ============================================================

mlflow server ^
    --backend-store-uri %DB_PATH% ^
    --default-artifact-root %ARTIFACT_PATH% ^
    --host 127.0.0.1 ^
    --port 5000

pause
