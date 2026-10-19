"""
Exploratory analysis and chart generation.
Run: python src/analysis.py
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "cleaned_sales_data.csv"
CHARTS = ROOT / "outputs" / "charts"
CHARTS.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA, parse_dates=["Order_Date"])

product_sales = df.groupby("Product")["Sales"].sum().sort_values()
plt.figure(figsize=(9, 5))
plt.barh(product_sales.index, product_sales.values)
plt.title("Total Sales by Product")
plt.xlabel("Sales")
plt.ylabel("Product")
plt.tight_layout()
plt.savefig(CHARTS / "sales_by_product.png", dpi=160)
plt.close()

region_sales = df.groupby("Region")["Sales"].sum().sort_values()
plt.figure(figsize=(8, 5))
plt.bar(region_sales.index, region_sales.values)
plt.title("Total Sales by Region")
plt.xlabel("Region")
plt.ylabel("Sales")
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig(CHARTS / "sales_by_region.png", dpi=160)
plt.close()

monthly = df.groupby("Order_Month")["Sales"].sum().sort_index()
plt.figure(figsize=(10, 5))
plt.plot(monthly.index, monthly.values, marker="o")
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(CHARTS / "monthly_sales_trend.png", dpi=160)
plt.close()

plt.figure(figsize=(9, 5))
plt.hist(df["Sales"], bins=30)
plt.title("Distribution of Order Sales")
plt.xlabel("Sales per Order")
plt.ylabel("Number of Orders")
plt.tight_layout()
plt.savefig(CHARTS / "sales_distribution.png", dpi=160)
plt.close()

top_product = product_sales.idxmax()
top_region = region_sales.idxmax()
report = f"""EXPLORATORY DATA ANALYSIS - KEY FINDINGS
========================================
Cleaned records: {len(df):,}
Total sales: {df['Sales'].sum():,.2f}
Average sales per order: {df['Sales'].mean():,.2f}
Top product by sales: {top_product} ({df.groupby('Product')['Sales'].sum().max():,.2f})
Top region by sales: {top_region} ({df.groupby('Region')['Sales'].sum().max():,.2f})
Number of product categories: {df['Category'].nunique()}
Date range: {df['Order_Date'].min().date()} to {df['Order_Date'].max().date()}

Interpretation:
- The product with the highest total sales may be a priority for inventory planning.
- Regional totals can help compare sales performance between regions.
- The monthly trend shows how sales change over time.
- The distribution chart helps identify typical order values and unusually large values.

Note: This is a practice dataset created for this project. Results are illustrative and are not real company data.
"""
(ROOT / "outputs" / "key_findings.txt").write_text(report, encoding="utf-8")
print(report)
print(f"Charts saved to {CHARTS}")
