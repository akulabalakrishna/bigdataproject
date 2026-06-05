import os
import subprocess
import sys

def start_mlflow():
    # Configuration
    SCRIPTS_PATH = r"C:\Users\HP\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\LocalCache\local-packages\Python310\Scripts"
    PROJECT_ROOT = "E:/Z5008_Readmission_Project"
    MLFLOW_DATA = os.path.join(PROJECT_ROOT, "mlflow_data")
    DB_PATH = f"sqlite:///{MLFLOW_DATA}/mlflow_fresh.db"
    ARTIFACT_PATH = f"file:///{MLFLOW_DATA}/mlruns"
    
    # Ensure data directory exists
    os.makedirs(MLFLOW_DATA, exist_ok=True)
    os.makedirs(os.path.join(MLFLOW_DATA, "mlruns"), exist_ok=True)

    # Update PATH for the child process
    env = os.environ.copy()
    env["PATH"] = SCRIPTS_PATH + os.pathsep + env["PATH"]

    cmd = [
        "mlflow", "server",
        "--backend-store-uri", DB_PATH,
        "--default-artifact-root", ARTIFACT_PATH,
        "--host", "127.0.0.1",
        "--port", "5000"
    ]

    print("="*60)
    print(f"Starting MLflow Local Server on Windows...")
    print(f"Store: {DB_PATH}")
    print(f"Artifacts: {ARTIFACT_PATH}")
    print(f"URL: http://127.0.0.1:5000")
    print("="*60)
    print("Press Ctrl+C to stop the server.")

    try:
        subprocess.run(cmd, env=env, check=True)
    except KeyboardInterrupt:
        print("\nMLflow server stopped by user.")
    except Exception as e:
        print(f"\nError starting MLflow server: {e}")

if __name__ == "__main__":
    start_mlflow()
