"""
Shared helper functions used by every data collector script.

The core idea: we NEVER overwrite a historical data point. Government
data (especially GDP) gets revised after it's first published. So every
time we save a value, we check whether that date already has a value in
the file. If it does, we save the NEW value as a new row with a higher
revision_number, and keep the old row too.

Dashboards should always read the LATEST revision per date (see
load_latest() below) but the full revision history stays in the file
forever.
"""

import os
import pandas as pd
from datetime import datetime, timezone

COLUMNS = [
    "date", "indicator", "value", "unit",
    "release_date", "revision_number", "source", "downloaded_at"
]


def save_observation(filepath, date, indicator, value, unit, release_date, source):
    """
    Append one data point to a processed CSV, handling revisions correctly.

    filepath      - e.g. "data/processed/gdp.csv"
    date          - the period this number describes, e.g. "2026-01-01" for Q1 2026
    indicator     - short code, e.g. "GDP_GROWTH_YOY"
    value         - the number itself, e.g. 7.2
    unit          - e.g. "percent", "USD_billion", "INR"
    release_date  - when the government published THIS value, e.g. "2026-05-31"
    source        - e.g. "RBI", "MoSPI", "data.gov.in"

    Returns True if a new row was written, False if this exact value for
    this exact date was already saved (no duplicate rows).
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    if os.path.exists(filepath):
        df = pd.read_csv(filepath)
    else:
        df = pd.DataFrame(columns=COLUMNS)

    existing = df[(df["date"] == date) & (df["indicator"] == indicator)]

    if len(existing) > 0:
        # Has this exact value already been recorded for this date? Skip duplicate.
        last = existing.sort_values("revision_number").iloc[-1]
        if float(last["value"]) == float(value):
            return False
        next_revision = int(last["revision_number"]) + 1
    else:
        next_revision = 0

    new_row = {
        "date": date,
        "indicator": indicator,
        "value": value,
        "unit": unit,
        "release_date": release_date,
        "revision_number": next_revision,
        "source": source,
        "downloaded_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(filepath, index=False)
    return True


def load_latest(filepath):
    """
    Read a processed CSV and return only the latest revision of each date.
    This is what the dashboard should use for charts.
    """
    if not os.path.exists(filepath):
        return pd.DataFrame(columns=COLUMNS)

    df = pd.read_csv(filepath, parse_dates=["date", "release_date"])
    df = df.sort_values(["date", "revision_number"])
    latest = df.groupby("date", as_index=False).tail(1)
    return latest.sort_values("date").reset_index(drop=True)
