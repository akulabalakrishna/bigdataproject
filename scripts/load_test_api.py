import requests
import time
import json
import numpy as np

def run_load_test():
    url = "http://localhost:3002/predict"
    payload_path = "examples/readmission_prediction_payload.json"
    n_requests = 10

    with open(payload_path, 'r') as f:
        payload = json.load(f)

    print(f"Starting 10x load test on {url}")
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
            
            latency = end_req - start_req
            print(f"Request {i+1}: Status {response.status_code}, Time {latency*1000:.2f}ms")
            print(f"Response: {response.text}")
            
            if response.status_code == 200:
                success_count += 1
                latencies.append(latency)
            else:
                failure_count += 1
                
        except Exception as e:
            print(f"Request {i+1} failed: {e}")
            failure_count += 1

    end_total = time.time()

    with open("reports/api_10x_load_test_evidence.md", "w") as f:
        f.write("\n" + "="*40 + "\n")
        f.write("LOAD TEST RESULTS\n")
        f.write("="*40 + "\n")
        f.write(f"Total Requests:   {n_requests}\n")
        f.write(f"Success Count:    {success_count}\n")
        f.write(f"Failure Count:    {failure_count}\n")
        
        if latencies:
            f.write(f"Average Latency:  {np.mean(latencies)*1000:.2f} ms\n")
        
        f.write("="*40 + "\n")
    print("Test complete. Results saved to reports/api_10x_load_test_evidence.md")

if __name__ == "__main__":
    run_load_test()
