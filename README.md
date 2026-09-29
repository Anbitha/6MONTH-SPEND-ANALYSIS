# 6MONTH-SPEND-ANALYSIS
A personal finance analytics project that turns raw bank statement transactions into a structured spend profile — uncovering who you are as a spender through category segmentation, anomaly detection, time-of-day patterns, and behavioral archetypes.
What It Does:
1.Cleans messy bank data — parses 4 date formats and 3 currency formats, standardizes transaction types, drops duplicates
2.Categorizes spend — maps 40+ messy vendor strings to clean vendor names, then to 12 spend categories (Food Delivery, Quick Commerce, Ecommerce, Transport, Cafe, Restaurants, Subscriptions, Utilities, Groceries, Investments, Fuel, Entertainment)
3.Builds a Spend DNA report — headline financial stats, category × month spend matrix, category × hour-of-day heatmap
4.Flags anomalies — z-score-based outlier detection (>2σ) per category to surface unusually large transactions
5.Profiles spending archetypes — applies 11 quantitative rules (Foodie, Shopaholic, Investor, Late-Night Snacker, YOLO Spender, Movie Geek, Kanjoos, Thrifty, and more) to label the spender's persona
Data Notes:
1.Bank CSVs mix date formats (2024-01-01, 01-Jan-24, 01/01/24) — parsed explicitly, not with format="mixed" alone, to avoid    silent misparses (e.g. 30/06/24 → 2024-01-01 in some pandas versions)
2.Amounts contain ₹, Rs., commas — cleaned via regex before pd.to_numeric
3.Some balance values are corrupted (negative running totals) — excluded from analysis

