-- Run these queries against data/processed/online_retail.db.
-- 1. Executive KPIs
SELECT ROUND(SUM(Revenue), 2) AS total_revenue_gbp,
       COUNT(DISTINCT InvoiceNo) AS total_orders,
       COUNT(DISTINCT CustomerID) AS total_customers,
       ROUND(SUM(Revenue) / COUNT(DISTINCT InvoiceNo), 2) AS average_order_value_gbp
FROM sales;

-- 2. Monthly revenue and order trend
SELECT YearMonth, ROUND(SUM(Revenue), 2) AS revenue_gbp,
       COUNT(DISTINCT InvoiceNo) AS orders, SUM(Quantity) AS units_sold
FROM sales GROUP BY YearMonth ORDER BY YearMonth;

-- 3. Top 10 products by revenue
SELECT StockCode, Description, ROUND(SUM(Revenue), 2) AS revenue_gbp,
       SUM(Quantity) AS units_sold
FROM sales GROUP BY StockCode, Description
ORDER BY revenue_gbp DESC LIMIT 10;

-- 4. Country performance
SELECT Country, ROUND(SUM(Revenue), 2) AS revenue_gbp,
       COUNT(DISTINCT InvoiceNo) AS orders,
       COUNT(DISTINCT CustomerID) AS customers
FROM sales GROUP BY Country ORDER BY revenue_gbp DESC;

-- 5. Repeat customer analysis
WITH customer_orders AS (
    SELECT CustomerID, COUNT(DISTINCT InvoiceNo) AS order_count
    FROM sales GROUP BY CustomerID
)
SELECT CASE WHEN order_count = 1 THEN 'One-time' ELSE 'Repeat' END AS customer_type,
       COUNT(*) AS customers,
       ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM customer_orders), 2) AS customer_share_pct
FROM customer_orders GROUP BY customer_type;

-- 6. Customer-level RFM base table (reference date = day after latest invoice)
WITH customer_rfm AS (
    SELECT CustomerID,
           CAST(julianday((SELECT DATE(MAX(InvoiceDate), '+1 day') FROM sales))
                - julianday(MAX(InvoiceDate)) AS INTEGER) AS Recency_Days,
           COUNT(DISTINCT InvoiceNo) AS Frequency,
           ROUND(SUM(Revenue), 2) AS Monetary_GBP
    FROM sales GROUP BY CustomerID
)
SELECT * FROM customer_rfm ORDER BY Monetary_GBP DESC;
