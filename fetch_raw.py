import requests
import json
from datetime import datetime
import os

# Make sure a "raw_data" folder exists to store untouched API responses
os.makedirs("raw_data", exist_ok=True)

url = "https://data.police.uk/api/crimes-street/all-crime"
params = {
    "lat": "51.5074",
    "lng": "-0.1278",
    "date": "2026-06"
}

response = requests.get(url, params=params)

print("Status code:", response.status_code)

if response.status_code == 200:
    data = response.json()

    # Build a filename that includes today's date and time, so we never overwrite old raw data
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"raw_data/crimes_raw_{timestamp}.json"

    # Save the RAW, untouched response exactly as it came from the API
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Saved {len(data)} raw records to {filename}")
else:
    print("Request failed. Response text:")
    print(response.text)