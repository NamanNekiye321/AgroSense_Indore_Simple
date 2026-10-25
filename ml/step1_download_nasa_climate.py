"""
================================================================================
FILE: step1_download_nasa_climate.py
PROJECT: AgroSense Indore (Simple Edition)
TEAM MEMBER: Kuldeep (Data Pipeline Lead)
================================================================================

PURPOSE:
    Downloads REAL climate data for Indore's 5 tehsils from NASA POWER API.
    NASA POWER (Prediction of Worldwide Energy Resources) is a free government
    satellite dataset providing daily weather measurements globally.

DATA SOURCE:
    - API:    https://power.larc.nasa.gov/api/temporal/daily/point
    - Portal: https://power.larc.nasa.gov/
    - Variables downloaded:
        T2M          = Temperature at 2 meters height (°C)
        RH2M         = Relative Humidity at 2 meters (%)
        PRECTOTCORR  = Corrected Precipitation (mm/day)
    - Date range: 2019-01-01 to 2023-12-31 (5 full agricultural years)
    - Community: AG (Agriculture)

WHY NASA POWER?
    - Free, no API key required
    - Global coverage (works for any lat/lon in Madhya Pradesh)
    - Trusted by agricultural researchers worldwide
    - ICAR and FAO both cite NASA POWER in their research

OUTPUT:
    data/climate_by_tehsil_season.csv
    (5-year seasonal averages per tehsil for Kharif and Rabi)

HOW TO RUN:
    python3 step1_download_nasa_climate.py
    (Takes 3-5 minutes due to API rate limits. Run once and commit the output.)

NOTE:
    If this script fails (e.g., no internet), the file data/climate_by_tehsil_season.csv
    already contains the pre-downloaded values. You do NOT need to re-run this
    every time. It is a one-time data collection step.
================================================================================
"""

import time
import os
import pandas as pd
import requests


# ============================================================
# STEP 1: DEFINE TEHSIL GPS COORDINATES
# Source: Google Maps / India Government Maps
# These are the central coordinates for each tehsil in Indore district
# ============================================================
TEHSILS = {
    "Indore":   {"lat": 22.7196, "lon": 75.8577},
    "Sanwer":   {"lat": 22.9781, "lon": 75.8239},
    "Depalpur": {"lat": 22.8483, "lon": 75.5492},
    "Mhow":     {"lat": 22.5539, "lon": 75.7644},
    "Hatod":    {"lat": 22.7969, "lon": 75.7289},
}


# ============================================================
# STEP 2: DEFINE AGRICULTURAL SEASONS
# Based on Indian Council of Agricultural Research (ICAR) standards
# and Madhya Pradesh Kisan Kalyan Department seasonal calendars
# ============================================================
def classify_season(month):
    """
    Returns the agricultural season for a given month number.
    - Kharif: Monsoon crop season (June to October) - major season in Malwa
    - Rabi:   Winter crop season (November to March) - 2nd major season
    - Zaid:   Summer crops (April-May) - minor season, very hot, less water
    """
    if month in [6, 7, 8, 9, 10]:
        return "Kharif"   # Rainy / Monsoon season
    elif month in [11, 12, 1, 2, 3]:
        return "Rabi"     # Winter crop season
    else:
        return "Zaid"     # Short summer season (April-May)


# ============================================================
# STEP 3: DOWNLOAD DATA FROM NASA POWER API
# We download 5 years (2019-2023) for each tehsil.
# The API returns daily data as JSON.
# We calculate seasonal averages from daily values.
# ============================================================
all_seasonal_records = []

print("=" * 60)
print("AgroSense Indore - NASA POWER Climate Downloader")
print("Downloading 5 years of daily climate data (2019-2023)...")
print("Source: https://power.larc.nasa.gov/")
print("=" * 60)

for tehsil_name, coords in TEHSILS.items():
    print(f"\n[{tehsil_name}] Fetching data (Lat: {coords['lat']}, Lon: {coords['lon']})...")

    # Build the NASA POWER API URL
    # Parameters: T2M (temperature), RH2M (humidity), PRECTOTCORR (rainfall)
    api_url = (
        f"https://power.larc.nasa.gov/api/temporal/daily/point?"
        f"parameters=T2M,RH2M,PRECTOTCORR"
        f"&community=AG"
        f"&longitude={coords['lon']}"
        f"&latitude={coords['lat']}"
        f"&start=20190101"
        f"&end=20231231"
        f"&format=JSON"
    )

    # Retry up to 3 times in case of network issues
    api_response = None
    for attempt in range(1, 4):
        try:
            response = requests.get(api_url, timeout=45)
            if response.status_code == 200:
                api_response = response.json()
                print(f"  ✅ Download successful on attempt {attempt}")
                break
            else:
                print(f"  ⚠️  Attempt {attempt} failed (HTTP {response.status_code}). Retrying in 3s...")
                time.sleep(3)
        except Exception as e:
            print(f"  ⚠️  Attempt {attempt} error: {e}. Retrying in 3s...")
            time.sleep(3)

    if not api_response:
        print(f"  ❌ Failed to download data for {tehsil_name}. Skipping.")
        continue

    # Parse the nested JSON structure from NASA POWER
    # Format: data["properties"]["parameter"]["T2M"]["20190101"] = value
    properties = api_response.get("properties", {}).get("parameter", {})
    temp_data  = properties.get("T2M",          {})
    humid_data = properties.get("RH2M",         {})
    rain_data  = properties.get("PRECTOTCORR",  {})

    # -------------------------------------------------------
    # STEP 4: PROCESS DAILY DATA → MONTHLY → SEASONAL AVERAGES
    # Using pandas for clean vectorized processing
    # -------------------------------------------------------
    # Build a daily DataFrame from the NASA JSON
    daily_records = []
    for date_str in temp_data:
        temp    = temp_data.get(date_str, -999)
        humid   = humid_data.get(date_str, -999)
        rain    = rain_data.get(date_str, -999)

        # NASA POWER uses -999 to indicate missing data → drop those rows
        if temp == -999 or humid == -999 or rain == -999:
            continue

        year  = int(date_str[:4])
        month = int(date_str[4:6])
        season = classify_season(month)

        daily_records.append({
            "year":        year,
            "month":       month,
            "season":      season,
            "temperature": temp,
            "humidity":    humid,
            "rainfall_mm_day": rain
        })

    if not daily_records:
        print(f"  ❌ No valid data parsed for {tehsil_name}. Skipping.")
        continue

    df_daily = pd.DataFrame(daily_records)

    # Group by season and calculate averages across all 5 years
    # For rainfall, we sum per season-year then average across years
    seasonal_group = df_daily.groupby("season")

    for season_name, group in seasonal_group:
        if season_name == "Zaid":
            continue  # Skip Zaid — not a primary crop season for Indore

        # Average daily temperature and humidity across the season
        avg_temp    = round(group["temperature"].mean(), 2)
        avg_humid   = round(group["humidity"].mean(), 2)

        # Seasonal total rainfall = sum of daily rainfall per year, then average across 5 years
        yearly_rain = group.groupby("year")["rainfall_mm_day"].sum()
        avg_rain    = round(yearly_rain.mean(), 2)

        all_seasonal_records.append({
            "tehsil":                    tehsil_name,
            "season":                    season_name,
            "temperature_avg_c":         avg_temp,
            "humidity_avg_pct":          avg_humid,
            "rainfall_seasonal_total_mm": avg_rain,
            "data_source":               "NASA POWER API (T2M + RH2M + PRECTOTCORR) 2019-2023",
            "years_averaged":            5
        })

    print(f"  📊 Processed {len(daily_records)} daily records for {tehsil_name}")

    # Respect NASA API rate limits (1 request per 2 seconds recommended)
    time.sleep(2)


# ============================================================
# STEP 5: SAVE THE FINAL CLIMATE TABLE AS CSV
# This file is then used by build_dataset.py to anchor climate data
# ============================================================
if all_seasonal_records:
    df_out = pd.DataFrame(all_seasonal_records)

    out_path = os.path.join("data", "climate_by_tehsil_season.csv")
    os.makedirs("data", exist_ok=True)
    df_out.to_csv(out_path, index=False)

    print(f"\n✅ Climate data saved: {out_path}")
    print(f"   Total records: {len(df_out)}")
    print(df_out.to_string(index=False))
else:
    print("\n❌ No data was downloaded. Check your internet connection and try again.")
    print("   The existing data/climate_by_tehsil_season.csv (pre-downloaded) can be used instead.")
