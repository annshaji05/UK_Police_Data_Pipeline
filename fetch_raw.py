import requests
import json
from datetime import datetime
import os
import time

# Make sure a "raw_data" folder exists to store untouched API responses
os.makedirs("raw_data", exist_ok=True)

# The 4 London areas we chose, each with genuinely different crime profiles
LOCATIONS = {
    "westminster": {"lat": "51.5074", "lng": "-0.1278"},
    "city_of_london": {"lat": "51.5155", "lng": "-0.0922"},
    "hackney": {"lat": "51.5450", "lng": "-0.0553"},
    "richmond": {"lat": "51.4613", "lng": "-0.3037"},
}

# The last 3 months known to have data available (checked earlier via
# the crimes-street-dates endpoint)
MONTHS = ["2026-05", "2026-06", "2026-07"]

url = "https://data.police.uk/api/crimes-street/all-crime"

for area_name, coords in LOCATIONS.items():
    for month in MONTHS:
        params = {
            "lat": coords["lat"],
            "lng": coords["lng"],
            "date": month
        }

        response = requests.get(url, params=params)
        print(f"{area_name} | {month} | Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"raw_data/crimes_{area_name}_{month}_{timestamp}.json"

            with open(filename, "w") as f:
                json.dump(data, f, indent=2)

            print(f"  Saved {len(data)} records to {filename}")
        else:
            print(f"  Failed: {response.text}")

        time.sleep(1)

print("\nAll done fetching raw data.")