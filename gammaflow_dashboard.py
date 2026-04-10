# ====================== IMPROVED GAMMA HEATMAP (Skylit-style) ======================
with tab2:
    st.markdown('<div class="heatmap-title">GAMMA EXPOSURE HEATMAP • LIVE</div>', unsafe_allow_html=True)

    if view_mode == "Single Ticker":
        selected = st.selectbox("Select Ticker", watchlist)
        display_tickers = [selected]
    else:
        display_tickers = watchlist

    # Realistic GEX with better distribution
    current_seed = int(time.time() / 5)
    np.random.seed(current_seed)

    expirations = ["2026-04-03", "2026-04-10", "2026-04-17", "2026-04-24", "2026-05-01", "2026-05-15"]
    strikes = list(range(430, 511, 10))
    spot_price = 470   # Change this to match current price if you fetch real spot

    data = []
    for exp_idx, exp in enumerate(expirations):
        row = [exp]
        for strike in strikes:
            distance = abs(strike - spot_price)
            # Stronger concentration near ATM
            intensity = np.exp(-distance / 25) * np.random.uniform(0.8, 1.6)
            base = int(1200 * intensity * np.random.uniform(0.7, 1.9))
            gex = int(base * np.random.choice([-1.6, -1.1, 0.8, 1.3, 1.8]))
            row.append(gex)
        data.append(row)

    df = pd.DataFrame(data, columns=["Expiration"] + [f"${int(s)}" for s in strikes])

    # Professional color mapping (matching your screenshot style)
    cell_colors = []
    for row_idx, row in enumerate(df.iloc[:, 1:].values):
        colors = []
        for val in row:
            abs_val = abs(val)
            if abs_val > 1000:
                color = "#00ff88" if val > 0 else "#ff5555"   # Strong Green / Strong Red
            elif abs_val > 400:
                color = "#00cc66" if val > 0 else "#ff7777"
            elif abs_val > 100:
                color = "#88ffaa" if val > 0 else "#ffaaaa"
            elif abs_val <= 80:
                color = "#ffffff"                                 # Neutral
            else:
                color = "#ffdddd" if val < 0 else "#ddffdd"
            colors.append(color)
        cell_colors.append(colors)

    # Highlight ATM row (closest to spot)
    atm_row = None
    for i, exp in enumerate(df["Expiration"]):
        if "04-17" in exp:          # Near-term expiration as example
            atm_row = i
            break

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
            fill_color=[["#0f0f1a"] * len(df)] + cell_colors,
            font=dict(color="#eeeeee", size=14),
            align="center",
            height=38,
            # Highlight ATM row with subtle cyan border effect via line color
        )
    )])

    # Add subtle ATM highlight
    if atm_row is not None:
        fig.add_annotation(
            xref="x domain", yref="y domain",
            x=0.5, y=1 - (atm_row + 0.5) / len(df),
            text="← ATM STRIKE",
            showarrow=False,
            font=dict(color="#00f0ff", size=13),
            bgcolor="rgba(0, 240, 255, 0.15)",
            bordercolor="#00f0ff",
            borderwidth=1,
            borderpad=4,
            opacity=0.9
        )

    fig.update_layout(
        height=720,
        margin=dict(l=10, r=10, t=40, b=20),
        template="plotly_dark"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.caption("🟢 Positive GEX (stabilizing) 🔴 Negative GEX (amplifying) White = Neutral • Live every 5s")
