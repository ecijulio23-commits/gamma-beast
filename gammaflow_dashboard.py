import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from polygon import RESTClient
from datetime import datetime

st.set_page_config(page_title="GammaFlow Beast", layout="wide", page_icon="🚀", initial_sidebar_state="expanded")

# === FUTURISTIC MORPHING BACKGROUND + CSS ===
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #0a0a0a, #1a0033, #2a004d);
        background-size: 400% 400%;
        animation: morph 15s ease infinite;
        color: #00ffcc;
    }
    @keyframes morph {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .main-header {
        font-size: 3.2rem; font-weight: 900; 
        background: linear-gradient(90deg, #00ffcc, #ff00ff, #00ffcc);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-align: center; text-shadow: 0 0 40px #00ffcc;
        margin-bottom: 10px;
    }
    .card {
        background: rgba(20, 20, 40, 0.85); 
        border: 1px solid #00ffcc; 
        border-radius: 16px; 
        padding: 20px; 
        box-shadow: 0 0 25px rgba(0, 255, 204, 0.3);
    }
    .neon-text { text-shadow: 0 0 15px #00ffcc; }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">GAMMAFLOW BEAST</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; font-size:1.1rem; color:#ff00ff;">Polygon Free Tier • Real Options Chain • Approximated GEX</p>', unsafe_allow_html=True)

# Sidebar
st.sidebar.header("🔑 Polygon Free Tier")
polygon_key = st.sidebar.text_input("API Key", type="password", help="Enter your Polygon free tier key")

st.sidebar.header("Watchlist")
tickers = st.sidebar.multiselect("Select Tickers", 
                                 ["META", "NVDA", "TSLA", "AAPL", "AMD", "GOOGL", "AMZN"], 
                                 default=["GOOGL"])

view_mode = st.sidebar.radio("Heatmap View", ["Single Ticker", "All Tickers (Combined)"], horizontal=True)

if st.sidebar.button("🔄 Refresh All Data", type="primary"):
    st.rerun()

# Initialize client
client = None
if polygon_key:
    try:
        client = RESTClient(api_key=polygon_key)
    except Exception as e:
        st.sidebar.error(f"Key error: {e}")

# Tabs
tab1, tab2, tab3 = st.tabs(["🔥 Beast Alerts", "🌡️ Gamma Heatmap", "📊 Live Flow Reads"])

# ===================== BEAST ALERTS =====================
with tab1:
    st.subheader("Recent Beast Alerts")
    if "alerts" not in st.session_state:
        st.session_state.alerts = []

    if st.button("🔥 Simulate Nuclear Beast", type="primary"):
        new_alert = {
            "time": datetime.now().strftime("%H:%M:%S"),
            "ticker": "GOOGL 250418C00160000",
            "volume": 12400,
            "price": 12.50,
            "uoa": 92.3,
            "conviction": 95,
            "size_mult": 2.5
        }
        st.session_state.alerts.insert(0, new_alert)
        st.rerun()

    for alert in st.session_state.alerts[:6]:
        st.markdown(f"""
        <div class="card">
            <strong>🚨 {alert['ticker']}</strong> • {alert['time']}
            <br>Volume: {alert['volume']:,} • Price: ${alert['price']}
            <br>UOA: {alert['uoa']:.1f}x • Conviction: {alert['conviction']}/100
        </div>
        """, unsafe_allow_html=True)

# ===================== GAMMA HEATMAP (Real Polygon Data) =====================
with tab2:
    st.subheader("🌡️ Gamma Heatmap")
    
    if not client:
        st.warning("Enter your Polygon API key in the sidebar to pull real options data.")
        st.stop()

    if view_mode == "Single Ticker":
        selected_ticker = st.selectbox("Select Ticker", tickers, index=0)
        tickers_to_show = [selected_ticker]
    else:
        tickers_to_show = tickers

    st.info(f"Fetching real options chain for: **{', '.join(tickers_to_show)}** (Free tier — limited depth)")

    # Pull real options chain from Polygon
    try:
        chain = []
        for ticker in tickers_to_show:
            for option in client.list_snapshot_options_chain(
                ticker,
                params={
                    "expiration_date.gte": "2026-04-01",   # adjust as needed
                    "limit": 500
                }
            ):
                chain.append(option)
        
        if not chain:
            st.error("No options data returned. Try a different ticker or check API key.")
            st.stop()

        # Convert to DataFrame
        df_list = []
        for o in chain:
            df_list.append({
                "Expiration": o.expiration_date,
                "Strike": o.strike_price,
                "Type": o.contract_type.upper(),
                "Volume": o.day.volume if hasattr(o.day, 'volume') else 0,
                "OI": o.open_interest if hasattr(o, 'open_interest') else 0,
                "LastPrice": o.day.close if hasattr(o.day, 'close') else 0
            })
        
        options_df = pd.DataFrame(df_list)

        # Approximate GEX (real gamma not available on free tier)
        spot_price = 450  # placeholder — in production fetch real quote
        options_df["Distance"] = abs(options_df["Strike"] - spot_price)
        options_df["Approx_Gamma"] = np.exp(-options_df["Distance"] / 30) * 0.08   # higher near ATM
        options_df["GEX"] = options_df["Approx_Gamma"] * options_df["OI"] * 100 * np.where(options_df["Type"] == "CALL", 1, -1)
        options_df["GEX"] = options_df["GEX"].round(0)

        # Pivot for table (Expiration rows, Strike columns)
        pivot_df = options_df.pivot_table(
            index="Expiration", 
            columns="Strike", 
            values="GEX", 
            aggfunc="sum"
        ).fillna(0).round(0)

        # Keep only reasonable strikes for readability
        pivot_df = pivot_df.loc[:, pivot_df.columns[(pivot_df.columns >= spot_price - 80) & (pivot_df.columns <= spot_price + 80)]]

        # Create Skylit-style heatmap table
        colors = []
        for row in pivot_df.values:
            row_colors = []
            for val in row:
                if val > 500:
                    row_colors.append("#00cc66")   # strong positive green
                elif val > 50:
                    row_colors.append("#00ff99")
                elif abs(val) < 30:
                    row_colors.append("#ffffff")   # neutral
                elif val > -200:
                    row_colors.append("#ff6666")
                else:
                    row_colors.append("#cc0000")   # strong negative red
            colors.append(row_colors)

        fig = go.Figure(data=[go.Table(
            header=dict(
                values=["Expiration"] + [f"${int(s)}" for s in pivot_df.columns],
                fill_color="#1a0033",
                font=dict(color="#00ffcc", size=14),
                align="center"
            ),
            cells=dict(
                values=[pivot_df.index] + [pivot_df[col] for col in pivot_df.columns],
                fill_color=[["#1a0033"]] + colors,
                font=dict(color="#111111", size=13),
                align="center",
                height=38
            )
        )])

        fig.update_layout(
            title=f"Gamma Exposure Heatmap — {', '.join(tickers_to_show)}",
            height=620,
            margin=dict(l=10, r=10, t=50, b=10),
            template="plotly_dark"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.caption("🟢 Strong Positive GEX (stabilizing) • 🔴 Strong Negative GEX (amplifying) • White = Neutral")

    except Exception as e:
        st.error(f"Error fetching Polygon data: {e}")
        st.info("Free tier has rate limits and limited depth. Try fewer tickers or refresh later.")

# ===================== LIVE FLOW READS =====================
with tab3:
    st.subheader("📊 Live Flow Reads")
    if client:
        st.success("Real options flow would go here (expand with Polygon trades/aggs if needed)")
        # Placeholder — can be expanded later
        st.dataframe(pd.DataFrame({
            "Ticker": tickers_to_show,
            "Recent Sweep": ["Yes", "No"][:len(tickers_to_show)],
            "Aggression": [78.5, 45.2][:len(tickers_to_show)]
        }), use_container_width=True, hide_index=True)
    else:
        st.warning("Enter Polygon key to see flow data.")

st.success("✅ Connected to Polygon Free Tier • Real Chain + Approximated GEX")
st.caption("Full accurate GEX needs paid tier (Greeks) or Unusual Whales integration.")

st.markdown("---")
st.caption("More visually aggressive than Skylit • Built with ❤️ for the flow")
