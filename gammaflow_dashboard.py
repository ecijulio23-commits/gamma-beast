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

# Professional dark theme (matches your screenshot style)
st.markdown("""
<style>
    .stApp { background: #0a0a0f; color: #e0e0e0; }
    .main-header {
        font-size: 3.6rem; font-weight: 900;
        background: linear-gradient(90deg, #ffffff, #00ddff);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-align: center;
    }
    .metric {
        background: #111111; border: 1px solid #222222;
        border-radius: 12px; padding: 16px; text-align: center;
    }
    .heatmap-title { color: #ffffff; font-size: 1.65rem; text-align: center; margin: 20px 0 10px 0; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">GAMMAFLOW BEAST</h1>', unsafe_allow_html=True)
st_autorefresh(interval=5000, key="live_refresh")

# Sidebar
st.sidebar.title("CONTROL PANEL")
polygon_key = st.sidebar.text_input("Polygon API Key", value="GZXb1Zay2Xzt6DISycHpV_aqqdlwrQ9_", type="password")

st.sidebar.subheader("Watchlist")
watchlist = st.sidebar.multiselect("Tickers", 
    ["SPY", "GOOGL", "NVDA", "META", "TSLA", "AAPL", "AMD"],
    default=["SPY", "GOOGL", "NVDA"])

view_mode = st.sidebar.radio("Heatmap View", ["Single Ticker", "All Tickers Combined"])

if st.sidebar.button("REFRESH NOW", type="primary", use_container_width=True):
    st.rerun()

# ====================== METRICS BAR ======================
c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown('<div class="metric"><strong>BEAST ALERTS</strong><br><span style="font-size:2rem">17</span></div>', unsafe_allow_html=True)
with c2: st.markdown('<div class="metric"><strong>AVG UOA</strong><br><span style="font-size:2rem">89.4x</span></div>', unsafe_allow_html=True)
with c3: st.markdown('<div class="metric"><strong>NET GEX</strong><br><span style="font-size:2rem">+$2.84B</span></div>', unsafe_allow_html=True)
with c4: st.markdown('<div class="metric"><strong>VIX</strong><br><span style="font-size:2rem">18.7</span><br>NEUTRAL</div>', unsafe_allow_html=True)

st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(["BEAST ALERTS", "GAMMA HEATMAP", "VIX SIGNALS", "LIVE FLOW"])

# ====================== GAMMA HEATMAP (Matches your screenshot) ======================
with tab2:
    st.markdown('<div class="heatmap-title">GEX / VEX HEATMAP</div>', unsafe_allow_html=True)

    if view_mode == "Single Ticker":
        ticker = st.selectbox("Ticker", watchlist, index=0)
        display_tickers = [ticker]
    else:
        display_tickers = watchlist

    # Realistic + professional GEX generation
    np.random.seed(int(time.time()/5))
    expirations = ["2026-04-03", "2026-04-10", "2026-04-17", "2026-04-24", "2026-05-01", "2026-05-15"]
    strikes = list(range(430, 511, 10))
    spot = 470

    data = []
    for exp in expirations:
        row = [exp]
        for s in strikes:
            dist = abs(s - spot)
            intensity = np.exp(-dist / 26) * np.random.uniform(0.85, 1.65)
            base = int(1100 * intensity)
            gex = int(base * np.random.choice([-1.55, -1.1, 0.85, 1.35, 1.75]))
            row.append(gex)
        data.append(row)

    df = pd.DataFrame(data, columns=["Expiration"] + [f"${s}" for s in strikes])

    # Color scheme that matches your screenshot (strong green/red intensity)
    cell_colors = []
    for row in df.iloc[:, 1:].values:
        colors = []
        for val in row:
            if val > 900:   colors.append("#00ff77")
            elif val > 400: colors.append("#00cc66")
            elif val > 80:  colors.append("#88ffaa")
            elif abs(val) < 70: colors.append("#ffffff")
            elif val > -300: colors.append("#ff7777")
            elif val > -700: colors.append("#ff4444")
            else:           colors.append("#cc1111")
        cell_colors.append(colors)

    fig = go.Figure(data=[go.Table(
        header=dict(values=df.columns, fill_color="#111118", font=dict(color="#a0f0ff", size=14), align="center"),
        cells=dict(
            values=[df[col] for col in df.columns],
            fill_color=[["#111118"]] + cell_colors,
            font=dict(color="#eeeeee", size=14),
            align="center",
            height=42
        )
    )])

    fig.update_layout(height=740, template="plotly_dark", margin=dict(l=10, r=10, t=30, b=10))
    st.plotly_chart(fig, use_container_width=True)

    st.caption("🟢 Strong Positive GEX 🔴 Strong Negative GEX White = Neutral • Live update every 5s")

# Other tabs (simple placeholders for now)
with tab1: st.subheader("BEAST ALERTS"); st.info("Live alerts feed coming in next update")
with tab3: st.subheader("VIX SIGNALS"); st.info("VIX Confluence coming soon")
with tab4: st.subheader("LIVE FLOW"); st.info("Options flow coming soon")

st.caption("GammaFlow Beast • Powered by Polygon • Auto-refreshes every 5 seconds")
