"""
Collects data from data.gov.in's open API.

SETUP REQUIRED (one-time, takes 2 minutes):
1. Go to https://data.gov.in/user/register and make a free account
2. After logging in, go to your profile page — you'll see an "API Key"
3. Copy that key and save it as a GitHub secret named DATA_GOV_API_KEY
   (instructions for this are in the main README)

HOW TO FIND A DATASET'S resource_id:
1. Go to https://data.gov.in and search for what you want (e.g. "GDP",
   "GST collection", "exports")
2. Open a dataset page. Click the "API" tab.
3. It shows you an example URL like:
   https://api.data.gov.in/resource/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
4. That XXXX...XXXX part is the resource_id — paste it into
   DATASETS below.

This script ships with ONE example wired up. Add more by copying the
pattern in DATASETS.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from utils import save_observation
import requests
from datetime import date

API_KEY = os.environ.get("DATA_GOV_API_KEY", "")

# Add datasets here as you find their resource_id on data.gov.in
DATASETS = {
    # "GST_COLLECTION": {
    #     "resource_id": "PASTE-RESOURCE-ID-HERE",
    #     "value_field": "gst_collection_crore",   # the column name in that dataset
    #     "date_field": "month",
    #     "unit": "INR_crore",
    # },
}

OUTPUT_FILE = "data/processed/data_gov_indicators.csv"


def fetch_dataset(resource_id, limit=10):
    url = f"https://api.data.gov.in/resource/{resource_id}"
    params = {"api-key": API_KEY, "format": "json", "limit": limit}
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json().get("records", [])


def run():
    if not API_KEY:
        print("[error] DATA_GOV_API_KEY is not set. See instructions at the top of this file.")
        return

    if not DATASETS:
        print("[info] No datasets configured yet. Add one to DATASETS in this file "
              "following the instructions in the docstring at the top.")
        return

    for indicator, config in DATASETS.items():
        try:
            records = fetch_dataset(config["resource_id"])
            if not records:
                print(f"[skip] No records for {indicator}")
                continue
            latest = records[0]  # data.gov.in usually returns most recent first
            save_observation(
                filepath=OUTPUT_FILE,
                date=latest[config["date_field"]],
                indicator=indicator,
                value=latest[config["value_field"]],
                unit=config["unit"],
                release_date=date.today().isoformat(),
                source="data.gov.in",
            )
            print(f"[saved] {indicator}: {latest[config['value_field']]}")
        except Exception as e:
            print(f"[error] {indicator}: {e}")


if __name__ == "__main__":
    run()
