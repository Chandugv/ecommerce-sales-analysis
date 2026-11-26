# Power BI Dashboard Build Guide

## Load data
1. Run the Python pipeline.
2. In Power BI Desktop, choose **Get data → Text/CSV**.
3. Import `data/processed/online_retail_clean.csv`.
4. Confirm data types: dates as Date/Time, quantity as Whole Number, unit price and revenue as Decimal Number, IDs as Text.
5. Create a date-only column in Power Query if needed and build a calendar table.

## Page 1 — Executive Overview
- Cards: Total Revenue, Total Orders, Total Customers, Average Order Value.
- Line chart: Revenue by YearMonth.
- Bar chart: Revenue by Country (Top 10).
- Slicers: Date, Country.

## Page 2 — Product Performance
- Bar chart: Top 10 products by Revenue.
- Matrix: Product, Revenue, Units Sold, Orders.
- Slicers: Date, Country.

## Page 3 — Customer Insights
- Cards: Customers, Revenue per Customer, Repeat Customer Share.
- Bar chart: customer order-frequency distribution.
- Table: Customer ID, Recency, Frequency, Monetary value.
- Slicers: Country, date.

## Design checks
- Use consistent GBP currency formatting.
- Label the reporting period.
- Add a note that cancelled invoices and non-positive quantity/price rows are excluded from the sales analysis.
- Validate visuals against the SQL outputs before publishing.
- Do not publish customer-level identifiers publicly; aggregate customer results in screenshots.
