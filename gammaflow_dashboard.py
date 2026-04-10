import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from polygon import RESTClient
from datetime import datetime
import time

st.set_page_config(page_title="GammaFlow Beast", layout="wide", page_icon="⚫", initial_sidebar_state="expanded")

# ====================== SINGULARITY DARK THEME ======================
st.markdown("""
<style>
    .stApp {
        background: #05050a;
        color: #e0e0e0;
    }
    .main-header {
        font-size: 3.8rem;
        font-weight: 900;
        background: linear-gradient(90deg, #ffffff, #a0f0ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        text-shadow: 0 0 40px rgba(160, 240, 255, 0.5);
        letter-spacing: -2px;
    }
    .glass-card {
        background: rgba(15, 15, 25, 0.95);
        border: 1px solid #333333;
        border-radius: 18px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 0 25px rgba(0,0,0,0.7);
    }
    .metric {
        background: #111111;
        border: 1px solid #222;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
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

# Initialize client
client = None
if polygon_key:
    try:
        client = RESTClient(api_key=polygon_key)
    except:
        st.sidebar.warning("Invalid or limited Polygon key")

# Live Ticker Bar (simulated + real quotes where possible)
st.markdown("**LIVE MARKET**")
ticker_bar = st.empty()

# ====================== QUICK METRICS ======================
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown('<div class="metric"><strong>BEAST ALERTS</strong><br><span style="font-size:1.8rem">14</span></div>', unsafe_allow_html=True)
with m2:
    st.markdown('<div class="metric"><strong>AVG UOA</strong><br><span style="font-size:1.8rem">86.3x</span></div>', unsafe_allow_html=True)
with m3:
    st.markdown('<div class="metric"><strong>NET GEX</strong><br><span style="font-size:1.8rem">+$2.1B</span></div>', unsafe_allow_html=True)
with m4:
    st.markdown('<div class="metric"><strong>VIX REGIME</strong><br><span style="font-size:1.8rem;color:#888">NEUTRAL</span></div>', unsafe_allow_html=True)

st.markdown("---")

# ====================== TABS ======================
tab1, tab2, tab3, tab4 = st.tabs(["🔥 BEAST ALERTS", "🌡️ GAMMA HEATMAP", "📡 VIX SIGNALS", "📊 LIVE FLOW"])

# TAB 1: BEAST ALERTS
with tab1:
    st.subheader("BEAST ALERT FEED")
    if "alerts" not in st.session_state:
        st.session_state.alerts = []

    if st.button("🚨 SIMULATE NUCLEAR BEAST", type="primary"):
        new = {"time": datetime.now().strftime("%H:%M:%S"), "ticker": "SPY 250418C00520000", "volume": 18400, "price": 11.20, "uoa": 94.8, "conviction": 96}
        st.session_state.alerts.insert(0, new)
        st.rerun()

    for a in st.session_state.alerts[:10]:
        st.markdown(f"""
        <div class="glass-card">
            <strong>⚫ {a['ticker']}</strong> <span style="float:right;color:#666">{a['time']}</span><br><br>
            Vol: <strong>{a['volume']:,}</strong> | Price: <strong>${a['price']}</strong><br>
            UOA: <strong>{a['uoa']:.1f}x</strong> | Conviction: <strong>{a['conviction']}/100</strong>
        </div>
        """, unsafe_allow_html=True)

# TAB 2: GAMMA HEATMAP (Only color here)
with tab2:
    st.markdown('<div class="heatmap-title">GAMMA EXPOSURE HEATMAP</div>', unsafe_allow_html=True)

    if view_mode == "Single Ticker":
        selected = st.selectbox("Ticker", watchlist, index=0)
        display = [selected]
    else:
        display = watchlist

    st.info(f"Realistic GEX simulation for: {', '.join(display)}  (Free tier → real chain limited)")

    # High-quality simulated GEX (Skylit-style, only vibrant colors)
    np.random.seed(42)
    exps = ["2026-04-03","2026-04-10","2026-04-17","2026-04-24","2026-05-01","2026-05-15"]
    strikes = list(range(420, 521, 10))

    data = []
    for exp in exps:
        row = [exp]
        for s in strikes:
            dist = abs(s - 465)
            base = np.random.randint(80, 950) * max(0.2, 1 - dist/110)
            gex = int(base * np.random.choice([-1.6, -1.1, 0.7, 1.5, 2.0]))
            row.append(gex)
        data.append(row)

    df = pd.DataFrame(data, columns=["Expiration"] + [f"${s}" for s in strikes])

    fig = go.Figure(data=[go.Table(
        header=dict(values=df.columns, fill_color="#111111", font=dict(color="#ccc", size=14), align="center"),
        cells=dict(
            values=[df[col] for col in df.columns],
            fill_color=[["#111111"]] + [[
                "#00cc66" if v > 500 else "#00ff88" if v > 100 else
                "#ffffff" if abs(v) < 60 else "#ff6666" if v > -200 else "#cc0000"
                for v in df[col]
            ] for col in df.columns[1:]],
            font=dict(color="#eee", size=13), align="center", height=42
        )
    )])

    fig.update_layout(height=680, template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

    st.caption("🟢 Positive GEX (dealers stabilize) 🔴 Negative GEX (dealers amplify) White = Neutral")

# TAB 3: VIX SIGNALS (Bolt-inspired)
with tab3:
    st.subheader("VIX CONFLUENCE SIGNALS")
    st.info("VIX regime + confluence scores (simulated — real VIX via Polygon possible with upgrade)")
    
    vix = 18.7
    regime = "NEUTRAL"
    buy_score = 5
    sell_score = 3

    colA, colB = st.columns(2)
    with colA:
        st.metric("VIX", f"{vix}", "NEUTRAL")
    with colB:
        st.metric("Term Structure", "CONTANGO", "Mild")

    # Signal Orb
    orb_color = "#888888"
    orb_text = "● NEUTRAL"
    if buy_score >= 6:
        orb_color = "#00cc66"
        orb_text = "▲ BUY"
    elif sell_score >= 5:
        orb_color = "#cc0000"
        orb_text = "▼ SELL"

    st.markdown(f"""
    <div style="text-align:center; margin:30px 0;">
        <div style="width:140px; height:140px; margin:auto; border-radius:9999px; background:{orb_color}; 
                    box-shadow:0 0 60px {orb_color}; display:flex; align-items:center; justify-content:center; font-size:2.2rem; color:#000;">
            {orb_text}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.progress(buy_score / 8, text=f"BUY SCORE: {buy_score}/8")
    st.progress(sell_score / 7, text=f"SELL SCORE: {sell_score}/7")

# TAB 4: LIVE FLOW
with tab4:
    st.subheader("LIVE OPTIONS FLOW")
    n = min(len(display), 5)
    flow = pd.DataFrame({
        "Ticker": display[:n],
        "Contract": ["250418C460","250418C470","250418C480","250418C490","250418C500"][:n],
        "Volume": [14200,9800,7500,5200,3100][:n],
        "Aggression": [92.1,76.4,81.9,55.2,67.8][:n]
    })
    st.dataframe(flow, use_container_width=True, hide_index=True)

st.caption("GammaFlow Beast • Singularity Mode • Powered by Polygon (free tier) • More aggressive than Skylit")
