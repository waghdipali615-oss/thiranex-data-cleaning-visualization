"""
Interactive Streamlit dashboard.
Run: streamlit run app.py
"""
from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "cleaned_sales_data.csv"

st.set_page_config(page_title="Sales Data Insights", page_icon="📊", layout="wide")
st.title("📊 Data Cleaning & Visualization Dashboard")
st.caption("Thiranex Internship — Data Science Task 1 | Sample practice dataset")

if not DATA_PATH.exists():
    st.error("Cleaned dataset not found. Run: python src/clean_data.py")
    st.stop()

df = pd.read_csv(DATA_PATH, parse_dates=["Order_Date"])
with st.sidebar:
    st.header("Filters")
    regions = st.multiselect("Region", sorted(df["Region"].dropna().unique()), default=sorted(df["Region"].dropna().unique()))
    products = st.multiselect("Product", sorted(df["Product"].dropna().unique()), default=sorted(df["Product"].dropna().unique()))
    min_date = df["Order_Date"].min().date()
    max_date = df["Order_Date"].max().date()
    date_range = st.date_input("Order date range", value=(min_date, max_date), min_value=min_date, max_value=max_date)

filtered = df[df["Region"].isin(regions) & df["Product"].isin(products)].copy()
if isinstance(date_range, tuple) and len(date_range) == 2:
    filtered = filtered[(filtered["Order_Date"].dt.date >= date_range[0]) & (filtered["Order_Date"].dt.date <= date_range[1])]

if filtered.empty:
    st.warning("No records match these filters. Please change your selections.")
    st.stop()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Sales", f"₹{filtered['Sales'].sum():,.0f}")
c2.metric("Orders", f"{len(filtered):,}")
c3.metric("Average Order Value", f"₹{filtered['Sales'].mean():,.0f}")
c4.metric("Products", f"{filtered['Product'].nunique()}")

left, right = st.columns(2)
with left:
    p = filtered.groupby("Product", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False)
    st.plotly_chart(px.bar(p, x="Product", y="Sales", title="Sales by Product", text_auto=".2s"), use_container_width=True)
with right:
    r = filtered.groupby("Region", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False)
    st.plotly_chart(px.bar(r, x="Region", y="Sales", title="Sales by Region", color="Region"), use_container_width=True)

monthly = filtered.assign(Order_Month=filtered["Order_Date"].dt.to_period("M").astype(str)).groupby("Order_Month", as_index=False)["Sales"].sum()
st.plotly_chart(px.line(monthly, x="Order_Month", y="Sales", markers=True, title="Monthly Sales Trend"), use_container_width=True)

with st.expander("View cleaned data"):
    st.dataframe(filtered, use_container_width=True)
    st.download_button("Download filtered CSV", filtered.to_csv(index=False).encode("utf-8"), "filtered_sales_data.csv", "text/csv")
