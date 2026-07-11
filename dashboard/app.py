"""
India Macro Terminal — Streamlit Dashboard

This reads the processed CSVs (created by the scripts/collect_*.py
files) and displays them. It does NOT fetch any data itself — that's
the collectors' job, run on a schedule by GitHub Actions.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import streamlit as st
import pandas as pd
from utils import load_latest

st.set_page_config(page_title="India Macro Terminal", layout="wide", page_icon="🇮🇳")

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")

st.title("🇮🇳 India Macro Terminal")
st.caption("Data from RBI, data.gov.in, and market sources · Updated daily via GitHub Actions")

tab1, tab2, tab3 = st.tabs(["Overview", "Policy Rates", "Market Data"])

# ---------- OVERVIEW ----------
with tab1:
    col1, col2 = st.columns(2)

    rates_file = os.path.join(DATA_DIR, "rbi_policy_rates.csv")
    if os.path.exists(rates_file):
        rates = load_latest(rates_file)
        with col1:
            st.subheader("Current Policy Rates")
            for _, row in rates.iterrows():
                st.metric(row["indicator"].replace("_", " ").title(), f"{row['value']}%")
    else:
        with col1:
            st.info("No policy rate data yet — run `scripts/collect_rbi_rates.py`.")

    market_file = os.path.join(DATA_DIR, "market_data.csv")
    if os.path.exists(market_file):
        market = load_latest(market_file)
        with col2:
            st.subheader("Latest Market Snapshot")
            for _, row in market.iterrows():
                st.metric(row["indicator"].replace("_", " ").title(), f"{row['value']:,}")
    else:
        with col2:
            st.info("No market data yet — run `scripts/collect_market_data.py`.")

# ---------- POLICY RATES ----------
with tab2:
    st.subheader("RBI Policy Rates — History")
    if os.path.exists(rates_file):
        rates = load_latest(rates_file)
        for indicator in rates["indicator"].unique():
            subset = rates[rates["indicator"] == indicator].sort_values("date")
            st.write(f"**{indicator.replace('_', ' ').title()}**")
            st.line_chart(subset.set_index("date")["value"])
    else:
        st.info("No data yet.")

# ---------- MARKET DATA ----------
with tab3:
    st.subheader("Market Data — History")
    if os.path.exists(market_file):
        market = load_latest(market_file)
        for indicator in market["indicator"].unique():
            subset = market[market["indicator"] == indicator].sort_values("date")
            st.write(f"**{indicator.replace('_', ' ').title()}**")
            st.line_chart(subset.set_index("date")["value"])
    else:
        st.info("No data yet.")

st.divider()
st.caption("Built with Streamlit · Data sources: RBI, data.gov.in, Yahoo Finance")
