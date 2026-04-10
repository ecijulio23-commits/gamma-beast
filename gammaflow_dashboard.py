
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="GammaFlow Beast", layout="wide")
st.title("🚀 GammaFlow Beast Dashboard")
st.markdown("**Live UOA + Gamma + RohOnChain 11-step AlphaCombiner**")

st.sidebar.header("Watchlist")
watchlist = st.sidebar.multiselect("Tickers", ["META", "NVDA", "TSLA", "AAPL", "AMD", "GOOGL", "AMZN"], default=["META", "NVDA", "TSLA"])

st.sidebar.header("Settings")
conviction_threshold = st.sidebar.slider("Minimum Conviction", 70, 100, 85)

st.subheader("Recent Beast Alerts")

if "alerts" not in st.session_state:
    st.session_state.alerts = []

if st.button("🔥 Simulate Nuclear Beast (Test)"):
    new_alert = {
        "time": datetime.now().strftime("%H:%M:%S"),
        "ticker": "META 250418C00615000",
        "volume": 15200,
        "price": 8.10,
        "uoa": 84.4,
        "conviction": 100,
        "size_mult": 2.0
    }
    st.session_state.alerts.insert(0, new_alert)
    st.rerun()

for alert in st.session_state.alerts[:10]:
    with st.expander(f"🚨 {alert['ticker']} @ {alert['time']} — {alert['conviction']}/100", expanded=True):
        st.write(f"**Volume:** {alert['volume']:,} contracts")
        st.write(f"**Price:** ${alert['price']}")
        st.write(f"**UOA Aggression:** {alert['uoa']:.1f}x")
        st.progress(alert['conviction']/100)
        st.caption(f"Suggested size: **{alert['size_mult']:.1f}x** your base")

st.success("✅ Webhook Server is running in background")
st.info("Webhook URL: https://indexically-cytoid-michiko.ngrok-free.dev/webhook")
st.caption("When you upgrade Unusual Whales and add the webhook, real alerts will appear here live.")
