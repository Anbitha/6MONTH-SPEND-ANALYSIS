import pandas as pd
pd.set_option("display.width", 1000)  # Show all columns when printing

# 1. Read the CSV
df = pd.read_csv("DADS MP2 Dataset.csv")


# 2. Parse the four date formats using errors='coerce'
#    Formats seen: 2024-01-01, 01-Jan-24, 01/01/24, 01 Jan 2024

def parse_date(s):
    s = str(s).strip()
    for fmt in ("%Y-%m-%d", "%d-%b-%y", "%d/%m/%y", "%d %b %Y", "%d/%m/%Y"):
        try:
            return pd.to_datetime(s, format=fmt)
        except ValueError:
            pass
    return pd.NaT

df['Date'] = df['Date'].apply(parse_date)


# 3. Parse the three amount formats (â¹2462, 50.00, Rs. 625)
#    Strip currency symbols and commas, then convert to numeric
df["Amount"] = (
    df["Amount"]
    .astype(str)
    .str.replace('₹', "").str.replace('Rs.', "", regex=False).str.replace(',', "").str.strip()# remove rupee symbol, Rs., commas, spaces
    .pipe(pd.to_numeric, errors="coerce")
)

# 4. Standardise the Type field (Debit/DR -> Debit, Credit/CR -> Credit)
df["Type"] = df["Type"].str.upper().str.strip()
df["Type"] = df["Type"].replace({"DR": "DEBIT", "CR": "CREDIT"})

# 5. Drop duplicates (full rows, and also by Ref which should be unique)
df = df.drop_duplicates()


# 6. Clean up remaining columns
df["Mode"] = df["Mode"].str.upper().str.strip()
df["Ref"] = df["Ref"].str.strip()
df["Description"] = df["Description"].astype(str).str.strip()

# Drop rows where the date failed to parse (errors='coerce' creates NaT)
df = df.dropna(subset=["Date", "Amount"])

# Sort by date and time for a clean chronological view
df = df.sort_values(["Date", "Time"]).reset_index(drop=True)



# --- Derive the stats from your data ---
name = "RAHUL SHARMA"
n_months = df['Date'].dt.to_period('M').nunique()
n_transactions = len(df)
start = df['Date'].min().strftime('%b %Y')
end = df['Date'].max().strftime('%b %Y')

# --- Print the header ---
print("=" * 80)
print("SpendDNA REPORT - " + name)
print(f"{n_months} months - {n_transactions:,} transactions - {start} to {end}")
print("=" * 80)

vendor_dict = {
    'Swiggy':     ['SWIGGY', 'BUNDL','GROFERS','INSTAMART'],                    # BUNDL = Swiggy's parent/Instamart
    'Zomato':      ['ZOMATO', 'DINING'],                   # ZOMATO-DINING, ZOMATO MEDIA
    'Amazon':      ['AMAZON', 'AMZN',],
    'Prime':['PRIME'],                     # AMAZON SELLER, AMZN-INTPYMT, AMZN PRIME
    'Blinkit':     ['BLINKIT'],               # BLINKIT BANGALORE, SWIGGY-INSTAMART
    'Zepto':       ['ZEPTO','KIRANAKART'],
    'BigBasket':   ['BIGBASKET','INNOVATIVE'],
    'DMart':       ['DMART','AVENUE'],
    'Flipkart':    ['FLIPKART', 'FKART'],
    'Myntra':      ['MYNTRA'],                      # FSN E-COMMERCE = Myntra
    'Nykaa':       ['NYKAA','FSN'],
    'Uber':        ['UBER', 'Uber*'],
    'Ola':         ['OLA','ANI'],
    'Rapido':      ['RAPIDO','ROPPEN'],
    'BMTC':        ['BMTC', 'TUMMOC','TRANSPORTATION'],                     # TUMMOC = BMTC ticketing
    'Starbucks':   ['STARBUCKS','COFFEE'],
    'Cafe Coffee Day': ['CCD', 'COFFEE DAY'],
    'Truffles':    ['TRUFFLES'],
    'Restaurants': ['RESTAURANT','DINEOUT'],                  # UPI-RESTAURANT-xxxx
    'Zerodha':     ['ZERODHA'], 
       'Groww':['GROWW','NEXTBILLION'],   # investments
    'Netflix':     ['NETFLIX'],
    'Disney+ Hotstar': ['HOTSTAR', 'STAR INDIA'],  # streaming
    'Spotify':     ['SPOTIFY'],
    'Airtel':      ['AIRTEL', 'BHARTI'],
    'Jio':         ['JIO', 'RELIANCE'],
    'Vodafone Idea': ['VODAFONE', 'VI-RECHARGE', 'VI POSTPAID'],
    'Rent':        ['RENT-LANDLORD'],
    'Electricity': ['BESCOM', 'BANGALORE ELEC','TWC'],  # BESCOM + water (BWSSB)
    'BookMyShow':  ['BOOKMYSHOW', 'BMS ','BIGTREE','MOVIE'],                 # BMS MOVIE TICKETS
    'ATM Withdrawal': ['ATM-WDL'],
    'Petrol':      ['PETROL', 'IOC', 'BPCL', 'INDIAN OIL', 'HP PETROL'],
    'Salary':      ['SALARY', 'TECHCRUSH'],
    'Thirdwave':['THIRDWAVE'],
    'P2P':['AMAN-', 'PRIYA-', 'ANKIT-', 'NEHA-', 'VIKAS-', 'KARAN-', 'SNEHA-'],
    'WATER':['BWSSB','WATER'],
    'Meghana':['MEGHANA'],
}

def extract_vendor(description):
    """Return the canonical vendor name for a description, or 'Other'."""
    text = str(description).upper()
    for vendor, keywords in vendor_dict.items():
        for kw in keywords:
            if kw.upper() in text:
                return vendor
    return 'Other'

# Apply to the DataFrame
df['vendor_clean'] = df['Description'].apply(extract_vendor)

#category 

# Map each vendor to one of the 12 categories
category_map = {
    'Swiggy':          'Food Delivery',
    'Zomato':          'Food Delivery',
    'Amazon':          'Ecommerce',
    'Zepto':           'Quick Commerce',
    'Uber':            'Cab',
    'Starbucks':       'Cafe',
    'Ola':             'Cab',
    'Rapido':          'Cab',
    'Restaurants':     'Restaurants',
    'Flipkart':        'Ecommerce',
    'Blinkit':         'Quick Commerce',
    'BMTC':            'Transport',
    'Petrol':          'Fuel',
    'Electricity':     'Utilities',
    'DMart':           'Groceries',
    'Myntra':          'Ecommerce',
    'Nykaa':           'Ecommerce',
    'BigBasket':       'Quick Commerce',
    'P2P':             'Personal Transfer',
    'ATM Withdrawal':  'Cash Withdrawal',
    'Zerodha':         'Investments',
    'BookMyShow':      'Entertainment',
    'Disney+ Hotstar': 'Entertainment',
    'Meghana':         'Restaurants',
    'Thirdwave':       'Cafe',
    'Netflix':         'Subscriptions',
    'Groww':           'Investments',
    'Truffles':        'Restaurants',
    'Cafe Coffee Day': 'Cafe',
    'WATER':           'Utilities',
    'Vodafone Idea':   'Subscriptions',
    'Spotify':         'Subscriptions',
    'Salary':          'Salary',
    'Rent':            'Rent',
    'Jio':             'Subscriptions',
    'Airtel':          'Subscriptions',
    'Prime':           'Entertainment'
}

# Map to a new column; .map() leaves unknown vendors as NaN
df['category'] = df['vendor_clean'].map(category_map)

# Handle NaN for uncategorised entries
df['category'] = df['category'].fillna('Uncategorised')


# --- 1. Total credits and debits ---
total_credits = df.loc[df['Type'] == 'CREDIT', 'Amount'].sum()
total_debits  = df.loc[df['Type'] == 'DEBIT', 'Amount'].sum()

# --- 2. Net savings (credits - debits) ---
net_savings = total_credits - total_debits

# --- 3. Savings rate (as a percentage of income) ---
savings_rate = (net_savings / total_credits) * 100

# --- 4. Top 5 categories by spend (debits only) ---
top_categories = (
    df.loc[df['Type'] == 'DEBIT']
    .groupby('category')['Amount']
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

# --- 5. Top 5 vendors by spend (debits only) ---
top_vendors = (
    df.loc[df['Type'] == 'DEBIT']
    .groupby('vendor_clean')['Amount']
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

# --- 6. Total transaction count ---
total_transactions = len(df)

# --- Print with f-string formatting ---
print("=" * 45)
print("EXECUTIVE SUMMARY")
print("=" * 45)
print(f"Total Credits      : ₹{total_credits:,.2f}")
print(f"Total Debits       : ₹{total_debits:,.2f}")
print(f"Net Savings        : ₹{net_savings:,.2f}")
print(f"Savings Rate       : {savings_rate:.2f}%")
print(f"Total Transactions : {total_transactions}")

print("\n--- Top 5 Categories by Spend ---")
for cat, amt in top_categories.items():
    print(f"  {cat:<18} ₹{amt:>12,.2f}")

print("\n--- Top 5 Vendors by Spend ---")
for vendor, amt in top_vendors.items():
    print(f"  {vendor:<18} ₹{amt:>12,.2f}")

# Monthly Trend Analysis
import numpy as np

# --- 1. Add a month column (1 = Jan ... 6 = Jun) ---
df['month'] = df['Date'].dt.month

# --- 2. Build the pivot: rows = category, columns = month, values = total spent ---
# Only debits count as spend
spend = df.loc[df['Type'] == 'DEBIT']

month_pivot = spend.pivot_table(
    values='Amount',
    index='category',
    columns='month',
    aggfunc='sum'
)

# Ensure all 6 months exist as columns (fill missing with 0)
month_pivot = month_pivot.reindex(columns=[1, 2, 3, 4, 5, 6], fill_value=0)

print("MONTHLY SPEND:")
print(month_pivot)

# --- 3. Month-over-month % change using NumPy ---
# Growth = (last_month - first_month) / first_month * 100
first = month_pivot[month_pivot.columns[0]].to_numpy()
last  = month_pivot[month_pivot.columns[-1]].to_numpy()

with np.errstate(divide='ignore', invalid='ignore'):
    growth = np.where(first != 0, ((last - first) / first) * 100, np.nan)

growth_series = pd.Series(growth, index=month_pivot.index)

#print("\nOverall growth (last vs first month, %):")
#print(growth_series.round(2))

# --- 4. Biggest growth and biggest decline ---
biggest_growth  = growth_series.idxmax()
biggest_decline = growth_series.idxmin()

print(f"\nBiggest month-on-month growth : {biggest_growth}  ({growth_series[biggest_growth]:.1f}%)")
print(f"Biggest month-on-month decline: {biggest_decline}  ({growth_series[biggest_decline]:.1f}%)")

#time of day analysis

# --- 1. Extract hour from Time (HH:MM) ---
df['hour'] = df['Time'].str[:2].astype(int)

# --- 2. Restrict to spend (debits) ---
spend = df.loc[df['Type'] == 'DEBIT']

# --- 3. Build category × hour matrix with NumPy ---
categories = spend['category'].dropna().unique()
categories = sorted(categories)

# 2D array: rows = categories, cols = 24 hours
heatmap = np.zeros((len(categories), 24), dtype=float)

# Fill using groupby counts
counts = spend.groupby(['category', 'hour']).size()
for (cat, hr), val in counts.items():
    row = list(categories).index(cat)
    heatmap[row, hr] = val

heatmap_df = pd.DataFrame(heatmap, index=categories, columns=range(24))



# --- 5. Surface time-of-day insights ---
def hour_share(category, start, end):
    """% of a category's transactions falling in [start, end) hours."""
    total = counts.get((category, slice(None)), 0)
    mask = heatmap_df.loc[category, start:end-1].sum()
    return mask / heatmap_df.loc[category].sum() * 100

print("\n--- Time-of-day insights ---")

# Swiggy: 9 PM - 1 AM (21:00 to 01:00)
swiggy_total = heatmap_df.loc['Food Delivery'].sum()
swiggy_late  = heatmap_df.loc['Food Delivery', 21:24].sum() + heatmap_df.loc['Food Delivery', 0:1].sum()
print(f"Food Delivery (incl. Swiggy) between 9 PM-1 AM: {swiggy_late/swiggy_total*100:.1f}%")

# Cafe: 8-11 AM
cafe_total = heatmap_df.loc['Cafe'].sum()
cafe_morning = heatmap_df.loc['Cafe', 8:11].sum()
print(f"Cafe spending between 8-11 AM: {cafe_morning/cafe_total*100:.1f}%")

# --- 6. Peak hour for each category (printable bar) ---
#print("\n--- Peak hour per category ---")
for cat in categories:
    peak = heatmap_df.loc[cat].idxmax()
    val  = int(heatmap_df.loc[cat].max())
    bar = '#' * min(val, 40)
    #print(f"{cat:<18} hour {peak:>2}:00  {bar} ({val})")

#Anamolies


# --- 1. Compute category mean and std, then z-score ---
category_mean = df.groupby('category')['Amount'].transform('mean')
category_std  = df.groupby('category')['Amount'].transform('std')

df['z_score'] = (df['Amount'] - category_mean) / category_std

# --- 2. Flag anomalies: z_score > 2 ---
anomalies = df[df['z_score'] > 2]

# ---  . Sort by z_score descending and take top 5 ---
top_anomalies = anomalies.sort_values('z_score', ascending=False).head(5)

# ---  . Print with date, vendor, category, amount, z_score ---
print("\nTop 5 Anomalous Transactions (z-score > 2):")
print(top_anomalies[['Date', 'vendor_clean', 'category', 'Amount','z_score']].to_string(index=False))

#Archetype analysis

# --- 1. Compute the base metrics ---
total_debits = df.loc[df['Type'] == 'DEBIT', 'Amount'].sum()
total_credits = df.loc[df['Type'] == 'CREDIT', 'Amount'].sum()

# Category share of debits
cat_spend = df.loc[df['Type'] == 'DEBIT'].groupby('category')['Amount'].sum()
cat_share = cat_spend / total_credits * 100

# Savings rate
savings_rate = (total_credits - total_debits) / total_credits * 100

# Food Delivery late-night share (21:00 - 02:00)
fd = df.loc[(df['Type'] == 'DEBIT') & (df['category'] == 'Food Delivery')]
fd_late = fd['hour'].between(21, 23).sum() + fd['hour'].between(0,  2).sum()
fd_late_share = fd_late / len(fd) * 100 if len(fd) > 0 else 0

# Distinct subscription vendors
sub_vendors = df.loc[(df['Type'] == 'DEBIT') & (df['category'] == 'Subscriptions'), 'vendor_clean'].nunique()

# Monthly spend (for thrifty rule)
df['month'] = df['Date'].dt.month
monthly_spend = df.loc[df['Type'] == 'DEBIT'].groupby('month')['Amount'].sum()
avg_monthly_spend = monthly_spend.mean()

# Entertainment share (for movie geek)
ent_share = cat_spend.get('Entertainment', 0) / total_debits * 100

# Avg utilities bill (for kanjoos)
avg_utilities = df.loc[(df['Type'] == 'DEBIT') & (df['category'] == 'Utilities'), 'Amount'].mean()

# --- 2. Apply all rules ---
archetypes = []

# THE FOODIE
if cat_share.get('Food Delivery', 0) + cat_share.get('Restaurants', 0) + cat_share.get('Cafe', 0) > 25:
    archetypes.append('THE FOODIE')

# THE QUICK COMMERCE JUNKIE
if cat_share.get('Quick Commerce', 0) > 15:
    archetypes.append('THE QUICK COMMERCE JUNKIE')

# THE SHOPAHOLIC
if cat_share.get('Ecommerce', 0) > 15:
    archetypes.append('THE SHOPAHOLIC')

# THE INVESTOR
if cat_share.get('Investments', 0) > 15:
    archetypes.append('THE INVESTOR')

# THE LATE-NIGHT SNACKER
if fd_late_share > 50:
    archetypes.append('THE LATE-NIGHT SNACKER')

# THE CAB COMMUTER
if cat_share.get('Cab', 0) > 10:
    archetypes.append('THE CAB COMMUTER')

# THE SUBSCRIPTION LOVER
if sub_vendors >= 5:
    archetypes.append('THE SUBSCRIPTION LOVER')

# THE YOLO SPENDER
if savings_rate < 10:
    archetypes.append('THE YOLO SPENDER')

# THE DISCIPLINED SAVER
if savings_rate >  40:
    archetypes.append('THE DISCIPLINED SAVER')

# --- 3. Custom archetypes ---

# MOVIE GEEK: entertainment >  25% of debits
if ent_share >  25:
    archetypes.append('MOVIE GEEK')

# KANJOOS: avg utilities bill < ₹1000
if avg_utilities < 1000:
    archetypes.append('KANJOOS')

# THRIFTY: avg monthly spend < monthly salary
salary = df.loc[df['Type'] == 'CREDIT', 'Amount'].sum()/6
if avg_monthly_spend < salary:
    archetypes.append('THRIFTY')

# --- 4. Print results ---
print("=" * 45)
print("RAHUL'S SPEND PERSONA — ARCHETYPE MATCH")
print("=" * 45)
print(f"Savings rate          : {savings_rate:.1f}%")
print(f"Food+Rest+Cafe share  : {cat_share.get('Food Delivery',0)+cat_share.get('Restaurants',0)+cat_share.get('Cafe',0):.1f}%")
print(f"Quick Commerce share   : {cat_share.get('Quick Commerce',0):.1f}%")
print(f"Ecommerce share        : {cat_share.get('Ecommerce',0):.1f}%")
print(f"Investments share       : {cat_share.get('Investments',0):.1f}%")
print(f"Late-night food share   : {fd_late_share:.1f}%")
print(f"Distinct sub vendors     : {sub_vendors}")
print(f"Entertainment share      : {ent_share:.1f}%")
print(f"Avg utilities bill        : ₹{avg_utilities:,.2f}")
print(f"Avg monthly spend        : ₹{avg_monthly_spend:,.2f}")

print("\nMatched archetypes:")
for a in archetypes:

    print(f"  ✔ {a}")







