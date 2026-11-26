# E-commerce Sales Analysis

An end-to-end business analytics portfolio project using the **UCI Online Retail** transactional dataset. The project demonstrates data preparation with Python, business analysis with SQL, and dashboard design in Power BI.

> **Project status:** Starter implementation. Run the pipeline on the source dataset before reporting any metrics or findings. No performance figures or business conclusions are pre-filled.

## Business questions
1. How do revenue and order volumes change over time?
2. Which products and countries contribute most to revenue?
3. What is the average order value (AOV)?
4. How concentrated is revenue among customers?
5. What does customer recency, frequency and monetary (RFM) behaviour look like?

## Tech stack
- Python: pandas, numpy, matplotlib
- SQL: SQLite-compatible SQL
- Power BI: Power Query and DAX measures
- Git/GitHub: version control and portfolio documentation

## Dataset
Use the **UCI Online Retail** dataset, covering transactions from 1 December 2010 to 9 December 2011. The source workbook contains 541,909 invoice-line records and is licensed under CC BY 4.0.
- Source: https://archive.ics.uci.edu/dataset/352/online-retail
- DOI: https://doi.org/10.24432/C5BW33
- Citation: Chen, D. (2015). *Online Retail* [Dataset]. UCI Machine Learning Repository.

The raw workbook is downloaded by the pipeline and is intentionally excluded from Git because it is large and belongs to the upstream dataset.

## Repository structure
```text
ecommerce-sales-analysis/
├── data/
│   ├── raw/                 # downloaded source workbook (gitignored)
│   └── processed/           # cleaned CSV and SQLite database (gitignored)
├── outputs/                 # generated summaries and charts (gitignored)
├── powerbi/
│   ├── DAX_MEASURES.md
│   └── DASHBOARD_GUIDE.md
├── sql/
│   ├── schema.sql
│   └── analysis_queries.sql
├── src/
│   ├── download_data.py
│   └── analyze.py
├── .gitignore
├── requirements.txt
└── README.md
```

## Run locally
Python 3.10+ is recommended.
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
python src/download_data.py
python src/analyze.py
```

The analysis script creates:
- `data/processed/online_retail_clean.csv`
- `data/processed/online_retail.db`
- `outputs/kpi_summary.csv`
- `outputs/monthly_sales.csv`
- `outputs/top_products.csv`
- `outputs/top_countries.csv`
- `outputs/monthly_revenue.png`

## Cleaning approach
The pipeline preserves the original source file and creates a separate analysis-ready table. It:
- standardizes column names and data types;
- parses invoice timestamps;
- removes rows without a customer ID for customer-level analysis;
- excludes cancellation invoices (invoice numbers beginning with `C`);
- excludes non-positive quantities and unit prices from sales calculations;
- calculates line revenue as `quantity * unit_price`.

These are explicit analytical choices, not claims that the source records are erroneous. The script prints row counts at each stage so the impact can be measured and explained.

## SQL analysis
Open `sql/schema.sql` and `sql/analysis_queries.sql`. The Python pipeline loads the cleaned data into SQLite as `sales` so the queries can be run directly.

## Power BI
Follow `powerbi/DASHBOARD_GUIDE.md` and copy measures from `powerbi/DAX_MEASURES.md`. Import the cleaned CSV (or connect to the SQLite database with an appropriate connector).

Suggested pages:
1. Executive overview: revenue, orders, customers, AOV, monthly trend.
2. Product performance: top products, revenue share, units sold.
3. Geographic performance: revenue and orders by country.
4. Customer analysis: RFM distribution and repeat-customer behaviour.

## Reporting results honestly
Only add metrics to a resume after running the pipeline and reviewing the generated outputs. Suggested resume wording after verification:

> Analyzed **[verified row count]** UCI retail invoice lines using Python, SQL and Power BI; built a KPI dashboard covering revenue, orders, AOV and customer behaviour, and identified **[verified finding]**.

Do not describe this personal project as employment or an internship.

## License and attribution
Project code: MIT License (see `LICENSE`).
Dataset: CC BY 4.0; attribution is required. The dataset remains the property of its original publisher/contributors.
