-- SQLite schema. The Python pipeline creates the `sales` table from the cleaned CSV.
CREATE TABLE IF NOT EXISTS sales (
    InvoiceNo TEXT NOT NULL,
    StockCode TEXT NOT NULL,
    Description TEXT,
    Quantity INTEGER NOT NULL,
    InvoiceDate TEXT NOT NULL,
    UnitPrice REAL NOT NULL,
    CustomerID TEXT NOT NULL,
    Country TEXT NOT NULL,
    Revenue REAL NOT NULL,
    OrderDate TEXT NOT NULL,
    YearMonth TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_sales_invoice ON sales(InvoiceNo);
CREATE INDEX IF NOT EXISTS idx_sales_customer ON sales(CustomerID);
CREATE INDEX IF NOT EXISTS idx_sales_date ON sales(InvoiceDate);
CREATE INDEX IF NOT EXISTS idx_sales_country ON sales(Country);
