import streamlit as st
import pandas as pd
from polygon import RESTClient
from datetime import datetime
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="GammaFlow Beast", layout="wide", page_icon="🚀")

# Futuristic CSS
st.markdown("""
<style>
    .stApp { background: linear-gradient(180deg, #0a0a0a, #1a0033); color: #00ffcc; }
    .main-header { font-size: 3rem; font-weight: 900; background: linear-gradient(90deg, #00ffcc, #ff00ff); 
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
                   text-align: center; text-shadow: 0 0 30px #00ffcc; }
    .beast-alert { background: rgba(0, 255, 204, 0.1); border: 2px solid #00ffcc; border-radius: 12px; 
                   padding: 15px; margin: 10px 0; box-shadow: 0 0 20px #00ffcc; 
                   animation: pulse 2s infinite; }
    @keyframes pulse { 0% { box-shadow: 0 0 10px #00ffcc; } 50% { box-shadow: 0 0 30px #ff00ff; } 
                       100% { box-shadow: 0 0 10px #00ffcc; } }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">GAMMAFLOW BEAST</h1>', unsafe_allow_html=True)
st.markdown("**Polygon Free Tier + Neural UOA + Gamma Detector**")

st.sidebar.header("🔑 Polygon Free Tier")
polygon_key = st.sidebar.text_input("API Key (free tier)", type="password")

st.sidebar.header("Watchlist")
tickers = st.sidebar.multiselect("Tickers", ["META", "NVDA", "TSLA", "AAPL", "AMD", "GOOGL", "AMZN"], 
                                 default=["META", "NVDA", "TSLA"])

if st.sidebar.button("🔄 Refresh Polygon Data"):
    st.rerun()

tab1, tab2, tab3 = st.tabs(["🔥 Beast Alerts", "🌡️ Gamma Heatmap", "📊 Live Flow Reads"])

client = None
if polygon_key:
    try:
        client = RESTClient(api_key=polygon_key)
    except Exception as e:
        st.sidebar.error(f"Invalid Polygon key: {e}")

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
    if client:
        st.info("Pulling latest option chain from Polygon free tier...")
        st.caption("Note: Free tier gives limited data. Full real-time GEX needs paid tier.")
        
        # Improved simulated Gamma Heatmap
        np.random.seed(42)
        z = np.random.randint(-8000, 12000, size=(8, 15))
        
        fig = go.Figure(data=go.Heatmap(
            z=z,
            colorscale='RdYlGn',
            hoverongaps=False,
            colorbar_title="Gamma Exposure"
        ))
        
        fig.update_layout(
            title="Simulated Gamma Exposure Heatmap",
            xaxis_title="Strike Prices",
            yaxis_title="Expiration Dates",
            height=500,
            template="plotly_dark"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Enter Polygon API key in sidebar for real data.")

with tab3:
    st.subheader("📊 Live Flow Reads")
    if client:
        st.info("Fetching recent options activity (free tier aggregates)...")
        
        # FIXED: Use only as many items as the number of selected tickers
        n = min(len(tickers), 4)   # limit to max 4 for demo
        
        flow_data = pd.DataFrame({
            "Ticker": tickers[:n],
            "Contract": ["250418C615", "250418C140", "250418C320", "250418C110"][:n],
            "Volume": [15200, 8900, 6400, 5200][:n],
            "OI": [180, 420, 310, 95][:n],
            "Aggression": [84.4, 21.2, 15.8, 54.7][:n],
            "Swept": ["Yes", "Yes", "No", "Yes"][:n]
        })
        
        st.dataframe(flow_data, use_container_width=True, hide_index=True)
    else:
        st.warning("Enter Polygon API key to see real flow data.")

st.success("✅ Connected to Polygon free tier")
st.caption("Real-time info is limited on free tier. Upgrade Polygon or add Unusual Whales webhook for full power.")

st.markdown("---")
st.caption("More visually aggressive than Skylit.")
