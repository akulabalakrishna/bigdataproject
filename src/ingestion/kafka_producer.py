import time
import json
import pandas as pd
from kafka import KafkaProducer
import os

def json_serializer(data):
    return json.dumps(data).encode("utf-8")

def stream_admissions(limit=100):
    bootstrap_servers = ['localhost:9092']
    topic = 'mimic-admissions'
    
    print(f"Connecting to Kafka at {bootstrap_servers}...")
    try:
        producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=json_serializer,
            request_timeout_ms=10000,
            retry_backoff_ms=500
        )
        print(f"Connected to Kafka successfully.")
    except Exception as e:
        print(f"Failed to connect to Kafka: {e}")
        return
    
    raw_path = "E:/Z5008_Readmission_Project/data/raw/mimiciii/ADMISSIONS.csv.gz"
    
    if not os.path.exists(raw_path):
        print(f"Raw data not found at {raw_path}.")
        return

    # Select only privacy-safe columns for streaming demo
    safe_columns = [
        'HADM_ID', 'ADMISSION_TYPE', 'ADMITTIME', 'DISCHTIME', 
        'INSURANCE', 'RELIGION', 'MARITAL_STATUS', 'ETHNICITY', 'DIAGNOSIS'
    ]
    
    print(f"Reading real data from {raw_path}...")
    df = pd.read_csv(raw_path, compression='gzip', usecols=safe_columns, nrows=limit)
    
    print(f"Sending to topic: {topic}")
    print(f"Starting stream of {len(df)} safety-filtered records...")
    
    count = 0
    for _, row in df.iterrows():
        data = row.to_dict()
        
        # Ensure all data is JSON serializable
        for key in data:
            if pd.isna(data[key]):
                data[key] = None
            elif not isinstance(data[key], (str, int, float, bool, type(None))):
                data[key] = str(data[key])
        
        try:
            producer.send(topic, data)
            count += 1
            if count % 20 == 0:
                print(f"Sent {count} records successfully...")
        except Exception as e:
            print(f"Error sending record: {e}")
        
        time.sleep(0.05) # Simulate real-time delay
        
    producer.flush()
    print("="*60)
    print(f"STREAMING COMPLETE")
    print(f"Sent {count} records successfully to {topic}")
    print("="*60)

if __name__ == "__main__":
    stream_admissions(limit=100)

