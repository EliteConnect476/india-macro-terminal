"""
RBI policy rates (Repo Rate, SDF, MSF, Bank Rate, CRR, SLR).

WHY THIS ONE ISN'T FULLY AUTOMATED:
Unlike Yahoo Finance or data.gov.in, RBI does not publish these rates
through a stable, machine-readable API. Their website's page layout
changes over time, so an automated scraper here would silently break
every few months without you knowing — which is worse than no
automation at all for numbers this important.

The good news: these rates only change 4-6 times a year (after each
Monetary Policy Committee meeting), so manual updates are genuinely
fine. This script does NOT fetch anything automatically. Instead, it
holds the CURRENT known values as of when this project was set up.
When the RBI announces a new rate (check https://www.rbi.org.in or any
financial news site), update the CURRENT_RATES dictionary below and
run this script once — it'll add the new revision automatically using
the same revision-tracking logic as everything else.

You do NOT need to know how to code to do this — see the README
section "Updating RBI rates when they change" for the exact steps
using GitHub's website only.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from utils import save_observation

OUTPUT_FILE = "data/processed/rbi_policy_rates.csv"

# Update these values whenever the RBI MPC announces a change.
# effective_date = the date the new rate took effect (from the RBI press release)
CURRENT_RATES = {
    "REPO_RATE":    {"value": 5.25, "effective_date": "2025-12-05"},
    "SDF_RATE":     {"value": 5.00, "effective_date": "2025-12-05"},
    "MSF_RATE":     {"value": 5.50, "effective_date": "2025-12-05"},
    "BANK_RATE":    {"value": 5.50, "effective_date": "2025-12-05"},
}


def run():
    for indicator, info in CURRENT_RATES.items():
        saved = save_observation(
            filepath=OUTPUT_FILE,
            date=info["effective_date"],
            indicator=indicator,
            value=info["value"],
            unit="percent",
            release_date=info["effective_date"],
            source="RBI",
        )
        status = "saved new value" if saved else "already up to date"
        print(f"[{status}] {indicator}: {info['value']}%")


if __name__ == "__main__":
    run()
