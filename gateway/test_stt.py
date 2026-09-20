import requests
import os

url = "https://api.sarvam.ai/speech-to-text"
headers = {"api-subscription-key": "sk_b7zyfv59_q1pV0JXoTApKDUQ8oITKGtFK"}
files = {'file': ('question.webm', b"dummy audio content", 'audio/webm')}
data = {'language_code': "en-IN"}

try:
    print("Sending to Sarvam...")
    r = requests.post(url, headers=headers, files=files, data=data, timeout=15)
    print(f"Status Code: {r.status_code}")
    print(f"Response: {r.text}")
except Exception as e:
    print(f"Exception: {e}")
