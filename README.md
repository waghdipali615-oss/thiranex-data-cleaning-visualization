# Thiranex Internship — Data Science Task 1
## Data Cleaning & Visualization Project

This beginner-friendly project demonstrates how to clean a raw dataset, explore it with Python, and present key findings in an interactive dashboard.

> **Dataset note:** `data/raw_sales_data.csv` is a synthetic practice dataset created for this project. It is not real company or customer data.

## Project structure

```text
Thiranex_Data_Cleaning_Visualization_Project/
├── app.py
├── requirements.txt
├── data/
│   ├── raw_sales_data.csv
│   └── cleaned_sales_data.csv
├── src/
│   ├── clean_data.py
│   └── analysis.py
└── outputs/
    ├── cleaning_summary.txt
    ├── key_findings.txt
    └── charts/
        ├── sales_by_product.png
        ├── sales_by_region.png
        ├── monthly_sales_trend.png
        └── sales_distribution.png
```

## Tools used
- Python — programming language
- Pandas and NumPy — data cleaning and processing
- Matplotlib and Seaborn — static charts
- Streamlit and Plotly — interactive dashboard

## Data cleaning performed
1. Checked missing values and duplicate records.
2. Standardized text fields by trimming spaces and using consistent capitalization.
3. Converted date and numeric columns to appropriate data types.
4. Removed exact duplicate rows.
5. Treated invalid quantity, unit-price, and discount values as missing values using domain rules.
6. Filled missing categorical values with the mode and numeric values with the median.
7. Recalculated `Sales = Quantity × Unit_Price`.
8. Created an `Order_Month` field for time-based analysis.

## How to run (Windows / VS Code)

### 1. Extract the ZIP
Extract the project folder somewhere easy to find, then open that folder in VS Code.

### 2. Open the terminal
In VS Code, choose **Terminal → New Terminal**.

### 3. Create and activate a virtual environment (recommended)
```bash
python -m venv .venv
.venv\Scripts\activate
```
If PowerShell blocks activation, use Command Prompt or continue with your usual Python environment.

### 4. Install packages
```bash
pip install -r requirements.txt
```

### 5. Run data cleaning
```bash
python src/clean_data.py
```

### 6. Generate charts and key findings
```bash
python src/analysis.py
```

### 7. Launch the interactive dashboard
```bash
streamlit run app.py
```
A local browser tab should open with filters for region, product, and date. Stop the dashboard with `Ctrl + C` in the terminal.

## Expected outcome
- A cleaned CSV file with standardized values and no exact duplicates.
- A text report describing the cleaning steps.
- Four charts showing product sales, regional sales, monthly sales trend, and order-sales distribution.
- An interactive dashboard with key metrics, filters, charts, and CSV export.

## Suggested presentation summary
"I used Python to clean a raw sales dataset. First, I checked missing values and duplicates, corrected data types and inconsistent text, and handled invalid values. Then I used Pandas for processing and Matplotlib/Seaborn for visualizations. Finally, I created a Streamlit dashboard with sales KPIs, product and region comparisons, and a monthly sales trend. This project demonstrates the full workflow from raw data to useful insights."

## Important before submitting
- Open the dashboard and take your own screenshots for the internship report.
- Read `outputs/key_findings.txt` and use the values from your generated output when explaining results.
- If Thiranex provided a specific dataset or tutorial, replace the practice CSV with that official dataset and adapt the column names and cleaning rules. Do not claim this synthetic dataset is official Thiranex data.
