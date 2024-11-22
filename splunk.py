import requests
import json

splunk_hec_url = "your-splunk-server"
splunk_hec_token = "your_hec_token"

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

def process_and_send(sample_data):
    threat = predict_threat(sample_data)
    event = {
        "event": {
            "sample_data": sample_data.tolist(),
            "predicted_threat": threat
        }
    }
    send_to_splunk(event)
