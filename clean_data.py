"""
Data cleaning pipeline for the sample sales dataset.
Run: python src/clean_data.py
"""
from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "data" / "raw_sales_data.csv"
OUT_PATH = ROOT / "data" / "cleaned_sales_data.csv"
REPORT_PATH = ROOT / "outputs" / "cleaning_summary.txt"

def clean_data(df: pd.DataFrame):
    original_rows = len(df)
    missing_before = int(df.isna().sum().sum())
    duplicates_before = int(df.duplicated().sum())

    # Standardize text values
    for col in ["Product", "Category", "Region", "Customer_Segment"]:
        df[col] = df[col].astype("string").str.strip().str.title()

    # Convert data types safely
    df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
    for col in ["Quantity", "Unit_Price", "Sales", "Discount"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Remove exact duplicate rows
    df = df.drop_duplicates().copy()

    # Handle invalid values and outliers using reasonable domain rules.
    # Quantity should be positive and at most 100 for this example dataset.
    df.loc[(df["Quantity"] <= 0) | (df["Quantity"] > 100), "Quantity"] = np.nan
    # Unit price should be positive and below 200,000 in this example dataset.
    df.loc[(df["Unit_Price"] <= 0) | (df["Unit_Price"] > 200000), "Unit_Price"] = np.nan
    # Discount is a proportion and must be between 0 and 1.
    df.loc[(df["Discount"] < 0) | (df["Discount"] > 1), "Discount"] = np.nan

    # Fill missing values: categorical columns use mode; numeric columns use median.
    for col in ["Product", "Category", "Region", "Customer_Segment"]:
        mode = df[col].mode(dropna=True)
        df[col] = df[col].fillna(mode.iloc[0] if not mode.empty else "Unknown")
    for col in ["Quantity", "Unit_Price", "Discount"]:
        df[col] = df[col].fillna(df[col].median())

    # Recalculate sales so the value is consistent with cleaned quantity and price.
    df["Sales"] = (df["Quantity"] * df["Unit_Price"]).round(2)
    # Drop rows where the date could not be interpreted.
    df = df.dropna(subset=["Order_Date"]).copy()
    df["Order_Month"] = df["Order_Date"].dt.to_period("M").astype(str)

    summary = {
        "Rows in raw file": original_rows,
        "Exact duplicate rows removed": duplicates_before,
        "Missing cells before cleaning": missing_before,
        "Rows in cleaned file": len(df),
        "Missing cells after cleaning": int(df.isna().sum().sum()),
        "Duplicate rows after cleaning": int(df.duplicated().sum()),
    }
    return df, summary

def main():
    df = pd.read_csv(RAW_PATH)
    cleaned, summary = clean_data(df)
    cleaned.to_csv(OUT_PATH, index=False)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write("DATA CLEANING SUMMARY\n")
        f.write("=====================\n")
        for key, value in summary.items():
            f.write(f"{key}: {value}\n")
        f.write("\nMethods used:\n")
        f.write("- Standardized text capitalization and whitespace\n")
        f.write("- Converted date and numeric columns to correct types\n")
        f.write("- Removed exact duplicate rows\n")
        f.write("- Replaced invalid quantity, price, and discount values with missing values\n")
        f.write("- Filled categorical missing values with mode and numeric values with median\n")
        f.write("- Recalculated Sales = Quantity x Unit_Price\n")
    print("Cleaning complete.")
    print(f"Saved: {OUT_PATH}")
    print("\n".join(f"{k}: {v}" for k, v in summary.items()))

if __name__ == "__main__":
    main()
