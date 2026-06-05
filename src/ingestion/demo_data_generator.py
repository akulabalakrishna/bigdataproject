import pandas as pd
import numpy as np
import os
import gzip

def generate_demo_data():
    base_path = "E:/Z5008_Readmission_Project/data/raw/mimiciii/"
    os.makedirs(base_path, exist_ok=True)
    
    # Patients
    patients = pd.DataFrame({
        'SUBJECT_ID': range(1, 101),
        'GENDER': np.random.choice(['M', 'F'], 100),
        'DOB': pd.date_range(start='1940-01-01', periods=100, freq='Y'),
        'EXPIRE_FLAG': np.random.choice([0, 1], 100, p=[0.8, 0.2])
    })
    
    # Admissions
    admissions = pd.DataFrame({
        'SUBJECT_ID': np.random.randint(1, 101, 200),
        'HADM_ID': range(1000, 1200),
        'ADMITTIME': pd.to_datetime('2020-01-01') + pd.to_timedelta(np.random.randint(0, 365, 200), unit='D'),
        'DISCHTIME': None,
        'DEATHTIME': None,
        'ADMISSION_TYPE': np.random.choice(['EMERGENCY', 'ELECTIVE', 'URGENT'], 200),
        'ADMISSION_LOCATION': 'EMERGENCY ROOM',
        'DISCHARGE_LOCATION': 'HOME',
        'INSURANCE': 'Medicare',
        'LANGUAGE': 'ENGL',
        'RELIGION': 'NOT SPECIFIED',
        'MARITAL_STATUS': 'MARRIED',
        'ETHNICITY': 'WHITE',
        'DIAGNOSIS': 'PNEUMONIA',
        'HAS_CHARTEVENTS_DATA': 1
    })
    admissions['DISCHTIME'] = admissions['ADMITTIME'] + pd.to_timedelta(np.random.randint(1, 15, 200), unit='D')
    
    # Save as .csv.gz
    files = {
        'PATIENTS.csv.gz': patients,
        'ADMISSIONS.csv.gz': admissions
    }
    
    for filename, df in files.items():
        path = os.path.join(base_path, filename)
        df.to_csv(path, index=False, compression='gzip')
        print(f"Generated demo {filename}")

if __name__ == "__main__":
    generate_demo_data()
