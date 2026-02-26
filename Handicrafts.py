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

# Time period logic: 2025 included in Present
def get_time_period(year):
    if year < 2025:
        return "Past"
    else:
        return "Present"

# Regions & Districts
regions_districts = {
    "Jammu": ["Doda", "Jammu", "Kathua", "Kishtwar", "Poonch",
              "Rajouri", "Reasi", "Ramban", "Samba", "Udhampur"],
    "Kashmir": ["Anantnag", "Bandipora", "Baramulla", "Budgam", "Ganderbal",
                "Kulgam", "Kupwara", "Pulwama", "Shopian", "Srinagar"],
    "Ladakh": ["Leh", "Kargil", "Drass", "Zanskar", "Nubra", "Sankoo", "Turtuk"]
}

industry_types = ["Handicrafts", "Textile", "Food Processing", "Mining", "Tourism Support", "Small Scale"]
handicraft_items = ["Carpets", "Shawls", "Woodwork", "Papier-mâché", "Metalware", "Pashmina"]

# Generate random date within a year
def random_date_in_year(year):
    start = datetime(year, 1, 1)
    end = datetime(year, 12, 31)
    delta_days = (end - start).days
    return (start + timedelta(days=random.randint(0, delta_days))).date()

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
    industry_type = random.choice(industry_types)

    # Units registered differ by region
    if region == "Jammu":
        units_registered = random.randint(50, 1200)
    elif region == "Kashmir":
        units_registered = random.randint(100, 1500)
    else:  # Ladakh
        units_registered = random.randint(5, 400)

    # Handicrafts more common in Kashmir
    if industry_type == "Handicrafts" and region == "Kashmir":
        handicraft_item = random.choice(handicraft_items)
    elif industry_type == "Handicrafts":
        handicraft_item = random.choice(handicraft_items + ["None"])  # Some non-handicraft areas
    else:
        handicraft_item = "None"

    # Production & export values scale with units
    production_value = round(units_registered * np.random.uniform(1.0, 10.0), 2)  # crores
    export_value = round(production_value * np.random.uniform(0.3, 0.9), 2)

    # Employment scales with industry size
    employment_generated = int(units_registered * np.random.uniform(5, 20))

    govt_schemes = random.choice(["Yes", "No"])

    rows.append({
        "Record_ID": i,
        "Year": year,
        "Date": date_val.isoformat(),
        "Time_Period": time_period,
        "Region": region,
        "District": district,
        "Industry_Type": industry_type,
        "Handicraft_Item": handicraft_item,
        "Units_Registered": units_registered,
        "Production_Value_Cr": production_value,
        "Export_Value_Cr": export_value,
        "Employment_Generated": employment_generated,
        "Govt_Schemes_Available": govt_schemes
    })

# ----------------------------
# Save to CSV
# ----------------------------
df = pd.DataFrame(rows, columns=[
    "Record_ID", "Year", "Date", "Time_Period", "Region", "District",
    "Industry_Type", "Handicraft_Item", "Units_Registered",
    "Production_Value_Cr", "Export_Value_Cr", "Employment_Generated",
    "Govt_Schemes_Available"
])

df.to_csv("industry_handicrafts.csv", index=False)
print("✅ industry_handicrafts.csv generated with", len(df), "rows and", len(df.columns), "columns.")

