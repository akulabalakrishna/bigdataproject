import pandas as pd
import pytest

def calculate_readmission_pandas(df):
    """
    Simulates the readmission logic from src/spark_jobs/gold_job.py using Pandas
    instead of PySpark to avoid Java dependencies during local unit testing.
    """
    # Sort by SUBJECT_ID and ADMITTIME
    df = df.sort_values(by=['SUBJECT_ID', 'ADMITTIME']).reset_index(drop=True)
    
    # Calculate NEXT_ADMITTIME per subject
    df['NEXT_ADMITTIME'] = df.groupby('SUBJECT_ID')['ADMITTIME'].shift(-1)
    
    # Calculate days to next admit
    df['DAYS_TO_NEXT_ADMIT'] = (df['NEXT_ADMITTIME'] - df['DISCHTIME']).dt.days
    
    # Assign READMISSION_30 label
    # Condition: DAYS_TO_NEXT_ADMIT <= 30 and >= 0
    mask = (df['DAYS_TO_NEXT_ADMIT'] <= 30) & (df['DAYS_TO_NEXT_ADMIT'] >= 0)
    df['READMISSION_30'] = mask.astype(int)
    
    return df

def test_readmission_logic():
    data = [
        {"SUBJECT_ID": "P1", "ADMITTIME": "2020-01-01", "DISCHTIME": "2020-01-10"},
        {"SUBJECT_ID": "P1", "ADMITTIME": "2020-01-20", "DISCHTIME": "2020-01-25"}, # Readmitted in 10 days
        {"SUBJECT_ID": "P2", "ADMITTIME": "2020-01-01", "DISCHTIME": "2020-01-05"},
        {"SUBJECT_ID": "P2", "ADMITTIME": "2020-03-01", "DISCHTIME": "2020-03-05"}, # Readmitted in ~55 days
    ]
    df = pd.DataFrame(data)
    df['ADMITTIME'] = pd.to_datetime(df['ADMITTIME'])
    df['DISCHTIME'] = pd.to_datetime(df['DISCHTIME'])
    
    result = calculate_readmission_pandas(df)
    
    # First admission for P1
    assert result.loc[0, 'READMISSION_30'] == 1
    # Second admission for P1
    assert result.loc[1, 'READMISSION_30'] == 0
    # First admission for P2
    assert result.loc[2, 'READMISSION_30'] == 0
