import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from datetime import datetime, timedelta
import random

st.set_page_config(page_title="Smart Analytics Hub", page_icon="🧠", layout="wide")

st.markdown("""
<style>
    .main { background-color: #0e1117; }
    h1 { color: #00d4ff; text-align: center; }
    h2 { color: #ffffff; }
    .stMetric { background-color: #1e2130; padding: 10px; border-radius: 10px; }
    .stTabs [data-baseweb="tab"] { color: white; font-size: 18px; }
</style>
""", unsafe_allow_html=True)

st.title("🧠 Smart Analytics Hub")
st.markdown("<h4 style='text-align:center; color:#888'>Stock Market • Sports • ML Predictions</h4>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📈 Stock Market", "⚽ Sports Analytics", "🤖 ML Prediction"])

# ─── TAB 1: STOCK MARKET ───
with tab1:
    st.subheader("📈 Stock Market Explorer")
    
    stocks = {
        "Apple (AAPL)": "AAPL",
        "Google (GOOGL)": "GOOGL", 
        "Microsoft (MSFT)": "MSFT",
        "Tesla (TSLA)": "TSLA",
        "Amazon (AMZN)": "AMZN"
    }
    
    selected = st.selectbox("Select Stock", list(stocks.keys()))
    days = st.slider("Days of history", 30, 365, 90)
    
    # Generate realistic stock data
    dates = pd.date_range(end=datetime.today(), periods=days)
    base_prices = {"AAPL": 180, "GOOGL": 140, "MSFT": 380, "TSLA": 250, "AMZN": 185}
    base = base_prices[stocks[selected]]
    
    random.seed(42)
    prices = [base]
    for _ in range(days - 1):
        change = random.uniform(-0.03, 0.03)
        prices.append(round(prices[-1] * (1 + change), 2))
    
    df_stock = pd.DataFrame({"Date": dates, "Price": prices})
    df_stock["MA7"] = df_stock["Price"].rolling(7).mean()
    df_stock["MA30"] = df_stock["Price"].rolling(30).mean()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Current Price", f"${prices[-1]:.2f}")
    col2.metric("7 Day Change", f"{((prices[-1]-prices[-7])/prices[-7]*100):.1f}%")
    col3.metric("30 Day High", f"${max(prices[-30:]):.2f}")
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_stock["Date"], y=df_stock["Price"], name="Price", line=dict(color="#00d4ff")))
    fig.add_trace(go.Scatter(x=df_stock["Date"], y=df_stock["MA7"], name="7-day MA", line=dict(color="#ff4b4b", dash="dash")))
    fig.add_trace(go.Scatter(x=df_stock["Date"], y=df_stock["MA30"], name="30-day MA", line=dict(color="#00ff88", dash="dash")))
    fig.update_layout(template="plotly_dark", title=f"{selected} Price History")
    st.plotly_chart(fig, use_container_width=True)

# ─── TAB 2: SPORTS ───
with tab2:
    st.subheader("⚽ Premier League Analytics")
    
    pl_data = {
        "Team": ["Manchester City", "Arsenal", "Liverpool", "Chelsea", "Tottenham",
                 "Manchester United", "Newcastle", "Aston Villa", "Brighton", "West Ham"],
        "Played": [30, 30, 30, 30, 30, 30, 30, 30, 30, 30],
        "Won": [22, 21, 20, 16, 15, 13, 14, 14, 12, 11],
        "Drawn": [5, 4, 5, 6, 6, 7, 5, 4, 8, 7],
        "Lost": [3, 5, 5, 8, 9, 10, 11, 12, 10, 12],
        "Goals For": [72, 75, 68, 55, 58, 35, 55, 62, 48, 37],
        "Goals Against": [28, 25, 30, 45, 50, 48, 42, 48, 44, 52],
    }
    df_pl = pd.DataFrame(pl_data)
    df_pl["Points"] = df_pl["Won"] * 3 + df_pl["Drawn"]
    df_pl["Goal Diff"] = df_pl["Goals For"] - df_pl["Goals Against"]
    df_pl = df_pl.sort_values("Points", ascending=False).reset_index(drop=True)
    df_pl.index += 1

    st.dataframe(df_pl[["Team", "Played", "Won", "Drawn", "Lost", "Goals For", "Goals Against", "Goal Diff", "Points"]], use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        fig_bar = px.bar(df_pl, x="Team", y="Points", color="Points",
                        color_continuous_scale="blues", title="Points Table",
                        template="plotly_dark")
        fig_bar.update_xaxes(tickangle=45)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        fig_scatter = px.scatter(df_pl, x="Goals For", y="Goals Against",
                                size="Points", color="Points",
                                hover_name="Team", title="Attack vs Defence",
                                template="plotly_dark", color_continuous_scale="reds")
        st.plotly_chart(fig_scatter, use_container_width=True)

# ─── TAB 3: ML PREDICTION ───
with tab3:
    st.subheader("🤖 Stock Price Predictor")
    st.markdown("Predict if a stock price will go **UP** or **DOWN** tomorrow!")

    col1, col2 = st.columns(2)
    with col1:
        current_price = st.number_input("Current Price ($)", value=180.0)
        ma7 = st.number_input("7-day Moving Average ($)", value=175.0)
    with col2:
        ma30 = st.number_input("30-day Moving Average ($)", value=170.0)
        volume = st.selectbox("Trading Volume", ["Low", "Medium", "High"])

    if st.button("🔮 Predict Tomorrow"):
        score = 0
        if current_price > ma7: score += 1
        if current_price > ma30: score += 1
        if ma7 > ma30: score += 1
        if volume == "High": score += 1

        if score >= 3:
            st.success("📈 Prediction: Price likely to GO UP tomorrow!")
            confidence = score * 20 + 20
        else:
            st.error("📉 Prediction: Price likely to GO DOWN tomorrow!")
            confidence = (4 - score) * 20 + 20

        st.metric("Confidence Score", f"{confidence}%")

        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=confidence,
            title={"text": "Prediction Confidence"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#00d4ff"},
                "steps": [
                    {"range": [0, 40], "color": "#ff4b4b"},
                    {"range": [40, 70], "color": "#ffa500"},
                    {"range": [70, 100], "color": "#00ff88"}
                ]
            }
        ))
        fig_gauge.update_layout(template="plotly_dark")
        st.plotly_chart(fig_gauge, use_container_width=True)