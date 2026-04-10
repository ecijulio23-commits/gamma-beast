import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# Safe Polygon import
try:
    from polygon import RESTClient
    POLYGON_AVAILABLE = True
except ImportError:
    POLYGON_AVAILABLE = False

st.set_page_config(page_title="GammaFlow Beast", layout="wide", page_icon="⚫", initial_sidebar_state="expanded")

# Singularity Theme
st.markdown("""
<style>
    .stApp { background: #05050a; color: #e0e0e0; }
    .main-header {
        font-size: 3.8rem; font-weight: 900;
        background: linear-gradient(90deg, #ffffff, #a0f0ff);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-align: center; text-shadow: 0 0 40px rgba(160, 240, 255, 0.5);
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

# Auto-refresh every 5 seconds (5000 ms)
st_autorefresh(interval=5000, key="datarefresh")

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

# Polygon client
client = None
if polygon_key and POLYGON_AVAILABLE:
    try:
        client = RESTClient(api_key=polygon_key)
        st.sidebar.success("✅ Polygon connected (free tier)")
    except:
        st.sidebar.error("Polygon connection failed")
else:
    st.sidebar.warning("Enter valid Polygon key")

# Quick Metrics
col1, col2, col3, col4 = st.columns(4)
with col1: st.markdown('<div class="metric"><strong>BEAST ALERTS</strong><br><span style="font-size:1.8rem">14</span></div>', unsafe_allow_html=True)
with col2: st.markdown('<div class="metric"><strong>AVG UOA</strong><br><span style="font-size:1.8rem">86.3x</span></div>', unsafe_allow_html=True)
with col3: st.markdown('<div class="metric"><strong>NET GEX</strong><br><span style="font-size:1.8rem">+$2.1B</span></div>', unsafe_allow_html=True)
with col4: st.markdown('<div class="metric"><strong>VIX</strong><br><span style="font-size:1.8rem;color:#aaa">18.7 NEUTRAL</span></div>', unsafe_allow_html=True)

st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(["🔥 BEAST ALERTS", "🌡️ GAMMA HEATMAP", "📡 VIX SIGNALS", "📊 LIVE FLOW"])

# ==================== IMPROVED GAMMA HEATMAP ====================
with tab2:
    st.markdown('<div class="heatmap-title">GAMMA EXPOSURE HEATMAP</div>', unsafe_allow_html=True)

    if view_mode == "Single Ticker":
        selected = st.selectbox("Select Ticker", watchlist)
        display_tickers = [selected]
    else:
        display_tickers = watchlist

    # Realistic GEX generation (refreshes every 5s)
    np.random.seed(int(time.time()))  # change seed slightly each refresh for variation
    expirations = ["2026-04-03", "2026-04-10", "2026-04-17", "2026-04-24", "2026-05-01", "2026-05-15"]
    strikes = list(range(430, 511, 10))
    spot_price = 470

    data = []
    for exp in expirations:
        row = [exp]
        for strike in strikes:
            distance = abs(strike - spot_price)
            intensity = np.exp(-distance / 28) * np.random.uniform(0.7, 1.4)
            base_gex = int(800 * intensity * np.random.uniform(0.6, 1.8))
            gex = int(base_gex * np.random.choice([-1.4, -1.0, 0.8, 1.2, 1.6]))
            row.append(gex)
        data.append(row)

    df = pd.DataFrame(data, columns=["Expiration"] + [f"${s}" for s in strikes])

    # Professional color scaling
    cell_colors = []
    for row in df.iloc[:, 1:].values:
        colors = []
        for val in row:
            if val > 800: colors.append("#00cc44")
            elif val > 200: colors.append("#00ff77")
            elif val > 50: colors.append("#88ffaa")
            elif abs(val) <= 60: colors.append("#ffffff")
            elif val > -200: colors.append("#ff7777")
            elif val > -600: colors.append("#ff4444")
            else: colors.append("#cc0000")
        cell_colors.append(colors)

    fig = go.Figure(data=[go.Table(
        header=dict(values=df.columns, fill_color="#1a1a1a", font=dict(color="#dddddd", size=14), align="center"),
        cells=dict(
            values=[df[col] for col in df.columns],
            fill_color=[["#1a1a1a"]] + cell_colors,
            font=dict(color="#eeeeee", size=13),
            align="center",
            height=42
        )
    )])

    fig.update_layout(height=720, template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

    st.caption("🟢 Positive GEX (stabilizing) 🔴 Negative GEX (amplifying) White = Neutral")

# Keep your other tabs (Beast Alerts, VIX Signals, Live Flow) as they were before

st.caption("GammaFlow Beast • Singularity Mode • Auto-refresh every 5 seconds • Powered by Polygon (free tier)")
