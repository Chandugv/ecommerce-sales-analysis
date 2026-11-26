"""Clean UCI Online Retail data, create reproducible summaries and SQLite tables."""
from pathlib import Path
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"
OUTPUT_DIR = ROOT / "outputs"


def locate_workbook():
    files = list(RAW_DIR.glob("*.xlsx"))
    if not files:
        raise FileNotFoundError("Run `python src/download_data.py` first.")
    return files[0]


def main():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    source = locate_workbook()
    df = pd.read_excel(source, engine="openpyxl")
    raw_rows = len(df)
    df.columns = [str(c).strip().replace(" ", "_") for c in df.columns]
    required = ["InvoiceNo", "StockCode", "Description", "Quantity",
                "InvoiceDate", "UnitPrice", "CustomerID", "Country"]
    missing_columns = sorted(set(required) - set(df.columns))
    if missing_columns:
        raise ValueError(f"Unexpected source schema; missing columns: {missing_columns}")

    df["InvoiceNo"] = df["InvoiceNo"].astype(str).str.strip()
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df["UnitPrice"] = pd.to_numeric(df["UnitPrice"], errors="coerce")
    df["CustomerID"] = pd.to_numeric(df["CustomerID"], errors="coerce")
    df["Country"] = df["Country"].astype("string").str.strip()
    df["Description"] = df["Description"].astype("string").str.strip()

    invalid_dates = int(df["InvoiceDate"].isna().sum())
    missing_customer = int(df["CustomerID"].isna().sum())
    cancellation_rows = int(df["InvoiceNo"].str.upper().str.startswith("C").sum())
    nonpositive_qty = int((df["Quantity"] <= 0).sum())
    nonpositive_price = int((df["UnitPrice"] <= 0).sum())

    clean = df.dropna(subset=["InvoiceNo", "StockCode", "InvoiceDate",
                              "Quantity", "UnitPrice", "Country"]).copy()
    clean = clean[~clean["InvoiceNo"].str.upper().str.startswith("C")]
    clean = clean[(clean["Quantity"] > 0) & (clean["UnitPrice"] > 0)]
    clean = clean.dropna(subset=["CustomerID"]).copy()
    clean["CustomerID"] = clean["CustomerID"].astype("int64").astype(str)
    clean["Revenue"] = clean["Quantity"] * clean["UnitPrice"]
    clean["OrderDate"] = clean["InvoiceDate"].dt.date.astype(str)
    clean["YearMonth"] = clean["InvoiceDate"].dt.to_period("M").astype(str)
    clean.to_csv(PROCESSED_DIR / "online_retail_clean.csv", index=False)

    monthly = (clean.groupby("YearMonth", as_index=False)
               .agg(Revenue=("Revenue", "sum"),
                    Orders=("InvoiceNo", "nunique"),
                    Units_Sold=("Quantity", "sum")))
    monthly.to_csv(OUTPUT_DIR / "monthly_sales.csv", index=False)
    products = (clean.groupby(["StockCode", "Description"], as_index=False)
                .agg(Revenue=("Revenue", "sum"),
                     Units_Sold=("Quantity", "sum"),
                     Orders=("InvoiceNo", "nunique"))
                .sort_values("Revenue", ascending=False))
    products.head(20).to_csv(OUTPUT_DIR / "top_products.csv", index=False)
    countries = (clean.groupby("Country", as_index=False)
                 .agg(Revenue=("Revenue", "sum"),
                      Orders=("InvoiceNo", "nunique"),
                      Customers=("CustomerID", "nunique"))
                 .sort_values("Revenue", ascending=False))
    countries.to_csv(OUTPUT_DIR / "top_countries.csv", index=False)

    total_revenue = float(clean["Revenue"].sum())
    total_orders = int(clean["InvoiceNo"].nunique())
    total_customers = int(clean["CustomerID"].nunique())
    aov = total_revenue / total_orders if total_orders else 0
    kpis = pd.DataFrame([
        ("source_rows", raw_rows), ("clean_rows", len(clean)),
        ("rows_removed_by_pipeline", raw_rows - len(clean)),
        ("invalid_dates_in_source", invalid_dates),
        ("missing_customer_ids_in_source", missing_customer),
        ("cancellation_invoice_lines_in_source", cancellation_rows),
        ("nonpositive_quantity_lines_in_source", nonpositive_qty),
        ("nonpositive_price_lines_in_source", nonpositive_price),
        ("revenue_gbp", round(total_revenue, 2)),
        ("unique_orders", total_orders), ("unique_customers", total_customers),
        ("average_order_value_gbp", round(aov, 2)),
    ], columns=["metric", "value"])
    kpis.to_csv(OUTPUT_DIR / "kpi_summary.csv", index=False)

    with sqlite3.connect(PROCESSED_DIR / "online_retail.db") as conn:
        clean.to_sql("sales", conn, if_exists="replace", index=False)

    plt.figure(figsize=(11, 5))
    plt.plot(monthly["YearMonth"], monthly["Revenue"], marker="o")
    plt.title("Monthly Revenue")
    plt.xlabel("Month")
    plt.ylabel("Revenue (£)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "monthly_revenue.png", dpi=160)
    plt.close()

    print("\n=== DATA PIPELINE SUMMARY ===")
    print(f"Source rows: {raw_rows:,}")
    print(f"Clean rows: {len(clean):,}")
    print(f"Rows excluded by documented rules: {raw_rows - len(clean):,}")
    print(f"Revenue (£): {total_revenue:,.2f}")
    print(f"Orders: {total_orders:,}")
    print(f"Customers: {total_customers:,}")
    print(f"AOV (£): {aov:,.2f}")
    print(f"\nOutputs written to: {OUTPUT_DIR}")
    print("Review the exclusions and summaries before writing business conclusions.")


if __name__ == "__main__":
    main()
