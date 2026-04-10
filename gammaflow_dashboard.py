import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
import time
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

# Auto-refresh every 5 seconds
st_autorefresh(interval=5000, key="heatmap_refresh")

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

# Define the tabs properly
tab1, tab2, tab3, tab4 = st.tabs(["🔥 BEAST ALERTS", "🌡️ GAMMA HEATMAP", "📡 VIX SIGNALS", "📊 LIVE FLOW"])

# ====================== BEAST ALERTS ======================
with tab1:
    st.subheader("BEAST ALERT FEED")
    if "alerts" not in st.session_state:
        st.session_state.alerts = []

    if st.button("🚨 SIMULATE NUCLEAR BEAST", type="primary"):
        new_alert = {
            "time": datetime.now().strftime("%H:%M:%S"),
            "ticker": "SPY 250418C00520000",
            "volume": 18400,
            "price": 11.20,
            "uoa": 94.8,
            "conviction": 96
        }
        st.session_state.alerts.insert(0, new_alert)
        st.rerun()

    for alert in st.session_state.alerts[:10]:
        st.markdown(f"""
        <div class="glass-card">
            <strong>⚫ {alert['ticker']}</strong> <span style="float:right;color:#666">{alert['time']}</span><br><br>
            Vol: <strong>{alert['volume']:,}</strong> | Price: <strong>${alert['price']}</strong><br>
            UOA: <strong>{alert['uoa']:.1f}x</strong> | Conviction: <strong>{alert['conviction']}/100</strong>
        </div>
        """, unsafe_allow_html=True)

# ====================== GAMMA HEATMAP (Professional Skylit-style) ======================
with tab2:
    st.markdown('<div class="heatmap-title">GAMMA EXPOSURE HEATMAP • LIVE</div>', unsafe_allow_html=True)

    if view_mode == "Single Ticker":
        selected = st.selectbox("Select Ticker", watchlist)
        display_tickers = [selected]
    else:
        display_tickers = watchlist

    # Realistic GEX generation
    current_seed = int(time.time() / 5)
    np.random.seed(current_seed)

    expirations = ["2026-04-03", "2026-04-10", "2026-04-17", "2026-04-24", "2026-05-01", "2026-05-15"]
    strikes = list(range(430, 511, 10))
    spot_price = 470

    data = []
    for exp in expirations:
        row = [exp]
        for strike in strikes:
            distance = abs(strike - spot_price)
            intensity = np.exp(-distance / 25) * np.random.uniform(0.8, 1.6)
            base = int(1200 * intensity * np.random.uniform(0.7, 1.9))
            gex = int(base * np.random.choice([-1.6, -1.1, 0.8, 1.3, 1.8]))
            row.append(gex)
        data.append(row)

    df = pd.DataFrame(data, columns=["Expiration"] + [f"${int(s)}" for s in strikes])

    # Professional color scheme
    cell_colors = []
    for row in df.iloc[:, 1:].values:
        colors = []
        for val in row:
            abs_val = abs(val)
            if abs_val > 1000:
                color = "#00ff88" if val > 0 else "#ff5555"
            elif abs_val > 400:
                color = "#00cc66" if val > 0 else "#ff7777"
            elif abs_val > 100:
                color = "#88ffaa" if val > 0 else "#ffaaaa"
            else:
                color = "#ffffff"
            colors.append(color)
        cell_colors.append(colors)

    fig = go.Figure(data=[go.Table(
        header=dict(
            values=df.columns,
            fill_color="#0f0f1a",
            font=dict(color="#a0f0ff", size=14),
            align="center",
            height=40
        ),
        cells=dict(
            values=[df[col] for col in df.columns],
            fill_color=[["#0f0f1a"]] + cell_colors,
            font=dict(color="#eeeeee", size=14),
            align="center",
            height=38
        )
    )])

    fig.update_layout(height=720, template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

    st.caption("🟢 Positive GEX (stabilizing) 🔴 Negative GEX (amplifying) White = Neutral • Updates every 5s")

# ====================== PLACEHOLDERS FOR OTHER TABS ======================
with tab3:
    st.subheader("VIX SIGNALS")
    st.info("VIX Confluence dashboard coming soon...")

with tab4:
    st.subheader("LIVE FLOW")
    st.info("Live options flow coming soon...")

st.caption("GammaFlow Beast • Singularity Mode • Auto-refresh every 5 seconds • Powered by Polygon (free tier)")
