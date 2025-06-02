
# KAREN V7 + EARLYBIRDX + NOVA - LAUNCH STARTUP SCRIPT
# Author: Nova for Karen V7 Ops
# Purpose: Initialize, run, and sync full system with live market data

import streamlit as st
import pandas as pd
import requests
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")

# Streamlit UI setup
st.set_page_config(page_title="Karen V7 AI Terminal", layout="wide")
st.title("🧠 KAREN V7: AI STOCK COMMAND CENTER")
st.sidebar.title("Nova Command Panel")

# Live scan logic using Polygon snapshot endpoint
def earlybirdx_scan():
    url = f"https://api.polygon.io/v2/snapshot/locale/us/markets/stocks/tickers?apiKey={POLYGON_API_KEY}"
    try:
        response = requests.get(url)
        data = response.json().get("tickers", [])
        movers = []
        for stock in data:
            change = stock["day"]["change"]
            volume = stock["day"]["volume"]
            if change >= 0.05 and volume >= 500000:
                movers.append({
                    "Ticker": stock["ticker"],
                    "Change %": round(change * 100, 2),
                    "Last Price": stock["lastTrade"]["p"],
                    "Volume": volume
                })
        df = pd.DataFrame(movers).sort_values("Change %", ascending=False).head(10)
        return df
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()

# Karen prediction logic (placeholder)
def karen_predictions(live_data):
    predictions = []
    for _, row in live_data.iterrows():
        confidence = 75 + (row["Change %"] % 25)
        buy_low = round(row["Last Price"] * 0.95, 2)
        buy_high = round(row["Last Price"] * 0.98, 2)
        target = round(row["Last Price"] * 1.2, 2)
        predictions.append({
            "ticker": row["Ticker"],
            "confidence": int(confidence),
            "buy_zone": f"{buy_low}-{buy_high}",
            "target_exit": f"{target}"
        })
    return predictions

# Nova chat logic
def nova_respond(prompt):
    return f"[Nova] You said: {prompt}"

# View selector
selected_view = st.sidebar.radio("Choose View", ["Live Scans", "Karen’s Calls", "Nova Chat"])

if selected_view == "Live Scans":
    st.header("📡 EARLYBIRDX SCANNER (Live Market Data)")
    scan_results = earlybirdx_scan()
    if not scan_results.empty:
        st.dataframe(scan_results)
    else:
        st.warning("No movers found or market closed.")

elif selected_view == "Karen’s Calls":
    st.header("🧬 KAREN V7 STRATEGY CALLS (Live Predictions)")
    scan_results = earlybirdx_scan()
    predictions = karen_predictions(scan_results) if not scan_results.empty else []
    for pred in predictions:
        st.metric(label=pred['ticker'], value=f"{pred['confidence']}% Confidence",
                  delta=f"Buy Zone: {pred['buy_zone']} | Target: {pred['target_exit']}")

elif selected_view == "Nova Chat":
    st.header("🤖 NOVA COMMAND CONSOLE")
    user_input = st.text_input("Enter command or question for Nova:")
    if user_input:
        response = nova_respond(user_input)
        st.markdown(f"**Nova:** {response}")
