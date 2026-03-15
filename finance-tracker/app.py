import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import os

st.set_page_config(page_title="Personal Finance Tracker", page_icon="💰", layout="wide")

st.markdown("""
<style>
    .main { background-color: #0a0e1a; }
    .block-container { padding: 2rem 3rem; }
    h1 {
        background: linear-gradient(90deg, #00d4ff, #00ff88);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-size: 3rem !important;
        font-weight: 900 !important;
    }
    .income-card {
        background: linear-gradient(135deg, #1a3a2a, #0d2a1a);
        border-radius: 15px;
        padding: 20px;
        border-left: 4px solid #00ff88;
    }
    .expense-card {
        background: linear-gradient(135deg, #3a1a1a, #2a0d0d);
        border-radius: 15px;
        padding: 20px;
        border-left: 4px solid #ff4b4b;
    }
    .balance-card {
        background: linear-gradient(135deg, #1a2a3a, #0d1a2a);
        border-radius: 15px;
        padding: 20px;
        border-left: 4px solid #00d4ff;
    }
    div[data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 800 !important;
    }
    .stButton button {
        background: linear-gradient(90deg, #00d4ff, #00ff88);
        color: black;
        font-weight: 700;
        border-radius: 10px;
        border: none;
        padding: 10px 20px;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>💰 Personal Finance Tracker</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#888'>Track your income • Monitor expenses • Achieve your goals</p>", unsafe_allow_html=True)
st.markdown("---")

# ── DATA STORAGE ──
DATA_FILE = "finance_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

if "transactions" not in st.session_state:
    st.session_state.transactions = load_data()

# ── SIDEBAR - ADD TRANSACTION ──
st.sidebar.markdown("## ➕ Add Transaction")
st.sidebar.markdown("---")

trans_type = st.sidebar.selectbox("Type", ["💚 Income", "🔴 Expense"])
amount = st.sidebar.number_input("Amount (£)", min_value=0.01, value=100.0, step=0.01)

if "Income" in trans_type:
    categories = ["💼 Salary", "💰 Freelance", "📈 Investment", "🎁 Gift", "Other"]
else:
    categories = ["🏠 Rent", "🛒 Groceries", "🚗 Transport", "🎬 Entertainment",
                  "💊 Health", "👗 Shopping", "🍔 Food & Drink", "📱 Bills", "Other"]

category = st.sidebar.selectbox("Category", categories)
description = st.sidebar.text_input("Description", placeholder="e.g. Monthly salary")
date = st.sidebar.date_input("Date", datetime.today())

if st.sidebar.button("➕ Add Transaction"):
    transaction = {
        "type": "Income" if "Income" in trans_type else "Expense",
        "amount": amount,
        "category": category,
        "description": description,
        "date": str(date)
    }
    st.session_state.transactions.append(transaction)
    save_data(st.session_state.transactions)
    st.sidebar.success("✅ Transaction added!")

# ── MAIN CONTENT ──
if st.session_state.transactions:
    df = pd.DataFrame(st.session_state.transactions)
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.strftime("%Y-%m")

    total_income = df[df["type"] == "Income"]["amount"].sum()
    total_expense = df[df["type"] == "Expense"]["amount"].sum()
    balance = total_income - total_expense

    # ── METRICS ──
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💚 Total Income", f"£{total_income:,.2f}")
    with col2:
        st.metric("🔴 Total Expenses", f"£{total_expense:,.2f}")
    with col3:
        st.metric("💙 Balance", f"£{balance:,.2f}",
                 delta=f"£{balance:,.2f}",
                 delta_color="normal")

    st.markdown("---")

    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📈 Trends", "🏷️ Categories", "📋 Transactions"])

    # ── TAB 1: OVERVIEW ──
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            fig_pie = px.pie(
                df, values="amount", names="type",
                title="💰 Income vs Expenses",
                color="type",
                color_discrete_map={"Income": "#00ff88", "Expense": "#ff4b4b"},
                template="plotly_dark"
            )
            fig_pie.update_layout(paper_bgcolor="#0a0e1a")
            st.plotly_chart(fig_pie, use_container_width=True)

        with col2:
            expense_df = df[df["type"] == "Expense"]
            if not expense_df.empty:
                fig_exp = px.pie(
                    expense_df, values="amount", names="category",
                    title="🔴 Expenses by Category",
                    template="plotly_dark",
                    color_discrete_sequence=px.colors.qualitative.Bold
                )
                fig_exp.update_layout(paper_bgcolor="#0a0e1a")
                st.plotly_chart(fig_exp, use_container_width=True)

    # ── TAB 2: TRENDS ──
    with tab2:
        monthly = df.groupby(["month", "type"])["amount"].sum().reset_index()
        fig_bar = px.bar(
            monthly, x="month", y="amount", color="type",
            title="📈 Monthly Income vs Expenses",
            template="plotly_dark",
            color_discrete_map={"Income": "#00ff88", "Expense": "#ff4b4b"},
            barmode="group"
        )
        fig_bar.update_layout(paper_bgcolor="#0a0e1a", plot_bgcolor="#0a0e1a",
                             font=dict(color="white"))
        st.plotly_chart(fig_bar, use_container_width=True)

        monthly_balance = df.pivot_table(index="month", columns="type",
                                        values="amount", aggfunc="sum").fillna(0)
        if "Income" in monthly_balance and "Expense" in monthly_balance:
            monthly_balance["Balance"] = monthly_balance["Income"] - monthly_balance["Expense"]
            fig_line = px.line(
                monthly_balance.reset_index(), x="month", y="Balance",
                title="💙 Monthly Balance Trend",
                template="plotly_dark",
                color_discrete_sequence=["#00d4ff"]
            )
            fig_line.update_layout(paper_bgcolor="#0a0e1a", plot_bgcolor="#0a0e1a",
                                  font=dict(color="white"))
            fig_line.update_traces(line=dict(width=3))
            st.plotly_chart(fig_line, use_container_width=True)

    # ── TAB 3: CATEGORIES ──
    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 💚 Income Sources")
            income_df = df[df["type"] == "Income"].groupby("category")["amount"].sum().reset_index()
            if not income_df.empty:
                fig_inc = px.bar(income_df, x="amount", y="category",
                                orientation="h",
                                color="amount",
                                color_continuous_scale="Greens",
                                template="plotly_dark")
                fig_inc.update_layout(paper_bgcolor="#0a0e1a", plot_bgcolor="#0a0e1a",
                                     font=dict(color="white"))
                st.plotly_chart(fig_inc, use_container_width=True)

        with col2:
            st.markdown("### 🔴 Expense Categories")
            exp_cat = df[df["type"] == "Expense"].groupby("category")["amount"].sum().reset_index()
            if not exp_cat.empty:
                fig_exp_bar = px.bar(exp_cat, x="amount", y="category",
                                    orientation="h",
                                    color="amount",
                                    color_continuous_scale="Reds",
                                    template="plotly_dark")
                fig_exp_bar.update_layout(paper_bgcolor="#0a0e1a", plot_bgcolor="#0a0e1a",
                                         font=dict(color="white"))
                st.plotly_chart(fig_exp_bar, use_container_width=True)

    # ── TAB 4: TRANSACTIONS ──
    with tab4:
        st.markdown("### 📋 All Transactions")
        filter_type = st.selectbox("Filter by type", ["All", "Income", "Expense"])
        if filter_type != "All":
            display_df = df[df["type"] == filter_type]
        else:
            display_df = df
        display_df = display_df.sort_values("date", ascending=False)
        st.dataframe(display_df[["date", "type", "category", "description", "amount"]],
                    use_container_width=True)

        if st.button("🗑️ Clear All Transactions"):
            st.session_state.transactions = []
            save_data([])
            st.success("All transactions cleared!")
            st.rerun()
else:
    st.info("👈 Add your first transaction using the sidebar on the left!")
    st.markdown("### 💡 How to use:")
    st.markdown("1. Select **Income** or **Expense** from the sidebar")
    st.markdown("2. Enter the **amount** and **category**")
    st.markdown("3. Click **Add Transaction**")
    st.markdown("4. Watch your **charts update automatically!** 📊")

st.markdown("---")
st.markdown("<p style='text-align:center; color:#555'>Built by Vinothini | Personal Finance Tracker</p>", unsafe_allow_html=True)