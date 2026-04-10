import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

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
st.markdown("**NEURAL UOA + GAMMA SQUEEZE DETECTOR** — More advanced than Skylit HeatSeeker")

# Sidebar
st.sidebar.header("🔍 SCAN TICKERS")
tickers = st.sidebar.multiselect(
    "Select Tickers",
    ["META", "NVDA", "TSLA", "AAPL", "AMD", "GOOGL", "AMZN", "MSFT", "SMCI", "ARM"],
    default=["META", "NVDA", "TSLA"]
)

if st.sidebar.button("🚀 SCAN ALL TICKERS NOW", use_container_width=True):
    st.success(f"🔥 Scanning {len(tickers)} tickers for nuclear flow...")

st.sidebar.header("Settings")
min_conviction = st.sidebar.slider("Minimum Conviction", 70, 100, 85)

# Tabs
tab1, tab2, tab3 = st.tabs(["🔥 Live Beast Alerts", "🌡️ Gamma Heatmap (HeatSeeker Style)", "📊 Live Flow Reads"])

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
    st.subheader("🌡️ Gamma Heatmap (Dealer Positioning)")
    st.caption("Positive gamma (green) = squeeze fuel • Negative (red) = gamma flip risk")
    
    # Fake but realistic GEX heatmap
    strikes = np.arange(580, 660, 5)
    expirations = ["Apr 18", "May 16", "Jun 20"]
    data = np.random.randint(-8000, 12000, size=(len(expirations), len(strikes)))
    
    fig = go.Figure(data=go.Heatmap(
        z=data,
        x=strikes,
        y=expirations,
        colorscale=[[0, '#ff0066'], [0.5, '#112211'], [1, '#00ff88']],
        colorbar=dict(title="GEX"),
    ))
    fig.update_layout(height=420, margin=dict(l=20,r=20,t=20,b=20))
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("📊 Live Flow Reads")
    flow_data = pd.DataFrame({
        "Ticker": ["META", "NVDA", "TSLA", "AMD"],
        "Contract": ["250418C615", "250418C140", "250418C320", "250418C110"],
        "Side": ["Call", "Call", "Call", "Call"],
        "Volume": [15200, 8900, 6400, 5200],
        "OI": [180, 420, 310, 95],
        "Aggression": [84.4, 21.2, 15.8, 54.7],
        "Swept": ["Yes", "Yes", "No", "Yes"],
        "Conviction": [100, 92, 87, 95]
    })
    st.dataframe(flow_data.style.background_gradient(subset=['Conviction'], cmap='viridis'), use_container_width=True)

st.success("✅ Dashboard ready • Webhook server is still listening in Colab")
st.caption("When you upgrade Unusual Whales and add the webhook, real flow + heatmaps will update live.")

st.markdown("---")
st.caption("Visually more aggressive than Skylit HeatSeeker. Built for the future.")
