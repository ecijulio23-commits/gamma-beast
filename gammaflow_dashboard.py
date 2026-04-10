import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="GammaFlow Beast", layout="wide", page_icon="🚀", initial_sidebar_state="collapsed")

# ====================== FUTURISTIC CSS ======================
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #0a0a0a, #12002b, #2a004d, #1a0033);
        background-size: 300% 300%;
        animation: cyberMorph 25s ease infinite;
        color: #00ffcc;
    }
    @keyframes cyberMorph {
        0%   { background-position: 0% 50%; }
        50%  { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .main-header {
        font-size: 3.8rem; font-weight: 900;
        background: linear-gradient(90deg, #00ffcc, #ff00ff, #00ffff);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-align: center; text-shadow: 0 0 60px #00ffcc, 0 0 100px #ff00ff;
        letter-spacing: -2px;
    }
    .subtitle { text-align: center; font-size: 1.3rem; color: #ff00ff;
                text-shadow: 0 0 20px #ff00ff; margin-top: -10px; margin-bottom: 20px; }
    .glass-card {
        background: rgba(15, 15, 40, 0.75); border: 1px solid rgba(0, 255, 204, 0.4);
        border-radius: 20px; padding: 20px; box-shadow: 0 0 35px rgba(0, 255, 204, 0.25);
        backdrop-filter: blur(12px);
    }
    .metric-card {
        background: rgba(20, 20, 50, 0.7); border: 1px solid #00ffcc;
        border-radius: 16px; padding: 15px; text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ====================== HEADER ======================
st.markdown('<h1 class="main-header">GAMMAFLOW BEAST</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">NEURAL UOA + REAL-TIME GAMMA DETECTOR • CYBER TERMINAL v2</p>', unsafe_allow_html=True)

# Top status bar
col_status, col_watch, col_refresh = st.columns([1, 3, 1])
with col_status:
    st.success("● POLYGON FREE TIER CONNECTED (GEX Simulated)")

with col_watch:
    st.caption("WATCHLIST")
    watchlist = st.multiselect("", 
                               ["META", "NVDA", "TSLA", "AAPL", "AMD", "GOOGL", "AMZN"],
                               default=["GOOGL", "META", "NVDA", "TSLA"],
                               label_visibility="collapsed")

with col_refresh:
    if st.button("🔄 REFRESH TERMINAL", type="primary", use_container_width=True):
        st.rerun()

st.markdown("---")

# ====================== QUICK METRICS ======================
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown('<div class="metric-card"><h3>🧬 14 BEAST ALERTS</h3><p style="color:#ff00ff">+7 since last scan</p></div>', unsafe_allow_html=True)
with m2:
    st.markdown('<div class="metric-card"><h3>🔥 AVG UOA</h3><h2 style="color:#00ffcc">87.4x</h2></div>', unsafe_allow_html=True)
with m3:
    st.markdown('<div class="metric-card"><h3>🌡️ NET GEX</h3><h2 style="color:#00ff99">+$2.84B</h2><p style="color:#00cc66">BULLISH</p></div>', unsafe_allow_html=True)
with m4:
    st.markdown('<div class="metric-card"><h3>📡 LIVE FLOW</h3><h2 style="color:#ffff00">4.2K contracts</h2></div>', unsafe_allow_html=True)

st.markdown("---")

# ====================== TABS ======================
tab1, tab2, tab3 = st.tabs(["🔥 BEAST ALERTS", "🌡️ GAMMA HEATMAP", "📊 LIVE FLOW READS"])

# ====================== TAB 1: BEAST ALERTS ======================
with tab1:
    st.subheader("LIVE BEAST ALERTS FEED")
    if "alerts" not in st.session_state:
        st.session_state.alerts = []

    if st.button("🚨 SIMULATE NUCLEAR BEAST", type="primary"):
        new_alert = {
            "time": datetime.now().strftime("%H:%M:%S"),
            "ticker": "GOOGL 250418C00160000",
            "volume": 18700,
            "price": 14.80,
            "uoa": 96.7,
            "conviction": 98
        }
        st.session_state.alerts.insert(0, new_alert)
        st.rerun()

    for alert in st.session_state.alerts[:10]:
        st.markdown(f"""
        <div class="glass-card">
            <strong style="font-size:1.3rem">🚨 {alert['ticker']}</strong> 
            <span style="float:right; color:#ffff00">{alert['time']}</span><br>
            Volume: <strong>{alert['volume']:,}</strong> • Price: <strong>${alert['price']}</strong><br>
            UOA Aggression: <strong style="color:#ff00ff">{alert['uoa']:.1f}x</strong> • 
            Conviction: <span style="background:#00ffcc;color:#000;padding:2px 8px;border-radius:9999px">{alert['conviction']}/100</span>
        </div>
        """, unsafe_allow_html=True)

# ====================== TAB 2: GAMMA HEATMAP ======================
with tab2:
    st.subheader("GAMMA EXPOSURE HEATMAP")
    
    view = st.radio("View Mode", ["Single Ticker", "All Watchlist Combined"], horizontal=True, label_visibility="collapsed")
    
    if view == "Single Ticker":
        ticker = st.selectbox("Ticker", watchlist, index=0)
        display_tickers = [ticker]
    else:
        display_tickers = watchlist

    st.caption(f"Showing realistic simulated GEX for: **{', '.join(display_tickers)}**")

    # Realistic simulated GEX (Skylit-style)
    np.random.seed(42)
    expirations = ["2026-04-03", "2026-04-10", "2026-04-17", "2026-04-24", "2026-05-01", "2026-05-15"]
    strikes = list(range(420, 521, 10))

    data = []
    for exp in expirations:
        row = [exp]
        for s in strikes:
            dist = abs(s - 465)
            base = np.random.randint(80, 950) * max(0.2, 1 - dist/110)
            gex = int(base * np.random.choice([-1.4, -0.9, 0.7, 1.3, 1.8]))
            row.append(gex)
        data.append(row)

    df = pd.DataFrame(data, columns=["Expiration"] + [f"${s}" for s in strikes])

    # Skylit-style table
    fig = go.Figure(data=[go.Table(
        header=dict(values=df.columns, fill_color="#1a0033",
                    font=dict(color="#00ffcc", size=15), align="center"),
        cells=dict(
            values=[df[col] for col in df.columns],
            fill_color=[["#1a0033"]] + [[
                "#00cc66" if v > 500 else "#00ff99" if v > 100 else
                "#ffffff" if -50 < v < 50 else "#ff6666" if v > -200 else "#cc0000"
                for v in df[col]
            ] for col in df.columns[1:]],
            font=dict(color="#111111", size=14), align="center", height=42
        )
    )])

    fig.update_layout(title=f"Gamma Exposure — {', '.join(display_tickers)}", height=680, template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

    st.caption("🟢 Positive GEX = Dealers stabilize price 🔴 Negative GEX = Dealers amplify moves")

# ====================== TAB 3: LIVE FLOW READS ======================
with tab3:
    st.subheader("LIVE OPTIONS FLOW")
    n = min(len(display_tickers), 6)
    flow_df = pd.DataFrame({
        "Ticker": display_tickers[:n],
        "Contract": ["250418C460", "250418C470", "250418C480", "250418C490", "250418C500", "250418C510"][:n],
        "Volume": [18700, 12400, 9300, 6800, 4100, 2900][:n],
        "OI": [420, 680, 310, 520, 180, 95][:n],
        "Aggression": [96.7, 81.2, 67.4, 92.1, 44.8, 55.3][:n],
        "Swept": ["YES", "YES", "NO", "YES", "YES", "NO"][:n]
    })
    st.dataframe(flow_df, use_container_width=True, hide_index=True)

# ====================== FOOTER ======================
st.markdown("---")
st.caption("GAMMAFLOW BEAST v2 • More visually aggressive than Skylit • Simulated GEX (Polygon free tier limited)")
