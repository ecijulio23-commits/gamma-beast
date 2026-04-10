import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# Safe import for Polygon
try:
    from polygon import RESTClient
    POLYGON_AVAILABLE = True
except ImportError:
    POLYGON_AVAILABLE = False
    RESTClient = None

st.set_page_config(page_title="GammaFlow Beast", layout="wide", page_icon="⚫", initial_sidebar_state="expanded")

# Singularity Dark Theme
st.markdown("""
<style>
    .stApp { background: #05050a; color: #e0e0e0; }
    .main-header {
        font-size: 3.8rem; font-weight: 900;
        background: linear-gradient(90deg, #ffffff, #a0f0ff);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-align: center; text-shadow: 0 0 40px rgba(160, 240, 255, 0.5);
        letter-spacing: -2px;
    }
    .glass-card {
        background: rgba(15, 15, 25, 0.95); border: 1px solid #333333;
        border-radius: 18px; padding: 20px; margin: 10px 0;
        box-shadow: 0 0 25px rgba(0,0,0,0.7);
    }
    .metric {
        background: #111111; border: 1px solid #222;
        border-radius: 12px; padding: 15px; text-align: center;
    }
    .heatmap-title { color: #ffffff; font-size: 1.7rem; text-align: center; margin: 15px 0; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">GAMMAFLOW BEAST</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; color:#888; font-size:1.2rem;">SINGULARITY TERMINAL • REAL-TIME GAMMA + VIX CONFLUENCE</p>', unsafe_allow_html=True)

# Sidebar
st.sidebar.title("⚫ CONTROL PANEL")
polygon_key = st.sidebar.text_input("Polygon API Key", value="GZXb1Zay2Xzt6DISycHpV_aqqdlwrQ9_", type="password")

st.sidebar.subheader("Watchlist")
watchlist = st.sidebar.multiselect("Tickers", 
    ["META", "NVDA", "TSLA", "AAPL", "AMD", "GOOGL", "AMZN", "SPY"],
    default=["SPY", "GOOGL", "NVDA"])

view_mode = st.sidebar.radio("Heatmap View", ["Single Ticker", "All Tickers Combined"])

if st.sidebar.button("REFRESH TERMINAL", type="primary", use_container_width=True):
    st.rerun()

# Initialize client safely
client = None
if polygon_key and POLYGON_AVAILABLE:
    try:
        client = RESTClient(api_key=polygon_key)
        st.sidebar.success("✅ Polygon connected (free tier)")
    except Exception as e:
        st.sidebar.error(f"Polygon connection failed: {str(e)[:100]}")
else:
    if not POLYGON_AVAILABLE:
        st.sidebar.error("⚠️ polygon-api-client not installed. Check requirements.txt")
    else:
        st.sidebar.warning("Enter Polygon key for real data")

# Rest of the app (metrics, tabs, etc.) remains the same as the previous version I sent

# ... (copy the rest of the code from my previous message: metrics, tabs, beast alerts, gamma heatmap, vix signals, live flow)

st.caption("GammaFlow Beast • Singularity Mode • Powered by Polygon")
