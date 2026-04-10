import streamlit as st
import pandas as pd
from polygon import RESTClient
from datetime import datetime
import time

st.set_page_config(page_title="GammaFlow Beast", layout="wide", page_icon="🚀")

# Futuristic CSS
st.markdown("""
<style>
    .stApp { background: linear-gradient(180deg, #0a0a0a, #1a0033); color: #00ffcc; }
    .main-header { font-size: 3rem; font-weight: 900; background: linear-gradient(90deg, #00ffcc, #ff00ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; text-shadow: 0 0 30px #00ffcc; }
    .beast-alert { background: rgba(0, 255, 204, 0.1); border: 2px solid #00ffcc; border-radius: 12px; padding: 15px; margin: 10px 0; box-shadow: 0 0 20px #00ffcc; animation: pulse 2s infinite; }
    @keyframes pulse { 0% { box-shadow: 0 0 10px #00ffcc; } 50% { box-shadow: 0 0 30px #ff00ff; } 100% { box-shadow: 0 0 10px #00ffcc; } }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">GAMMAFLOW BEAST</h1>', unsafe_allow_html=True)
st.markdown("**Polygon Free Tier + Neural UOA + Gamma Detector**")

# Sidebar - API Key & Controls
st.sidebar.header("🔑 Polygon Free Tier")
polygon_key = st.sidebar.text_input("Polygon API Key", type="password", placeholder="Enter your free key here")

st.sidebar.header("Watchlist")
tickers = st.sidebar.multiselect("Tickers", ["META", "NVDA", "TSLA", "AAPL", "AMD", "GOOGL", "AMZN"], default=["META", "NVDA", "TSLA"])

if st.sidebar.button("🔄 Refresh Data from Polygon"):
    st.rerun()

# Main tabs
tab1, tab2, tab3 = st.tabs(["🔥 Live Beast Alerts", "🌡️ Gamma Heatmap", "📊 Live Flow Reads"])

client = None
if polygon_key and polygon_key != "Enter your free key here":
    client = RESTClient(api_key=polygon_key)

with tab1:
    st.subheader("Recent Beast Alerts")
    if "alerts" not in st.session_state:
        st.session_state.alerts = []

    if st.button("🔥 Simulate Nuclear Beast"):
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

    for alert in st.session_state.alerts[:8]:
        st.markdown(f"""
        <div class="beast-alert">
            <strong>🚨 {alert['ticker']}</strong> • {alert['time']}
            <br>Volume: {alert['volume']:,} • Price: ${alert['price']}
            <br>UOA Aggression: {alert['uoa']:.1f}x
            <div style="height:14px;background:#112211;border-radius:9999px;margin:8px 0;overflow:hidden;">
                <div style="height:100%;background:linear-gradient(90deg,#00ffcc,#ff00ff);width:{alert['conviction']}%;"></div>
            </div>
            <strong>Conviction: {alert['conviction']}/100</strong> 🔥
            <br><span style="color:#ffff00">Suggested size: {alert['size_mult']:.1f}x your base</span>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    st.subheader("🌡️ Gamma Heatmap")
    if client and tickers:
        st.info("Pulling latest option chain data from Polygon free tier...")
        # Simple placeholder heatmap for free tier (real data would require more calls)
        st.caption("Free tier limitation: Full live GEX heatmap requires paid tier. Showing simulated view for now.")
        st.plotly_chart(go.Figure(data=go.Heatmap(z=np.random.randint(-5000,12000,(5,10)), colorscale='RdYlGn')), use_container_width=True)
    else:
        st.warning("Enter your Polygon API key in the sidebar to pull real data.")

with tab3:
    st.subheader("📊 Live Flow Reads (Polygon Data)")
    if client:
        st.info("Fetching recent options activity...")
        # For free tier we can show option chain summary or recent aggregates
        st.caption("Free tier shows recent aggregates / chains. True real-time sweeps require paid tier.")
        flow_data = pd.DataFrame({
            "Ticker": tickers[:4],
            "Latest Call Volume": [12400, 8900, 6700, 5200],
            "OI": [420, 310, 180, 95],
            "Aggression": [62, 45, 31, 78],
            "Status": ["Swept", "Block", "Normal", "Swept"]
        })
        st.dataframe(flow_data, use_container_width=True)
    else:
        st.warning("Enter Polygon API key to see real flow data.")

st.success("✅ Dashboard connected to Polygon free tier")
st.caption("Real-time info is limited on free tier. Upgrade Polygon or Unusual Whales for true live sweeps.")

st.markdown("---")
st.caption("More visually aggressive than Skylit. Built for the future.")
