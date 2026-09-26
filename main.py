import requests
import pandas as pd

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
    df = pd.json_normalize(data)

    # only main columns and renamed to be cleaner
    df = df[[
        "category",
        "month",
        "location.latitude",
        "location.longitude",
        "location.street.name",
        "outcome_status.category"
    ]].rename(columns={
        "location.latitude": "latitude",
        "location.longitude": "longitude",
        "location.street.name": "street",
        "outcome_status.category": "outcome"
    })

    print("\nCleaned table preview:")
    print(df.head())

    print("\nCrime counts by category:")
    print(df["category"].value_counts())

    # Save to a CSV file
    df.to_csv("crimes_june_2026.csv", index=False)
    print("\nSaved to crimes_june_2026.csv")
else:
    print("Request failed. Response text:")
    print(response.text)