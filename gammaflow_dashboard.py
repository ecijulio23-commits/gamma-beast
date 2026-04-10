import streamlit as st
from datetime import datetime
import time

# Futuristic custom CSS (neon cyberpunk style)
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #0a0a0a, #1a0033);
        color: #00ffcc;
    }
    .main-header {
        font-size: 2.8rem;
        font-weight: 900;
        background: linear-gradient(90deg, #00ffcc, #ff00ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 10px;
        text-shadow: 0 0 20px #00ffcc;
    }
    .beast-alert {
        background: rgba(0, 255, 204, 0.1);
        border: 2px solid #00ffcc;
        border-radius: 12px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 0 15px #00ffcc;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 10px #00ffcc; }
        50% { box-shadow: 0 0 25px #ff00ff; }
        100% { box-shadow: 0 0 10px #00ffcc; }
    }
    .conviction-bar {
        height: 12px;
        background: #112211;
        border-radius: 9999px;
        overflow: hidden;
    }
    .conviction-fill {
        height: 100%;
        background: linear-gradient(90deg, #00ffcc, #ff00ff);
        border-radius: 9999px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">GAMMAFLOW BEAST</h1>', unsafe_allow_html=True)
st.markdown("**NEURAL UOA + GAMMA SQUEEZE DETECTOR** — *2026 Edition*")

col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("LIVE BEAST ALERTS")

    if "alerts" not in st.session_state:
        st.session_state.alerts = []

    if st.button("🔥 SIMULATE NUCLEAR BEAST", use_container_width=True):
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
            <br><span style="color:#ff00ff">Volume:</span> {alert['volume']:,} contracts 
            <span style="color:#ff00ff">• Price:</span> ${alert['price']}
            <br><span style="color:#00ffcc">UOA Aggression:</span> {alert['uoa']:.1f}x
            <div class="conviction-bar"><div class="conviction-fill" style="width: {alert['conviction']}%;"></div></div>
            <strong>Conviction: {alert['conviction']}/100</strong> 🔥
            <br><span style="color:#ffff00">Suggested size: {alert['size_mult']:.1f}x your base</span>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.subheader("SYSTEM STATUS")
    st.success("🟢 WEBHOOK SERVER LIVE")
    st.info(f"**Watchlist:** META, NVDA, TSLA, AAPL, AMD...")
    st.metric("Active Beasts Today", "3", "↑2")
    st.caption("Powered by RohOnChain 11-step AlphaCombiner")

st.divider()
st.caption("When you upgrade Unusual Whales and add the webhook, real nuclear moves will appear here instantly.")

st.markdown("---")
st.caption("Built to be more visually aggressive than Skylit. Future is now.")
