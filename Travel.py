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

# Tourist types & destination types
tourist_types = ["Domestic", "International"]
destination_types = ["Hill Station", "Heritage", "Wildlife", "Pilgrimage", "Adventure"]

# ----------------------------
# Helper Functions
# ----------------------------
def month_to_season(month):
    if month in (4, 5, 6): return "Summer"
    if month in (7, 8, 9): return "Monsoon"
    if month in (10, 11): return "Autumn"
    if month in (12, 1, 2): return "Winter"
    if month == 3: return "Spring"
    return "Unknown"

def random_date_in_year(year):
    start, end = datetime(year, 1, 1), datetime(year, 12, 31)
    return (start + timedelta(days=random.randint(0, (end - start).days))).date()

def is_festival_season(season, destination_type):
    base_prob = 0.08
    if season in ("Summer", "Winter"): base_prob += 0.12
    if destination_type == "Pilgrimage": base_prob += 0.10
    return random.random() < min(base_prob, 0.9)

def generate_footfall(region, destination_type, year):
    # Base ranges
    if destination_type == "Pilgrimage": low, high = 5000, 500000
    elif destination_type == "Hill Station": low, high = 2000, 300000
    elif destination_type == "Adventure": low, high = 1000, 100000
    elif destination_type == "Wildlife": low, high = 500, 80000
    else: low, high = 1000, 150000  # Heritage

    # Regional adjustments
    if region == "Ladakh":
        low, high = int(low * 0.3), int(high * 0.5)
        if destination_type == "Adventure":
            low, high = int(low * 2), int(high * 2)  # Ladakh = Adventure hub

    # Yearly growth (4% increase per year since 2014)
    growth_factor = 1 + (year - 2014) * 0.04
    return int(random.randint(low, high) * growth_factor)

def estimate_revenue_crore(footfall, avg_stay_days, tourist_type, festival):
    per_tourist = random.uniform(0.02, 0.08) if tourist_type == "International" else random.uniform(0.002, 0.02)
    revenue = footfall * per_tourist * (avg_stay_days / 3.0)
    revenue *= random.uniform(0.85, 1.25)
    if festival == "Yes":
        revenue *= 1.2  # festival boost
    return round(max(0.01, revenue), 2)

def estimate_hotels(footfall):
    base = int(max(10, min(2000, footfall // 250)))
    return max(1, int(random.gauss(base, base * 0.25)))

def estimate_employment(hotels_registered, footfall):
    direct = hotels_registered * random.randint(5, 25)
    indirect = int(footfall * random.uniform(0.0005, 0.005))
    return max(10, direct + indirect)

def generate_avg_stay(destination_type, tourist_type):
    base = random.uniform(4, 8) if tourist_type == "International" else random.uniform(1, 6)
    if destination_type == "Adventure": base *= 0.9
    if destination_type == "Pilgrimage": base *= 1.1
    return round(max(1.0, min(10.0, random.gauss(base, 1.2))), 1)

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

    # Tourist type (80% Domestic, 20% International; Ladakh gets more foreign visitors)
    if region == "Ladakh":
        tourist_type = np.random.choice(tourist_types, p=[0.6, 0.4])
    else:
        tourist_type = np.random.choice(tourist_types, p=[0.8, 0.2])

    destination_type = random.choice(destination_types)
    season = month_to_season(date_val.month)

    tourist_footfall = generate_footfall(region, destination_type, year)
    avg_stay_days = generate_avg_stay(destination_type, tourist_type)
    festival_season = "Yes" if is_festival_season(season, destination_type) else "No"
    revenue_cr = estimate_revenue_crore(tourist_footfall, avg_stay_days, tourist_type, festival_season)
    hotels_registered = estimate_hotels(tourist_footfall)
    employment_generated = estimate_employment(hotels_registered, tourist_footfall)

    rows.append({
        "Record_ID": i,
        "Year": year,
        "Date": date_val.isoformat(),
        "Time_Period": time_period,
        "Region": region,
        "District": district,
        "Tourist_Type": tourist_type,
        "Destination_Type": destination_type,
        "Season": season,
        "Tourist_Footfall": tourist_footfall,
        "Average_Stay_Days": avg_stay_days,
        "Festival_Season": festival_season,
        "Revenue_Cr": revenue_cr,
        "Hotels_Registered": hotels_registered,
        "Employment_Generated": employment_generated
    })

# ----------------------------
# Save to CSV
# ----------------------------
df = pd.DataFrame(rows)
df.to_csv("travel.csv", index=False)
print("✅ travel.csv generated with", len(df), "rows and", len(df.columns), "columns.")
