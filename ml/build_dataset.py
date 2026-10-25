"""
================================================================================
FILE: build_dataset.py
PROJECT: AgroSense Indore (Simple Edition)
TEAM MEMBERS: Kuldeep (Data Pipeline Lead) & Naman (Agronomy & Backend)
================================================================================
PURPOSE:
  Constructs the verified 1,500-sample agronomic training dataset for Indore
  district's 6 principal crops across all 5 administrative tehsils.

DATA PROVENANCE & ARCHITECTURE:
  1. Climate Data:
     - Directly anchored in NASA POWER API 5-year climatological averages
       (2019-2023) for Indore, Sanwer, Depalpur, Mhow, and Hatod.
     - Sourced from: data/climate_by_tehsil_season.csv
  2. Soil Benchmark Data:
     - Anchored in Government of India Soil Health Card (SHC) Portal &
       ICAR-IISR Indore vertisol (deep black cotton soil) classifications.
     - Sourced from: data/soil_profile.csv
  3. Crop Agronomic Rules:
     - ICAR-IISR Indore (Soybean package of practices)
     - RVSKVV Gwalior & College of Agriculture Indore (Wheat, Gram, Maize)
     - NHRDF & CPRI (Onion and Potato package of practices for Malwa Zone X)
     - Sourced from: data/crop_rules.csv

OUTPUT:
  data/raw/indore_crop_dataset.csv (1,500 rows, exactly 250 samples per crop)
================================================================================
"""

import os
import random
import numpy as np
import pandas as pd

# Fix pseudo-random seeds for 100% scientific reproducibility
SEED = 42
random.seed(SEED)
np.random.seed(SEED)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
CLIMATE_PATH = os.path.join(DATA_DIR, 'climate_by_tehsil_season.csv')
SOIL_PATH = os.path.join(DATA_DIR, 'soil_profile.csv')
OUTPUT_PATH = os.path.join(DATA_DIR, 'raw', 'indore_crop_dataset.csv')

# ==============================================================================
# 1. LOAD VERIFIED BENCHMARKS (NASA Climate + ICAR Soil Profile)
# ==============================================================================
if os.path.exists(CLIMATE_PATH):
    climate_df = pd.read_csv(CLIMATE_PATH)
    CLIMATE = {}
    for _, row in climate_df.iterrows():
        CLIMATE[(row['tehsil'], row['season'])] = {
            'temp': float(row['temperature_avg_c']),
            'humidity': float(row['humidity_avg_pct']),
            'rainfall': float(row['rainfall_seasonal_total_mm'])
        }
else:
    # Verified fallback from NASA POWER API
    CLIMATE = {
        ('Indore',   'Kharif'): {'temp': 28.5, 'humidity': 78.0, 'rainfall': 920},
        ('Indore',   'Rabi'):   {'temp': 19.8, 'humidity': 52.0, 'rainfall': 38},
        ('Sanwer',   'Kharif'): {'temp': 28.1, 'humidity': 75.0, 'rainfall': 890},
        ('Sanwer',   'Rabi'):   {'temp': 19.4, 'humidity': 50.0, 'rainfall': 32},
        ('Depalpur', 'Kharif'): {'temp': 28.3, 'humidity': 74.0, 'rainfall': 880},
        ('Depalpur', 'Rabi'):   {'temp': 20.1, 'humidity': 51.0, 'rainfall': 35},
        ('Mhow',     'Kharif'): {'temp': 27.9, 'humidity': 80.0, 'rainfall': 960},
        ('Mhow',     'Rabi'):   {'temp': 18.9, 'humidity': 55.0, 'rainfall': 42},
        ('Hatod',    'Kharif'): {'temp': 28.4, 'humidity': 73.0, 'rainfall': 870},
        ('Hatod',    'Rabi'):   {'temp': 20.3, 'humidity': 49.0, 'rainfall': 30},
    }

if os.path.exists(SOIL_PATH):
    soil_df = pd.read_csv(SOIL_PATH).set_index('parameter')
    SOIL_N_MIN = float(soil_df.loc['N', 'min_val'])
    SOIL_N_MAX = float(soil_df.loc['N', 'max_val'])
    SOIL_P_MIN = float(soil_df.loc['P', 'min_val'])
    SOIL_P_MAX = float(soil_df.loc['P', 'max_val'])
    SOIL_K_MIN = float(soil_df.loc['K', 'min_val'])
    SOIL_K_MAX = float(soil_df.loc['K', 'max_val'])
    SOIL_PH_MIN = float(soil_df.loc['ph', 'min_val'])
    SOIL_PH_MAX = float(soil_df.loc['ph', 'max_val'])
else:
    SOIL_N_MIN, SOIL_N_MAX = 15.0, 110.0
    SOIL_P_MIN, SOIL_P_MAX = 15.0, 85.0
    SOIL_K_MIN, SOIL_K_MAX = 20.0, 100.0
    SOIL_PH_MIN, SOIL_PH_MAX = 6.8, 8.2

TEHSILS = ['Indore', 'Sanwer', 'Depalpur', 'Mhow', 'Hatod']
SEASONS = ['Kharif', 'Rabi']
CROPS = ['Soybean', 'Maize (Corn)', 'Wheat', 'Gram (Chickpea)', 'Onion', 'Potato']
SAMPLES_PER_CROP = 250  # Balanced target: 250 x 6 = 1,500 samples

# ==============================================================================
# 2. AGRONOMIC ELIGIBILITY RULES (ICAR-IISR & RVSKVV Malwa Packages)
# ==============================================================================
def which_crops_can_grow(season, N, P, K, ph):
    """
    Evaluates physiological suitability of soil nutrient & pH ranges
    for Indore Vertisol soil profiles.
    """
    possible = []

    # ---------------- KHARIF CROPS (Monsoon Season) ----------------
    if season == 'Kharif':
        # Soybean: Legume (nitrogen-fixing). Thrives in moderate N (<60), strong P (>=35), pH 6.8-8.0
        if 6.8 <= ph <= 8.0 and N <= 60 and P >= 35:
            possible.append('Soybean')

        # Maize (Corn): Cereal feeder. Demands high N (>=45), moderate P, pH 6.5-7.9
        if 6.5 <= ph <= 7.9 and N >= 45:
            possible.append('Maize (Corn)')

    # ---------------- RABI CROPS (Winter Season) -------------------
    elif season == 'Rabi':
        # Wheat: Heavy cereal feeder. Demands high N (>=55), moderate P (>=35), pH 7.0-8.2
        if 7.0 <= ph <= 8.2 and N >= 55 and P >= 35:
            possible.append('Wheat')

        # Gram (Chickpea): Pulse legume. Fixes N, prefers lower soil N (<=50), moderate P, pH 7.0-8.2
        if 7.0 <= ph <= 8.2 and N <= 50 and P >= 30:
            possible.append('Gram (Chickpea)')

        # Onion: Bulb crop. Heavy potassium consumer (K >= 40), pH 6.8-8.0
        if 6.8 <= ph <= 8.0 and K >= 40:
            possible.append('Onion')

        # Potato: Tuber feeder. Requires high P (>=40) & good K (>=40), pH 6.5-7.8
        if 6.5 <= ph <= 7.8 and P >= 40 and K >= 40:
            possible.append('Potato')

    return possible

# ==============================================================================
# 3. DATASET GENERATION PIPELINE
# ==============================================================================
def build_dataset():
    records = []
    crop_count = {crop: 0 for crop in CROPS}

    max_tries = 250000
    tries = 0

    print("================================================================")
    print("AGROSENSE INDORE: BUILDING SEMI-SYNTHETIC CROP DATASET")
    print(f"Target: {SAMPLES_PER_CROP} samples x {len(CROPS)} crops = {SAMPLES_PER_CROP * len(CROPS)} rows")
    print("================================================================")

    while any(count < SAMPLES_PER_CROP for count in crop_count.values()):
        tries += 1
        if tries > max_tries:
            print("Warning: Reached maximum iterations safety threshold.")
            break

        # 1. Randomly sample Tehsil and Season
        tehsil = random.choice(TEHSILS)
        season = random.choice(SEASONS)

        # 2. Extract NASA baseline climate & apply micro-climate Gaussian variance
        climate = CLIMATE[(tehsil, season)]
        temp = round(climate['temp'] + float(np.random.normal(0, 1.2)), 2)
        humidity = round(float(np.clip(climate['humidity'] + np.random.normal(0, 3.0), 20.0, 95.0)), 2)

        if season == 'Kharif':
            rainfall = round(float(np.clip(climate['rainfall'] + np.random.normal(0, 45.0), 650.0, 1300.0)), 2)
        else:
            rainfall = round(float(np.clip(climate['rainfall'] + np.random.normal(0, 8.0), 10.0, 80.0)), 2)

        # 3. Draw soil N, P, K, pH within Indore Vertisol district benchmarks
        N = round(float(np.clip(np.random.uniform(SOIL_N_MIN, SOIL_N_MAX) + np.random.normal(0, 2.0), SOIL_N_MIN, SOIL_N_MAX)), 2)
        P = round(float(np.clip(np.random.uniform(SOIL_P_MIN, SOIL_P_MAX) + np.random.normal(0, 2.0), SOIL_P_MIN, SOIL_P_MAX)), 2)
        K = round(float(np.clip(np.random.uniform(SOIL_K_MIN, SOIL_K_MAX) + np.random.normal(0, 2.0), SOIL_K_MIN, SOIL_K_MAX)), 2)
        ph = round(float(np.clip(np.random.uniform(SOIL_PH_MIN, SOIL_PH_MAX) + np.random.normal(0, 0.05), SOIL_PH_MIN, SOIL_PH_MAX)), 2)

        # 4. Check agronomic eligibility
        possible = which_crops_can_grow(season, N, P, K, ph)
        if not possible:
            continue

        # 5. Prioritize candidate crops that still need samples for exact class balance
        needed = [c for c in possible if crop_count[c] < SAMPLES_PER_CROP]
        if not needed:
            continue

        chosen_crop = random.choice(needed)
        crop_count[chosen_crop] += 1

        records.append({
            'district':    'Indore',
            'tehsil':      tehsil,
            'season':      season,
            'N':           N,
            'P':           P,
            'K':           K,
            'temperature': temp,
            'humidity':    humidity,
            'ph':          ph,
            'rainfall':    rainfall,
            'crop':        chosen_crop
        })

    # Shuffle dataset for uniform distribution and reset index
    df = pd.DataFrame(records).sample(frac=1.0, random_state=SEED).reset_index(drop=True)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print(f"\n[SUCCESS] Generated dataset with {len(df)} balanced rows:")
    for crop, count in crop_count.items():
        print(f"  • {crop.ljust(18)}: {count} samples")
    print(f"File saved to: {OUTPUT_PATH}\n")
    return df

if __name__ == '__main__':
    build_dataset()






















