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

# Full MPC decision history, verified against RBI/PIB press releases and
# financial news coverage. Each entry is a real rate change announced at
# an actual MPC meeting. This gives the dashboard real history to chart
# instead of a single flat point.
#
# TO ADD A NEW RATE CHANGE: add one new entry per indicator at the bottom
# of RATE_HISTORY with the new value and effective_date, then run this
# script (or trigger the GitHub Action) once.
RATE_HISTORY = [
    # date,          REPO,  SDF,   MSF/Bank
    ("2023-02-08", 6.50, 6.25, 6.75),   # hiking cycle ends, held here till Feb 2025
    ("2025-02-07", 6.25, 6.00, 6.50),   # first cut in ~5 years
    ("2025-04-09", 6.00, 5.75, 6.25),
    ("2025-06-06", 5.50, 5.25, 5.75),   # 50bp cut, stance -> neutral
    ("2025-12-05", 5.25, 5.00, 5.50),   # current level (verified June 2026)
]


def run():
    for effective_date, repo, sdf, msf_bank in RATE_HISTORY:
        rates = {
            "REPO_RATE": repo,
            "SDF_RATE": sdf,
            "MSF_RATE": msf_bank,
            "BANK_RATE": msf_bank,
        }
        for indicator, value in rates.items():
            saved = save_observation(
                filepath=OUTPUT_FILE,
                date=effective_date,
                indicator=indicator,
                value=value,
                unit="percent",
                release_date=effective_date,
                source="RBI",
            )
            status = "saved" if saved else "already up to date"
            print(f"[{status}] {effective_date} {indicator}: {value}%")


if __name__ == "__main__":
    run()
