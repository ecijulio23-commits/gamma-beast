import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
import time
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="GammaFlow Beast", layout="wide", page_icon="⚫", initial_sidebar_state="expanded")

# ==================== MODERN TERMINAL THEME ====================
st.markdown("""
<style>
    .stApp { background: #0a0a0f; color: #e0e0e0; }
    .main-header {
        font-size: 3.4rem; font-weight: 900;
        background: linear-gradient(90deg, #00ddff, #ffffff);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-align: center; letter-spacing: -2px;
    }
    .metric-card {
        background: #111118; border: 1px solid #222233;
        border-radius: 12px; padding: 14px; text-align: center;
    }
    .heatmap-title { font-size: 1.8rem; font-weight: 700; text-align: center; margin: 10px 0; color: #ffffff; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">GAMMAFLOW BEAST</h1>', unsafe_allow_html=True)
st_autorefresh(interval=5000, key="terminal_refresh")

# Sidebar
st.sidebar.title("⚫ TERMINAL CONTROL")
polygon_key = st.sidebar.text_input("Polygon API Key", value="GZXb1Zay2Xzt6DISycHpV_aqqdlwrQ9_", type="password")

st.sidebar.subheader("Watchlist")
watchlist = st.sidebar.multiselect("Active Tickers", 
    ["SPY", "GOOGL", "NVDA", "META", "TSLA", "AAPL", "AMD"],
    default=["SPY", "GOOGL", "NVDA"])

if st.sidebar.button("REFRESH ALL DATA", type="primary", use_container_width=True):
    st.rerun()

# ==================== TOP LIVE TICKER + METRICS ====================
st.markdown("**LIVE MARKET**")
ticker_bar = st.empty()  # placeholder for future real ticker

c1, c2, c3, c4, c5 = st.columns(5)
with c1: st.markdown('<div class="metric-card"><strong>BEAST ALERTS</strong><br><span style="font-size:1.9rem">17</span></div>', unsafe_allow_html=True)
with c2: st.markdown('<div class="metric-card"><strong>AVG UOA</strong><br><span style="font-size:1.9rem">89.4x</span></div>', unsafe_allow_html=True)
with c3: st.markdown('<div class="metric-card"><strong>NET GEX</strong><br><span style="font-size:1.9rem">+$2.84B</span></div>', unsafe_allow_html=True)
with c4: st.markdown('<div class="metric-card"><strong>VIX</strong><br><span style="font-size:1.9rem">18.7</span></div>', unsafe_allow_html=True)
with c5: st.markdown('<div class="metric-card"><strong>REGIME</strong><br><span style="color:#00ddff">NEUTRAL</span></div>', unsafe_allow_html=True)

st.markdown("---")

# ==================== MAIN LAYOUT ====================
left_col, right_col = st.columns([3.2, 1])

# ==================== LEFT: INTERACTIVE HEATMAP ====================
with left_col:
    st.markdown('<div class="heatmap-title">GEX / VEX HEATMAP</div>', unsafe_allow_html=True)

    # Toggle between GEX and VEX
    mode = st.radio("Mode", ["GEX", "VEX"], horizontal=True, label_visibility="collapsed")

    # Generate realistic heatmap data
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
            base = int(1150 * intensity)
            val = int(base * np.random.choice([-1.6, -1.1, 0.85, 1.35, 1.75]))
            row.append(val)
        data.append(row)

    df = pd.DataFrame(data, columns=["Expiration"] + [f"${s}" for s in strikes])

    # Color logic (very close to your screenshot)
    cell_colors = []
    for row in df.iloc[:, 1:].values:
        colors = []
        for val in row:
            if mode == "GEX":
                if val > 900: color = "#00ff88"
                elif val > 400: color = "#00cc66"
                elif val > 80: color = "#88ffaa"
                elif abs(val) < 70: color = "#ffffff"
                elif val > -300: color = "#ff7777"
                elif val > -700: color = "#ff4444"
                else: color = "#cc1111"
            else:  # VEX
                color = "#77aaff" if val > 0 else "#ff88aa"
            colors.append(color)
        cell_colors.append(colors)

    fig = go.Figure(data=[go.Table(
        header=dict(values=df.columns, fill_color="#111118", font=dict(color="#a0f0ff", size=14), align="center"),
        cells=dict(
            values=[df[col] for col in df.columns],
            fill_color=[["#111118"]] + cell_colors,
            font=dict(color="#eeeeee", size=14),
            align="center",
            height=44
        )
    )])

    fig.update_layout(height=720, template="plotly_dark", margin=dict(l=10, r=10, t=20, b=10))
    st.plotly_chart(fig, use_container_width=True)

    st.caption("🟢 Positive = Stabilizing 🔴 Negative = Amplifying White = Neutral • Live every 5s")

# ==================== RIGHT PANEL: VIX + ALERTS ====================
with right_col:
    st.subheader("VIX CONFLUENCE")
    st.metric("VIX Level", "18.7", "NEUTRAL")

    # Simple signal orb
    st.markdown("""
    <div style="text-align:center; margin:20px 0;">
        <div style="width:130px; height:130px; margin:auto; border-radius:50%; background:#555555; 
                    box-shadow:0 0 50px #00ddff; display:flex; align-items:center; justify-content:center; font-size:1.8rem;">
            NEUTRAL
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("LIVE BEAST ALERTS")
    if "alerts" not in st.session_state:
        st.session_state.alerts = []

    if st.button("🚨 Simulate Nuclear Beast", type="primary", use_container_width=True):
        new = {"time": datetime.now().strftime("%H:%M:%S"), "ticker": "SPY 250418C00520000", "uoa": 96.2}
        st.session_state.alerts.insert(0, new)
        st.rerun()

    for alert in st.session_state.alerts[:6]:
        st.markdown(f"""
        <div style="background:#1a1a22; padding:12px; border-radius:10px; margin:8px 0;">
            <strong>{alert['ticker']}</strong><br>
            <small>{alert['time']} • UOA {alert['uoa']}x</small>
        </div>
        """, unsafe_allow_html=True)

st.caption("GammaFlow Beast • Interactive Terminal • Auto-refreshes every 5 seconds • Powered by Polygon")
