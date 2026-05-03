import json

import requests

# 🚨 CHANGE THIS URL if your Ollama server is remote 🚨
API_URL = "http://localhost:11434/api/generate"

# The prompt you want to send
prompt = "Explain the concept of large language models in three sentences."

headers = {"Content-Type": "application/json"}

data = {
    "model": "gemma4:e4b",  # Specify which model you want to use
    "prompt": prompt,
    "stream": False,
}

try:
    # Make the POST request to the API endpoint
    response = requests.post(API_URL, headers=headers, data=json.dumps(data))
    response.raise_for_status()  # Checks for bad status codes

    # Print the generated content
    result = response.json()
    print("Response:", result["response"])

except requests.exceptions.RequestException as e:
    print(f"Error connecting to the API: {e}")
    print("Please ensure the Ollama server is running on the specified URL.")
