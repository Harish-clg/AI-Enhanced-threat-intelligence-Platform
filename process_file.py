import requests
import json
import pandas as pd
from ml_module import predict_threat  

splunk_hec_url = "your splunk url"
splunk_hec_token = "your hec token"
file_path="D:/hackcode/data"
def send_to_splunk(event):
    headers = {
        'Authorization': f'Splunk {splunk_hec_token}',
        'Content-Type': 'application/json'
    }
    response = requests.post(splunk_hec_url, headers=headers, data=json.dumps(event))
    if response.status_code == 200:
        print("Data sent to Splunk successfully.")
    else:
        print(f"Failed to send data to Splunk. Status code: {response.status_code}")

def process_and_send(file_path):
   
    data = pd.read_csv(file_path, encoding='ISO-8859-1')
    # Preprocess and predict
    threat = predict_threat(data)
    event = {
        "event": {
            "file": file_path,
            "predicted_threat": threat
        }
    }
    send_to_splunk(event)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: process_file.py <file_path>")
        sys.exit(1)
    file_path = sys.argv[1]
    process_and_send(file_path)
