# 🌾 AgroSense Indore

<div align="center">

**AI-Powered Precision Agronomic Advisory for Indore District & Malwa Plateau (Zone X)**

![Node.js](https://img.shields.io/badge/Node.js-v16+-339933?style=flat-square&logo=node.js&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-NoSQL-47A248?style=flat-square&logo=mongodb&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)

*Recommends crops & fertilizer dosage based on real soil test values, NASA climate data, and ICAR agronomic guidelines — built for Indore farmers.*

</div>

---

## 👥 Team Roles & Responsibilities

| Member | Role | Files |
|---|---|---|
| **Luv** | Frontend & UI | `frontend/index.html`, `frontend/style.css`, `frontend/app.js` |
| **Kunal** | Backend & Server | `backend/server.js`, `backend/routes/api.js`, `backend/package.json` |
| **Naman** | Database & ML Bridge | `backend/database/`, `backend/ml_service/ml_bridge.js`, `predictor_service.py` |
| **Kuldeep** | ML Training & Data Pipeline | `ml/build_dataset.py`, `ml/train_indore_model.py`, `ml/step1_download_nasa_climate.py` |
| **Arhaan** | Documentation & Diagrams | `README.md`, `diagrams/` |

---

## 🚀 How to Run

### Requirements
- **Node.js** v16+
- **Python** 3.8+ with `pandas`, `numpy`, `scikit-learn`, `joblib`
- **MongoDB** running locally on port `27017` *(or set Atlas URI in `.env`)*

### Start the Server
```bash
cd backend
npm install
node server.js
```

Open **`http://localhost:5001`** in your browser.

> 💡 **No MongoDB?** The app still works — it automatically falls back to an in-memory buffer so no data is lost.

---

## 🤖 ML Model & Accuracy

| Detail | Value |
|---|---|
| Algorithm | Random Forest (Multi-Class Classifier) |
| **Accuracy** | **80.0%** (5-Fold Stratified Cross-Validation) |
| Features | N, P, K, pH, Temperature (°C), Humidity (%), Rainfall (mm) |
| Crop Classes | 22 crops (Soybean, Wheat, Chickpea, Maize, Onion, Potato…) |
| Model File | `models/indore_crop_model.pkl` |

### How Accuracy Was Calculated
1. **Data** — 1,500 calibrated rows synthesized from NASA POWER satellite data + ICAR agronomic rules via NumPy/Pandas.
2. **Split** — 80/20 stratified train-test split (all 22 crop classes appear in both sets).
3. **Validation** — 5-Fold Stratified Cross-Validation on the training set.
4. **Benchmark** — All four models compared; best selected by F1-Score and saved via `joblib`.

### Models Benchmarked
| Model | Accuracy |
|---|---|
| ✅ **Random Forest** | **80.0%** ← *Champion* |
| Extra Trees | 78.5% |
| Gradient Boosting | 76.0% |
| Decision Tree | ~70% |

---

## 🌿 Fertilizer Formula (ICAR Stoichiometric Method)

Calibrated for Indore **Vertisol** soils. Computes elemental deficit from soil test and scales by acreage:

```
DAP  (Phosphorus)  →  DAP_kg   = (P_target − P_actual) ÷ 0.46
Urea (Nitrogen)    →  Urea_kg  = (N_target − N_actual) ÷ 0.46
MOP  (Potassium)   →  MOP_kg   = (K_target − K_actual) ÷ 0.60

Total for farm     →  × landAreaAcres
```

---

## 🔬 Data Pipeline & Sources

| Source | What It Provides | Output |
|---|---|---|
| **NASA POWER API** | 5-year satellite climate (temp, humidity, rainfall) for all 5 tehsils | `data/climate_by_tehsil_season.csv` |
| **ICAR-IISR Indore** | Soybean NPK Package of Practices (NPKS 25:60:40) | `data/crop_rules.csv` |
| **RVSKVV / CoA Indore** | Wheat, Gram, Maize guidelines for Malwa Vertisols | `data/crop_rules.csv` |
| **GOI Soil Health Card Portal** | Indore District soil test rating chart | `data/soil_profile.csv` |
| **NumPy + Pandas** | Synthesizes 1,500 balanced training rows from above | `data/raw/indore_crop_dataset.csv` |

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/recommend` | Submit soil inputs → returns crop + fertilizer plan |
| `GET` | `/api/history` | Fetch past consultations from MongoDB |
| `GET` | `/api/status` | Server & MongoDB health check |

### Example — POST `/api/recommend`
```json
{
  "tehsil": "Sanwer",
  "nitrogen": 45,
  "phosphorus": 35,
  "potassium": 50,
  "ph": 7.6,
  "temperature": 28.5,
  "humidity": 68,
  "rainfall": 820,
  "landAreaAcres": 2.5
}
```

### Response
```json
{
  "success": true,
  "primaryCrop": "Soybean",
  "confidence": 94,
  "alternativeCrops": ["Wheat", "Chickpea"],
  "fertilizerPlan": {
    "ureaKgPerAcre": 32.6,
    "dapKgPerAcre": 54.3,
    "mopKgPerAcre": 16.7,
    "totalFarmUreaKg": 81.5,
    "totalFarmDapKg": 135.8,
    "totalFarmMopKg": 41.7
  },
  "mspRate": 4892
}
```

---

## 📁 Project Structure

```
AgroSense_Indore_Simple/
│
├── backend/
│   ├── database/
│   │   ├── models/Recommendation.js     # MongoDB schema for consultation history
│   │   └── mongodb_service.js           # Mongoose connection + in-memory fallback buffer
│   ├── ml_service/
│   │   ├── ml_bridge.js                 # Node.js → Python subprocess bridge
│   │   └── predictor_service.py         # Loads .pkl, runs predict_proba, computes ICAR dosage
│   ├── routes/
│   │   └── api.js                       # REST routes: /recommend, /history, /status
│   ├── .env                             # PORT & MONGODB_URI config
│   ├── package.json                     # Node.js dependencies
│   └── server.js                        # Express server entry point
│
├── data/
│   ├── climate_by_tehsil_season.csv     # NASA POWER 5-year averages per tehsil
│   ├── crop_rules.csv                   # ICAR/RVSKVV NPK targets & MSP rates
│   ├── soil_profile.csv                 # Indore Vertisol district benchmarks
│   └── raw/
│       └── indore_crop_dataset.csv      # 1,500 synthesized training rows
│
├── frontend/
│   ├── index.html                       # Bilingual (Hindi/English) UI with sliders & advisory card
│   ├── style.css                        # Dark/light theme CSS design system
│   └── app.js                           # Tehsil presets, NASA auto-fill, API fetch, result render
│
├── ml/
│   ├── step1_download_nasa_climate.py   # NASA POWER climate downloader (5 tehsils, 5 years)
│   ├── step2_scrape_govt_data.py        # Government portal data sourcing & parsing
│   ├── build_dataset.py                 # Generates the 1,500-row Indore-calibrated dataset
│   └── train_indore_model.py            # Trains, benchmarks & serializes the best ML model
│
├── models/
│   └── indore_crop_model.pkl            # Serialized Random Forest — 80.0% accuracy
│
└── README.md
```

---

