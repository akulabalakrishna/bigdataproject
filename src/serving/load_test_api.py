import requests
import time
import json
import numpy as np
import argparse

def run_load_test(url, n_requests):
    # Sample data matching Gold features
    payload = {
        "AGE": 65,
        "GENDER": "M",
        "ADMISSION_TYPE": "EMERGENCY",
        "INSURANCE": "Medicare",
        "RELIGION": "CATHOLIC",
        "MARITAL_STATUS": "MARRIED",
        "ETHNICITY": "WHITE",
        "DIAG_COUNT": 8,
        "PROC_COUNT": 3,
        "AVG_ICU_LOS": 4.5,
        "ICU_STAY_COUNT": 1
    }

    print(f"Starting load test on {url}")
    print(f"Sending {n_requests} requests...")

    latencies = []
    success_count = 0
    failure_count = 0

    start_total = time.time()
    for i in range(n_requests):
        try:
            start_req = time.time()
            response = requests.post(url, json=payload, timeout=5)
            end_req = time.time()
            
            if response.status_code == 200:
                success_count += 1
                latencies.append(end_req - start_req)
            else:
                failure_count += 1
                
            if (i + 1) % 10 == 0:
                print(f"Completed {i+1}/{n_requests} requests...")
        except Exception as e:
            print(f"Request {i+1} failed: {e}")
            failure_count += 1

    end_total = time.time()

    print("\n" + "="*40)
    print("LOAD TEST RESULTS")
    print("="*40)
    print(f"Total Requests:   {n_requests}")
    print(f"Success Count:    {success_count}")
    print(f"Failure Count:    {failure_count}")
    
    if latencies:
        print(f"Average Latency:  {np.mean(latencies)*1000:.2f} ms")
        print(f"P95 Latency:      {np.percentile(latencies, 95)*1000:.2f} ms")
        print(f"Max Latency:      {np.max(latencies)*1000:.2f} ms")
    
    print(f"Total Duration:   {end_total - start_total:.2f} seconds")
    print(f"Throughput:       {success_count / (end_total - start_total):.2f} req/sec")
    print("="*40)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://localhost:3000/predict", help="BentoML predict URL")
    parser.add_argument("--n", type=int, default=100, help="Number of requests")
    args = parser.parse_args()
    
    run_load_test(args.url, args.n)
