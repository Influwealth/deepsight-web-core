import os
import requests

# Load your Hugging Face API key
HUGGINGFACE_API_KEY = input("Enter your Hugging Face API key: ").strip()

# Define the API endpoint and test prompt
API_URL = "https://influwealth-deepsight-mistral7b.hf.space/api/predict"
prompt = "What are the risks of mining Kaspa?"

# Set up headers and payload
headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
payload = {"inputs": prompt}

try:
    print("Sending request to the Hugging Face API...")
    response = requests.post(API_URL, headers=headers, json=payload)

    # Check the response status
    if response.status_code == 200:
        print("âœ… API call successful!")
        print("Response:")
        print(response.json())
    else:
        print(f"âŒ Error: Received status code {response.status_code}")
        print("Response details:")
        print(response.text)
except Exception as e:
    print(f"âŒ Error during API call: {str(e)}")
