import sys
import os
import json

# Add epvo_py to sys.path
sys.path.append(r"g:\Мой диск\Google AI Studio\AD ЕПВО\epvo_py")

from epvo_client import epvo_client
from config import config

def fetch_and_save(type_code, filename):
    print(f"Fetching {type_code}...")
    url = f"{epvo_client.base_url}/org-data/{type_code}/find-all-pageable"
    params = {
        "page": 0,
        "size": 10,
        "universityId": config.ISVUZ_USERNAME
    }
    
    import httpx
    with httpx.Client(timeout=30.0) as client:
        response = client.get(url, params=params, headers=epvo_client.headers)
        if response.status_code == 200:
            data = response.json()
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Saved to {filename}")
        else:
            print(f"Error {response.status_code}: {response.text}")

fetch_and_save("ACCREDITATION_AGENCIES", r"g:\Мой диск\Google AI Studio\ЕПВО\scratch\epvo_agencies.json")
fetch_and_save("UNIVERSITY_ACCREDITATION", r"g:\Мой диск\Google AI Studio\ЕПВО\scratch\epvo_university_acc.json")
