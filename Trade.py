import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# ----------------------------
# Settings
# ----------------------------
random.seed(42)
np.random.seed(42)

NUM_ROWS = 100000
YEARS = list(range(2014, 2026))  # 2014–2025

# Time period logic
def get_time_period(year):
    return "Past" if year < 2025 else "Present"

# Regions & Districts
regions_districts = {
    "Jammu": ["Doda", "Jammu", "Kathua", "Kishtwar", "Poonch",
              "Rajouri", "Reasi", "Ramban", "Samba", "Udhampur"],
    "Kashmir": ["Anantnag", "Bandipora", "Baramulla", "Budgam", "Ganderbal",
                "Kulgam", "Kupwara", "Pulwama", "Shopian", "Srinagar"],
    "Ladakh": ["Leh", "Kargil", "Drass", "Zanskar", "Nubra", "Sankoo", "Turtuk"]
}

# Market types & commodities
market_types = ["Wholesale", "Retail", "Export Hub"]
commodities = ["Saffron", "Handicrafts", "Dry Fruits", "Wool", "Tea", "Spices", "Carpets", "Metalware", "Flowers"]

# Random date in a given year
def random_date_in_year(year):
    start = datetime(year, 1, 1)
    end = datetime(year, 12, 31)
    return (start + timedelta(days=random.randint(0, (end - start).days))).date()

# ----------------------------
# Generate Dataset
# ----------------------------
rows = []
for i in range(1, NUM_ROWS + 1):
    year = random.choice(YEARS)
    date_val = random_date_in_year(year)
    time_period = get_time_period(year)
    region = random.choice(list(regions_districts.keys()))
    district = random.choice(regions_districts[region])
    market_type = random.choice(market_types)
    commodity = random.choice(commodities)

    # Region bias in trade volume
    if region == "Jammu":
        base_trade = np.random.uniform(500, 4000)
    elif region == "Kashmir":
        base_trade = np.random.uniform(1000, 5000)
    else:  # Ladakh
        base_trade = np.random.uniform(100, 1500)

    # Commodity boosts (e.g., Saffron & Handicrafts are high value)
    commodity_multiplier = {
        "Saffron": 1.5,
        "Handicrafts": 1.3,
        "Carpets": 1.2,
        "Dry Fruits": 1.1,
        "Wool": 1.0,
        "Tea": 0.9,
        "Spices": 1.0,
        "Metalware": 0.8,
        "Flowers": 0.7
    }[commodity]

    # Year trend → gradual increase in trade volume
    year_factor = 1 + (year - 2014) * 0.03  # ~3% growth per year

    trade_volume = round(base_trade * commodity_multiplier * year_factor, 2)

    export_value = round(trade_volume * np.random.uniform(0.3, 0.8), 2)
    import_value = round(trade_volume * np.random.uniform(0.1, 0.5), 2)

    # Employment scales with market type
    if market_type == "Wholesale":
        employment = random.randint(500, 15000)
    elif market_type == "Export Hub":
        employment = random.randint(1000, 20000)
    else:  # Retail
        employment = random.randint(100, 5000)

    gst_collection = round(trade_volume * np.random.uniform(0.05, 0.18), 2)

    rows.append({
        "Record_ID": i,
        "Year": year,
        "Date": date_val.isoformat(),
        "Time_Period": time_period,
        "Region": region,
        "District": district,
        "Market_Type": market_type,
        "Trade_Volume_Cr": trade_volume,
        "Export_Value_Cr": export_value,
        "Import_Value_Cr": import_value,
        "Major_Commodity": commodity,
        "Employment_in_Trade": employment,
        "GST_Collection_Cr": gst_collection
    })

# ----------------------------
# Save to CSV
# ----------------------------
df = pd.DataFrame(rows)
df.to_csv("trade_commerce.csv", index=False)
print("✅ trade_commerce.csv generated with", len(df), "rows and", len(df.columns), "columns.")
