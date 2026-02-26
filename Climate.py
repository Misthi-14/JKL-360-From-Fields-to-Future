import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ----------------------------
# Settings
# ----------------------------
random.seed(42)
np.random.seed(42)

NUM_ROWS = 100000
YEARS = list(range(2014, 2026))  # longer range for climate trends

# Regions & Districts
regions_districts = {
    "Jammu": ["Doda", "Jammu", "Kathua", "Kishtwar", "Poonch",
              "Rajouri", "Reasi", "Ramban", "Samba", "Udhampur"],
    "Kashmir": ["Anantnag", "Bandipora", "Baramulla", "Budgam", "Ganderbal",
                "Kulgam", "Kupwara", "Pulwama", "Shopian", "Srinagar"],
    "Ladakh": ["Leh", "Kargil", "Drass", "Zanskar", "Nubra", "Sankoo", "Turtuk"]
}

# Generate random date within a year
def random_date_in_year(year):
    start = datetime(year, 1, 1)
    end = datetime(year, 12, 31)
    return (start + timedelta(days=random.randint(0, (end - start).days))).date()

# Seasonal mapping
def month_to_season(month):
    if month in (4, 5, 6):
        return "Summer"
    if month in (7, 8, 9):
        return "Monsoon"
    if month in (10, 11):
        return "Autumn"
    if month in (12, 1, 2):
        return "Winter"
    if month == 3:
        return "Spring"
    return "Unknown"

# Generate climate metrics
def generate_temperature(region, year, month):
    warming_trend = (year - 2014) * 0.1  # +0.1°C per year
    if region == "Jammu":
        base = random.uniform(15, 38)
    elif region == "Kashmir":
        base = random.uniform(-6, 30)
    else:  # Ladakh
        base = random.uniform(-25, 22)
    return round(base + warming_trend, 1)

def generate_rainfall(region, month):
    if region == "Jammu":
        return round(random.uniform(150, 600), 1) if month in [7, 8, 9] else round(random.uniform(10, 200), 1)
    elif region == "Kashmir":
        return round(random.uniform(80, 400), 1) if month in [7, 8, 9] else round(random.uniform(10, 150), 1)
    else:  # Ladakh
        return round(random.uniform(0, 60), 1)

def generate_snowfall(region, month):
    if region == "Jammu":
        return round(random.uniform(0, 10), 1) if month in [12, 1, 2] else 0.0
    elif region == "Kashmir":
        return round(random.uniform(20, 150), 1) if month in [12, 1, 2] else round(random.uniform(0, 20), 1)
    else:  # Ladakh
        return round(random.uniform(50, 300), 1) if month in [11, 12, 1, 2, 3] else round(random.uniform(0, 30), 1)

def generate_humidity(region):
    if region == "Jammu":
        return round(random.uniform(40, 95), 1)
    elif region == "Kashmir":
        return round(random.uniform(50, 90), 1)
    else:  # Ladakh
        return round(random.uniform(20, 50), 1)

def generate_aqi(region):
    if region == "Jammu":
        return random.randint(70, 250)
    elif region == "Kashmir":
        return random.randint(40, 160)
    else:  # Ladakh
        return random.randint(10, 90)

def extreme_weather(region, season):
    base_prob = 0.05
    if season == "Monsoon" and region == "Jammu":
        base_prob += 0.20  # floods
    if season == "Winter" and region in ["Kashmir", "Ladakh"]:
        base_prob += 0.25  # blizzards
    return "Yes" if random.random() < base_prob else "No"

# ----------------------------
# Generate Dataset
# ----------------------------
rows = []
for i in range(1, NUM_ROWS + 1):
    year = random.choice(YEARS)
    date_val = random_date_in_year(year)
    month = date_val.month
    season = month_to_season(month)
    region = random.choice(list(regions_districts.keys()))
    district = random.choice(regions_districts[region])

    avg_temp = generate_temperature(region, year, month)
    rainfall = generate_rainfall(region, month)
    snowfall = generate_snowfall(region, month)
    humidity = generate_humidity(region)
    aqi = generate_aqi(region)
    extreme = extreme_weather(region, season)

    rows.append({
        "Record_ID": i,
        "Year": year,
        "Date": date_val.isoformat(),
        "Region": region,
        "District": district,
        "Season": season,
        "Average_Temperature_C": avg_temp,
        "Rainfall_mm": rainfall,
        "Snowfall_mm": snowfall,
        "Humidity_Percent": humidity,
        "Air_Quality_Index": aqi,
        "Extreme_Weather": extreme
    })

# ----------------------------
# Save to CSV
# ----------------------------
df = pd.DataFrame(rows, columns=[
    "Record_ID", "Year", "Date", "Region", "District", "Season",
    "Average_Temperature_C", "Rainfall_mm", "Snowfall_mm",
    "Humidity_Percent", "Air_Quality_Index", "Extreme_Weather"
])

df.to_csv("climate.csv", index=False)
print("✅ Improved climate.csv generated with", len(df), "rows and", len(df.columns), "columns.")
