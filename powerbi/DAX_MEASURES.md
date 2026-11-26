# Power BI DAX Measures

Import `data/processed/online_retail_clean.csv` into Power BI. Rename the table to `Sales` (or adjust the table name below).

```dax
Total Revenue = SUM(Sales[Revenue])
Total Orders = DISTINCTCOUNT(Sales[InvoiceNo])
Total Customers = DISTINCTCOUNT(Sales[CustomerID])
Units Sold = SUM(Sales[Quantity])
Average Order Value = DIVIDE([Total Revenue], [Total Orders], 0)
Revenue per Customer = DIVIDE([Total Revenue], [Total Customers], 0)

Revenue MoM % =
VAR CurrentRevenue = [Total Revenue]
VAR PreviousRevenue =
    CALCULATE([Total Revenue], DATEADD('Date'[Date], -1, MONTH))
RETURN DIVIDE(CurrentRevenue - PreviousRevenue, PreviousRevenue)
```

Create a calendar table and mark it as the date table:

```dax
Date =
CALENDAR(MIN(Sales[InvoiceDate]), MAX(Sales[InvoiceDate]))
```

Add calculated columns to `Date`:
```dax
Year = YEAR('Date'[Date])
Month = FORMAT('Date'[Date], "MMM")
YearMonth = FORMAT('Date'[Date], "YYYY-MM")
MonthNumber = MONTH('Date'[Date])
```

Sort `Date[Month]` by `Date[MonthNumber]` and create a relationship from `Date[Date]` to the date-only column in Sales. If using the timestamp field, create a date-only column in Power Query first.
