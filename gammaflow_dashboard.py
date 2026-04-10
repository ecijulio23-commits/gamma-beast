import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="GammaFlow Beast", layout="wide", page_icon="⚫", initial_sidebar_state="expanded")

# ====================== SINGULARITY DARK THEME ======================
st.markdown("""
<style>
    .stApp {
        background: #0a0a0a;
        color: #e0e0e0;
    }
    .main-header {
        font-size: 3.9rem;
        font-weight: 900;
        background: linear-gradient(90deg, #ffffff, #a0f0ff, #ffffff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        text-shadow: 0 0 40px rgba(160, 240, 255, 0.6);
        letter-spacing: -3px;
    }
    .subtitle {
        text-align: center;
        font-size: 1.25rem;
        color: #888888;
        margin-top: -15px;
        margin-bottom: 25px;
    }
    .glass-card {
        background: rgba(20, 20, 25, 0.95);
        border: 1px solid #333333;
        border-radius: 18px;
        padding: 20px;
        box-shadow: 0 0 25px rgba(0, 0, 0, 0.6);
    }
    .metric-card {
        background: #111111;
        border: 1px solid #222222;
        border-radius: 14px;
        padding: 16px;
        text-align: center;
    }
    .heatmap-title {
        color: #ffffff;
        text-align: center;
        font-size: 1.6rem;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ====================== HEADER ======================
st.markdown('<h1 class="main-header">GAMMAFLOW BEAST</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">SINGULARITY TERMINAL • GAMMA DETECTION SYSTEM</p>', unsafe_allow_html=True)

# Sidebar (minimal & dark)
st.sidebar.title("CONTROL")
polygon_key = st.sidebar.text_input("Polygon API Key", type="password", help="Free tier supported for basic features")

st.sidebar.subheader("Watchlist")
watchlist = st.sidebar.multiselect("", 
                                   ["META", "NVDA", "TSLA", "AAPL", "AMD", "GOOGL", "AMZN"],
                                   default=["GOOGL", "META", "NVDA"])

view_mode = st.sidebar.radio("Heatmap Mode", ["Single Ticker", "All Tickers"], horizontal=True)

if st.sidebar.button("REFRESH TERMINAL", type="primary", use_container_width=True):
    st.rerun()

# ====================== QUICK STATUS ======================
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown('<div class="metric-card"><strong>BEAST ALERTS</strong><br><span style="font-size:2rem;color:#ffffff">17</span></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="metric-card"><strong>AVG UOA</strong><br><span style="font-size:2rem;color:#ffffff">84.2x</span></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="metric-card"><strong>NET GEX</strong><br><span style="font-size:2rem;color:#ffffff">+$1.94B</span></div>', unsafe_allow_html=True)
with col4:
    st.markdown('<div class="metric-card"><strong>LIVE FLOW</strong><br><span style="font-size:2rem;color:#ffffff">3.8K</span></div>', unsafe_allow_html=True)

st.markdown("---")

# ====================== TABS ======================
tab1, tab2, tab3 = st.tabs(["BEAST ALERTS", "GAMMA HEATMAP", "LIVE FLOW"])

# ====================== BEAST ALERTS ======================
with tab1:
    st.subheader("BEAST ALERT FEED")
    if "alerts" not in st.session_state:
        st.session_state.alerts = []

    if st.button("SIMULATE NUCLEAR BEAST", type="primary"):
        new_alert = {
            "time": datetime.now().strftime("%H:%M:%S"),
            "ticker": "GOOGL 250418C00160000",
            "volume": 15600,
            "price": 13.40,
            "uoa": 91.5,
            "conviction": 97
        }
        st.session_state.alerts.insert(0, new_alert)
        st.rerun()

    for alert in st.session_state.alerts[:8]:
        st.markdown(f"""
        <div class="glass-card">
            <strong style="font-size:1.35rem">⚫ {alert['ticker']}</strong> 
            <span style="float:right;color:#666666">{alert['time']}</span><br><br>
            Volume: <strong>{alert['volume']:,}</strong> | Price: <strong>${alert['price']}</strong><br>
            UOA: <strong>{alert['uoa']:.1f}x</strong> | Conviction: <strong>{alert['conviction']}/100</strong>
        </div>
        """, unsafe_allow_html=True)

# ====================== GAMMA HEATMAP (ONLY COLOR HERE) ======================
with tab2:
    st.markdown('<div class="heatmap-title">GAMMA EXPOSURE HEATMAP</div>', unsafe_allow_html=True)
    
    if view_mode == "Single Ticker":
        selected = st.selectbox("Select Ticker", watchlist)
        display_tickers = [selected]
    else:
        display_tickers = watchlist

    # Realistic simulated GEX data
    np.random.seed(42)
    expirations = ["2026-04-03", "2026-04-10", "2026-04-17", "2026-04-24", "2026-05-01", "2026-05-15"]
    strikes = list(range(420, 521, 10))

    data = []
    for exp in expirations:
        row = [exp]
        for s in strikes:
            dist = abs(s - 465)
            base = np.random.randint(90, 920) * max(0.25, 1 - dist/115)
            gex = int(base * np.random.choice([-1.5, -1.0, 0.8, 1.4, 1.9]))
            row.append(gex)
        data.append(row)

    df = pd.DataFrame(data, columns=["Expiration"] + [f"${s}" for s in strikes])

    # Pure Singularity-style heatmap (color ONLY here)
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=df.columns,
            fill_color="#1a1a1a",
            font=dict(color="#cccccc", size=14),
            align="center"
        ),
        cells=dict(
            values=[df[col] for col in df.columns],
            fill_color=[
                ["#1a1a1a"] * len(df)
            ] + [[
                "#00cc66" if v > 450 else
                "#00ff88" if v > 80 else
                "#ffffff" if abs(v) < 50 else
                "#ff6666" if v > -180 else
                "#cc0000"
                for v in df[col]
            ] for col in df.columns[1:]],
            font=dict(color="#eeeeee", size=13),
            align="center",
            height=40
        )
    )])

    fig.update_layout(
        height=680,
        margin=dict(l=20, r=20, t=40, b=20),
        template="plotly_dark"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.caption("🟢 Positive GEX (stabilizing)  🔴 Negative GEX (amplifying)  White = Neutral")

# ====================== LIVE FLOW ======================
with tab3:
    st.subheader("LIVE OPTIONS FLOW")
    n = min(len(display_tickers), 6)
    flow_df = pd.DataFrame({
        "Ticker": display_tickers[:n],
        "Contract": ["250418C460","250418C470","250418C480","250418C490","250418C500","250418C510"][:n],
        "Volume": [15600,11200,8400,6100,3900,2700][:n],
        "OI": [380,590,270,440,160,80][:n],
        "Aggression": [91.5,78.3,64.1,89.7,52.4,61.8][:n],
        "Swept": ["YES","YES","NO","YES","NO","YES"][:n]
    })
    st.dataframe(flow_df.style.set_properties(**{'color': '#eeeeee', 'background-color': '#111111'}), 
                 use_container_width=True, hide_index=True)

st.caption("SINGULARITY MODE • GammaFlow Beast • Simulated GEX (Polygon free tier)")
