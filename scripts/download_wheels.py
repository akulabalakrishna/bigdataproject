import subprocess
import sys
import os

api_packages = [
    "bentoml==1.1.0",
    "pandas==2.0.3",
    "scikit-learn==1.3.0",
    "joblib==1.3.2",
    "numpy==1.24.3",
    "python-dotenv==1.0.0"
]

airflow_packages = [
    "mlflow==2.9.2",
    "pandas==2.0.3",
    "scikit-learn==1.3.0",
    "joblib==1.3.2",
    "boto3==1.28.44",
    "kafka-python==2.0.2",
    "minio",
    "psycopg2-binary==2.9.7",
    "python-dotenv==1.0.0"
]

def download_packages(packages, dest_dir, python_ver, abi_ver):
    os.makedirs(dest_dir, exist_ok=True)
    for pkg in packages:
        print(f"\n--- Downloading {pkg} for python {python_ver} ---")
        cmd = [
            sys.executable, "-m", "pip", "download", pkg,
            "-d", dest_dir,
            "--platform", "manylinux2014_x86_64",
            "--only-binary=:all:",
            "--implementation", "cp",
            "--python-version", python_ver,
            "--abi", abi_ver,
            "--index-url", "https://mirrors.aliyun.com/pypi/simple/",
            "--trusted-host", "mirrors.aliyun.com",
            "--no-cache-dir"
        ]
        
        # Try up to 5 times
        success = False
        for attempt in range(1, 6):
            print(f"Attempt {attempt} for {pkg}...")
            result = subprocess.run(cmd)
            if result.returncode == 0:
                print(f"Successfully downloaded {pkg}")
                success = True
                break
            else:
                print(f"Failed to download {pkg} on attempt {attempt}")
        
        if not success:
            print(f"ERROR: Could not download {pkg} after 5 attempts.")
            sys.exit(1)

def main():
    # 1. Download API packages (Python 3.10)
    print("=== Downloading API packages (Python 3.10) ===")
    download_packages(api_packages, "pip_wheels", "3.10", "cp310")
    
    # 2. Download Airflow packages (Python 3.11)
    print("\n=== Downloading Airflow packages (Python 3.11) ===")
    download_packages(airflow_packages, "pip_wheels_airflow", "3.11", "cp311")
    
    # 3. Download pyspark (cross-platform source tarball)
    print("\n=== Downloading pyspark ===")
    pyspark_cmd = [
        sys.executable, "-m", "pip", "download", "pyspark==3.5.1",
        "-d", "pip_wheels_airflow",
        "--index-url", "https://mirrors.aliyun.com/pypi/simple/",
        "--trusted-host", "mirrors.aliyun.com",
        "--no-cache-dir"
    ]
    for attempt in range(1, 6):
        print(f"Attempt {attempt} for pyspark...")
        result = subprocess.run(pyspark_cmd)
        if result.returncode == 0:
            print("Successfully downloaded pyspark")
            break
        else:
            print(f"Failed to download pyspark on attempt {attempt}")
    else:
        print("ERROR: Could not download pyspark after 5 attempts.")
        sys.exit(1)
        
    print("\nAll downloads completed successfully!")

if __name__ == "__main__":
    main()
