import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Number of rows
num_rows = 100000

# Year range
years = list(range(2014, 2026))
time_period_map = {year: "Past" if year < 2019 else "Present" for year in years}

# Regions & Districts
regions = ["Jammu", "Kashmir", "Ladakh"]
districts = {
    "Jammu": ["Doda", "Jammu", "Kathua", "Kishtwar", "Poonch",
              "Rajouri", "Reasi", "Ramban", "Samba", "Udhampur"],
    "Kashmir": ["Anantnag", "Bandipora", "Baramulla", "Budgam", "Ganderbal",
                "Kulgam", "Kupwara", "Pulwama", "Shopian", "Srinagar"],
    "Ladakh": ["Leh", "Kargil", "Drass", "Zanskar", "Nubra", "Sankoo", "Turtuk"]
}

# Crop preferences by region
region_crops = {
    "Jammu": ["Rice", "Wheat", "Maize"],
    "Kashmir": ["Rice", "Apple", "Saffron", "Walnut"],
    "Ladakh": ["Wheat", "Barley", "Apple"]
}

# Function to determine season & rainfall based on month and region
def get_season_and_rainfall(date_value, region):
    month = date_value.month
    if region == "Ladakh":
        # Less rainfall in Ladakh
        rainfall = round(random.uniform(50, 200), 1)
    else:
        if 6 <= month <= 10:
            rainfall = round(random.uniform(600, 1200), 1)  # Monsoon
        elif 11 <= month or month <= 4:
            rainfall = round(random.uniform(200, 600), 1)   # Winter
        else:
            rainfall = round(random.uniform(50, 250), 1)    # Summer
    season = "Kharif" if 6 <= month <= 10 else "Rabi" if (11 <= month or month <= 4) else "Zaid"
    return season, rainfall

data = []

for i in range(1, num_rows + 1):
    year = random.choice(years)
    region = random.choice(regions)
    district = random.choice(districts[region])
    crop = random.choice(region_crops[region])
    
    # Random date in the selected year
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31)
    random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    
    season, rainfall = get_season_and_rainfall(random_date, region)

    # Bias values by region
    if region == "Jammu":
        cultivated_area = round(np.random.uniform(500, 7000), 2)
    elif region == "Kashmir":
        cultivated_area = round(np.random.uniform(300, 5000), 2)
    else:  # Ladakh
        cultivated_area = round(np.random.uniform(50, 1500), 2)

    production = round(cultivated_area * np.random.uniform(0.6, 2.0), 2)
    export_tons = round(production * np.random.uniform(0.1, 0.7), 2)

    # Revenue: Kashmir’s saffron/walnuts more valuable
    if crop in ["Saffron", "Walnut", "Apple"]:
        revenue = round(export_tons * np.random.uniform(0.5, 2.0), 2)
    else:
        revenue = round(export_tons * np.random.uniform(0.1, 0.8), 2)

    water_usage = round(cultivated_area * np.random.uniform(0.3, 1.5), 2)
    fertilizer_usage = round(cultivated_area * np.random.uniform(0.05, 0.25), 2)

    data.append([
        i, year, random_date.date(), time_period_map[year], region, district, crop,
        season, cultivated_area, production, export_tons, revenue,
        rainfall, water_usage, fertilizer_usage
    ])

# Create DataFrame
columns = [
    "Record_ID", "Year", "Date", "Time_Period", "Region", "District", "Crop_Type",
    "Season", "Cultivated_Area_HA", "Production_MT", "Export_Tons", "Revenue_Cr",
    "Rainfall_mm", "Water_Usage_ML", "Fertilizer_Usage_Tons"
]
df = pd.DataFrame(data, columns=columns)

# Save to CSV
df.to_csv("agriculture.csv", index=False)
print("✅ Improved dataset generated: agriculture.csv")
