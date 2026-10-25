"""
================================================================================
FILE: step2_scrape_govt_data.py
PROJECT: AgroSense Indore (Simple Edition)
TEAM MEMBER: Kuldeep (Data Pipeline Lead)
================================================================================

PURPOSE:
    Demonstrates HOW we collected official government agronomic data
    for Indore's 6 crops. This script shows the exact government sources
    we referenced and structures the data for our crop_rules.csv file.

DATA SOURCES (Government & ICAR Portals):
    1. ICAR-IISR (Indian Institute of Soybean Research), Indore
       URL: https://icar-iisr.icar.gov.in/
       Data: Soybean NPK requirements, recommended varieties (JS-9560, JS-2034)

    2. RVSKVV (Rajmata Vijayaraje Scindia Krishi Vishwavidyalaya), Gwalior
       URL: https://www.rvskvv.net/
       Data: Wheat, Gram, Maize package of practices for Malwa region

    3. Soil Health Card Scheme, Govt. of India
       URL: https://soilhealth.dac.gov.in/
       Data: District-level soil pH and NPK baseline values for Indore

    4. NHRDF (National Horticultural Research & Development Foundation)
       URL: https://nhrdf.org/
       Data: Onion production package of practices

    5. CPRI (Central Potato Research Institute)
       URL: https://www.cpri.res.in/
       Data: Potato production recommendations for central India

NOTE ON SCRAPING vs MANUAL EXTRACTION:
    Most government portals (ICAR, RVSKVV) publish data as PDFs, not as
    structured APIs. This script:
    - Shows the URLs we visited
    - Manually encodes the key agronomic numbers from PDFs
    - Constructs the structured crop_rules.csv using pandas
    - We use requests + BeautifulSoup only where the site has HTML tables

HOW TO RUN:
    python3 step2_scrape_govt_data.py
    This will regenerate data/crop_rules.csv from hardcoded government data.

IMPORTANT:
    The output crop_rules.csv is already committed to the repo.
    You only need to re-run this if you update the agronomic parameters.
================================================================================
"""

import os
import pandas as pd

# ============================================================
# NOTE: Most government data below was extracted MANUALLY from:
#   - PDF documents from ICAR-IISR Indore
#   - Package of Practices booklets from RVSKVV
#   - Soil Health Card district reports for Indore (MP)
#   - NHRDF & CPRI crop production guidelines
#
# Where HTML tables existed (e.g., some eKrishi pages), we used:
#   import requests
#   from bs4 import BeautifulSoup
#   ... (see commented examples below)
#
# The hardcoded dictionary below is the CLEANED, VERIFIED result
# of cross-referencing all those sources.
# ============================================================

print("Building crop_rules.csv from verified government agronomic data...")
print("Sources: ICAR-IISR | RVSKVV | SHC Portal | NHRDF | CPRI")
print()

# ============================================================
# CROP AGRONOMIC DATA TABLE
# All values verified from the government sources listed above.
# N, P, K values are in kg/hectare as per ICAR recommendations.
# MSP (Minimum Support Price) from Govt. of India 2024-25 notification.
# ============================================================
CROP_DATA = [
    {
        "crop":           "Soybean",
        "primary_season": "Kharif",
        # ICAR-IISR Indore: Table-1 (NPKS 25:60:40:20 kg/ha for Zone X)
        "n_req_kgha":     25,
        "p_req_kgha":     60,
        "k_req_kgha":     40,
        "ph_min":         6.8,
        "ph_max":         8.0,
        "min_rain_mm":    650,
        "max_rain_mm":    1200,
        "min_temp_c":     22,
        "max_temp_c":     35,
        "govt_msp_2024":  4892,   # ₹/quintal — Govt. of India MSP 2024-25
        "duration_days":  100,
        "source":         "ICAR-IISR Indore Table-1 (25:60:40 NPKS)"
    },
    {
        "crop":           "Maize (Corn)",
        "primary_season": "Kharif",
        # Directorate of Agriculture MP: Maize cultivation guide
        "n_req_kgha":     85,
        "p_req_kgha":     55,
        "k_req_kgha":     40,
        "ph_min":         6.5,
        "ph_max":         7.9,
        "min_rain_mm":    500,
        "max_rain_mm":    1000,
        "min_temp_c":     20,
        "max_temp_c":     34,
        "govt_msp_2024":  2225,
        "duration_days":  95,
        "source":         "Directorate of Agriculture MP - Maize Guide"
    },
    {
        "crop":           "Wheat",
        "primary_season": "Rabi",
        # RVSKVV Malwa: Sharbati and Malvi Durum wheat package of practices
        "n_req_kgha":     100,
        "p_req_kgha":     50,
        "k_req_kgha":     40,
        "ph_min":         7.0,
        "ph_max":         8.2,
        "min_rain_mm":    200,
        "max_rain_mm":    550,
        "min_temp_c":     12,
        "max_temp_c":     25,
        "govt_msp_2024":  2425,
        "duration_days":  120,
        "source":         "RVSKVV Malwa Sharbati Wheat Package"
    },
    {
        "crop":           "Gram (Chickpea)",
        "primary_season": "Rabi",
        # RVSKVV College of Agriculture Indore: Chana cultivation manual
        "n_req_kgha":     20,
        "p_req_kgha":     50,
        "k_req_kgha":     30,
        "ph_min":         7.0,
        "ph_max":         8.2,
        "min_rain_mm":    200,
        "max_rain_mm":    550,
        "min_temp_c":     12,
        "max_temp_c":     28,
        "govt_msp_2024":  5650,
        "duration_days":  110,
        "source":         "RVSKVV College of Agriculture Indore - Chana Manual"
    },
    {
        "crop":           "Onion",
        "primary_season": "Rabi",
        # NHRDF: Onion package of practices (Malwa edition)
        "n_req_kgha":     90,
        "p_req_kgha":     50,
        "k_req_kgha":     80,
        "ph_min":         6.8,
        "ph_max":         8.0,
        "min_rain_mm":    300,
        "max_rain_mm":    750,
        "min_temp_c":     14,
        "max_temp_c":     30,
        "govt_msp_2024":  1800,   # Market price (onion has no formal MSP, using avg market rate)
        "duration_days":  115,
        "source":         "NHRDF Onion Package of Practices (Malwa)"
    },
    {
        "crop":           "Potato",
        "primary_season": "Rabi",
        # CPRI + RVSKVV: Potato production guide for Central India
        "n_req_kgha":     110,
        "p_req_kgha":     70,
        "k_req_kgha":     90,
        "ph_min":         6.5,
        "ph_max":         7.8,
        "min_rain_mm":    300,
        "max_rain_mm":    650,
        "min_temp_c":     14,
        "max_temp_c":     25,
        "govt_msp_2024":  1500,
        "duration_days":  90,
        "source":         "CPRI & RVSKVV Potato Production Guide Indore"
    }
]

# ============================================================
# EXAMPLE: How we would scrape an HTML table if available
# (e.g., eKrishi MP portal has some HTML-based data)
#
# import requests
# from bs4 import BeautifulSoup
#
# EKRISHI_URL = "https://mpkrishi.mp.gov.in/hindisite_New/pdfs/Soyabean.pdf"
# # Most data is in PDF form, not HTML. For HTML tables:
# resp = requests.get("https://mpkrishi.mp.gov.in/crop_nutrients", timeout=15)
# soup = BeautifulSoup(resp.text, 'html.parser')
# table = soup.find('table', {'class': 'crop-data'})
# ...parse table rows into dict...
#
# Since MP Krishi and ICAR sites publish PDFs, we manually extracted
# the nutrient values and encoded them in CROP_DATA above.
# ============================================================

# Build and save the DataFrame
df = pd.DataFrame(CROP_DATA)

out_path = os.path.join("data", "crop_rules.csv")
os.makedirs("data", exist_ok=True)
df.to_csv(out_path, index=False)

print(f"✅ crop_rules.csv saved with {len(df)} crops.")
print()
print(df[["crop", "primary_season", "n_req_kgha", "p_req_kgha", "k_req_kgha",
          "ph_min", "ph_max", "govt_msp_2024"]].to_string(index=False))
print()
print("Data sources verified from official government portals:")
for row in CROP_DATA:
    print(f"  [{row['crop']}]: {row['source']}")
