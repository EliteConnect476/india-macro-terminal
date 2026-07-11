# India Macro Terminal — Setup Guide (No Coding Required)

Everything below happens through websites (GitHub.com and Streamlit's
website). You will never need to install Python, open a terminal, or
type a command. Follow the steps in order.

---

## Part 1 — Put this project on GitHub

GitHub is where your project "lives" — it stores your files and lets
the automatic daily updates run in the cloud (not on your computer).

1. Go to **github.com** and click **Sign up** if you don't have an account.
2. Once logged in, click the **+** icon top-right → **New repository**.
3. Name it `india-macro-terminal`. Leave it **Public**. Click **Create repository**.
4. On the new repo's page, click **uploading an existing file** (a link
   in the middle of the page).
5. Drag and drop **every file and folder** from this project into that
   upload box — keep the folder structure exactly as it is (the
   `scripts/`, `dashboard/`, `data/`, and `.github/` folders all need
   to come along, not just the files inside them).
6. Scroll down, click **Commit changes**.

Your project is now live on GitHub. GitHub Actions (the automatic
scheduler) is enabled by default — nothing more to do for that part.

---

## Part 2 — Get a free data.gov.in API key (optional, for government datasets)

Only needed if you want to pull datasets from data.gov.in (GST
collections, exports, etc). Skip this if you just want RBI rates + market data for now.

1. Go to **data.gov.in** → **Sign Up** → make a free account.
2. Log in, go to your profile → you'll see your **API Key**. Copy it.
3. Back on your GitHub repo page, click **Settings** (top menu of the repo) → **Secrets and variables** → **Actions** → **New repository secret**.
4. Name: `DATA_GOV_API_KEY`. Value: paste your key. Click **Add secret**.

---

## Part 3 — Deploy the dashboard (make it viewable as a website)

1. Go to **share.streamlit.io** and click **Sign in with GitHub** (use
   the same GitHub account from Part 1).
2. Click **Create app** → **From existing repo**.
3. Pick your `india-macro-terminal` repository.
4. In "Main file path", type: `dashboard/app.py`
5. Click **Deploy**.

After a minute or two, you'll get a public URL (something like
`your-name-india-macro-terminal.streamlit.app`) — that's your live
dashboard. Bookmark it.

---

## Part 4 — Confirm the automatic updates are working

1. On your GitHub repo page, click the **Actions** tab.
2. You should see a workflow called **Update Macro Data**.
3. Click **Run workflow** (top right) to trigger it manually the first
   time, rather than waiting for tomorrow's scheduled run.
4. After ~1 minute, refresh the page — you should see a green checkmark.
5. Go back to your Streamlit dashboard URL and refresh — you should see
   fresh data.

From here on, it runs automatically every day at 9 AM IST with no
action from you. If a run ever fails, GitHub emails the account owner
automatically.

---

## Updating RBI rates when they change

RBI's policy rates (repo rate, etc.) only change 4-6 times a year, after
each Monetary Policy Committee meeting — so this is done manually, not
automatically (see the comment at the top of
`scripts/collect_rbi_rates.py` for why).

When the RBI announces a new rate:

1. On GitHub, open `scripts/collect_rbi_rates.py` in your repo.
2. Click the pencil icon (top right of the file view) to edit it.
3. Find the `CURRENT_RATES` section and update the `value` and
   `effective_date` for whichever rate changed.
4. Scroll down, click **Commit changes**.
5. Go to the **Actions** tab → run the workflow manually once (Part 4,
   step 3) so the new rate shows up immediately instead of waiting for
   tomorrow.

---

## Adding a new data.gov.in dataset later

1. Go to **data.gov.in**, search for what you want, open the dataset,
   click the **API** tab — copy the `resource_id` shown there.
2. Edit `scripts/collect_data_gov.py` on GitHub (same pencil-icon method
   as above) and add an entry to the `DATASETS` dictionary, following
   the example pattern already commented in the file.
3. Commit changes. It'll be picked up on the next scheduled run.

---

## What's actually happening behind the scenes

- **Every day at 9 AM IST**, GitHub runs three small Python scripts
  in the cloud (not your computer) that fetch the latest RBI rates,
  market prices, and any data.gov.in datasets you've configured.
- New numbers are added to CSV files in `data/processed/` — old
  numbers are **never deleted**, even when a figure like GDP gets
  revised later. Every version is kept.
- The dashboard (`dashboard/app.py`) just reads those CSV files and
  draws charts. It doesn't fetch anything itself.
- Streamlit Cloud automatically redeploys your dashboard whenever the
  GitHub repo changes, so your live URL always reflects the latest data.

## File-by-file reference

| File | What it does |
|---|---|
| `scripts/utils.py` | Shared logic — saves data points without overwriting history |
| `scripts/collect_market_data.py` | Pulls Nifty, USD/INR, Gold, Crude, VIX from Yahoo Finance |
| `scripts/collect_rbi_rates.py` | Records current RBI policy rates (manually updated when they change) |
| `scripts/collect_data_gov.py` | Template for pulling datasets from data.gov.in's API |
| `dashboard/app.py` | The Streamlit dashboard itself |
| `.github/workflows/update_data.yml` | The schedule — runs the collectors daily |
| `data/processed/*.csv` | Where all the collected data actually lives |
