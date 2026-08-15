import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("CALLE_API_KEY")
BASE_URL = "https://api.heycall-e.com"

call_id = input("Paste CALL-E call id: ").strip()

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

call = requests.get(
    f"{BASE_URL}/v1/calls/{call_id}",
    headers=headers,
    timeout=30
)

events = requests.get(
    f"{BASE_URL}/v1/calls/{call_id}/events",
    headers=headers,
    timeout=30
)

print("\nCALL:\n")
print(call.text)

print("\nEVENTS:\n")
print(events.text)