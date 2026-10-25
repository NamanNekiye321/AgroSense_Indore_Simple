# 🌾 AgroSense Indore

> **AI-Powered Precision Agronomic Advisory Platform**  
> Crop recommendation & fertilizer planning system for Indore District, Malwa Plateau (Zone X)  
> Built with Node.js + Express · Python ML · MongoDB · scikit-learn

---

## 👥 Team

| Member | Role | Responsible Files |
|---|---|---|
| **Luv** | Frontend & UI | `frontend/index.html`, `frontend/style.css`, `frontend/app.js` |
| **Kunal** | Backend & Server | `backend/server.js`, `backend/routes/api.js`, `backend/package.json` |
| **Naman** | Database & ML Bridge | `backend/database/`, `backend/ml_service/ml_bridge.js`, `predictor_service.py` |
| **Kuldeep** | ML Training & Data Pipeline | `ml/step1_download_nasa_climate.py`, `ml/step2_scrape_govt_data.py`, `ml/build_dataset.py`, `ml/train_indore_model.py` |
| **Arhaan** | Documentation & Diagrams | `diagrams/` (all 15 draw.io XML diagrams), `README.md` |

---

## 🚀 Running the Project

### Requirements
- **Node.js** v16+
- **Python** 3.8+ with `pandas`, `numpy`, `scikit-learn`, `joblib`
- **MongoDB** running locally on port `27017` (or Atlas URI set in `.env`)

### Start
```bash
cd backend
npm install
node server.js
```

Then open **`http://localhost:5001`** in your browser.

> **Note**: If MongoDB is offline the app still works — it falls back to an in-memory buffer automatically.

---

## 🤖 ML Model

| Detail | Value |
|---|---|
| **Algorithm** | Random Forest (Multi-Class Classifier) |
| **Training Accuracy** | 80.0% (5-Fold Stratified CV) |
| **Feature Inputs** | N, P, K, pH, Temperature (°C), Humidity (%), Rainfall (mm) |
| **Crop Classes** | 22 crops (Soybean, Wheat, Chickpea, Maize, Onion, Potato, etc.) |
| **Model File** | `models/indore_crop_model.pkl` |
| **Models Benchmarked** | Random Forest (80.0%), Extra Trees (78.5%), Gradient Boosting (76.0%), Decision Tree |

### How Accuracy Was Calculated
1. 1,500 balanced rows synthesized from NASA POWER + ICAR agronomic rules via NumPy/Pandas.
2. 80/20 stratified train-test split (ensures all 22 crop classes appear in both sets).
3. 5-Fold Stratified Cross-Validation on the training set.
4. Best model selected by F1-Score and serialized to `.pkl` via `joblib`.

---

## 🌿 Fertilizer Formula (ICAR Stoichiometric Method)

Calibrated for Indore **Vertisol** soils. Given farmer's soil test values and land acreage:

1. **DAP** (covers Phosphorus): `DAP_kg = (P_target - P_actual) / 0.46`
2. **Urea** (covers remaining Nitrogen): `Urea_kg = (N_target - N_actual) / 0.46`
3. **MOP** (covers Potassium): `MOP_kg = (K_target - K_actual) / 0.60`
4. **Scale by Acreage**: multiply per-acre values by `landAreaAcres`

---

## 📊 Data Sources

| Source | What It Provides | Output File |
|---|---|---|
| **NASA POWER API** | 5-year satellite climate data (temp, humidity, rainfall) for all 5 tehsils | `data/climate_by_tehsil_season.csv` |
| **ICAR-IISR Indore** | Soybean NPK Package of Practices (NPKS 25:60:40) | `data/crop_rules.csv` |
| **RVSKVV / CoA Indore** | Wheat, Gram, Maize guidelines for Malwa Vertisols | `data/crop_rules.csv` |
| **GOI Soil Health Card Portal** | Indore District soil test rating chart | `data/soil_profile.csv` |
| **NumPy + Pandas** | Synthesize 1,500 calibrated training rows from above sources | `data/raw/indore_crop_dataset.csv` |
| **Govt MSP (2024)** | Minimum Support Prices (Soybean ₹4892, Wheat ₹2275/qtl) | `data/crop_rules.csv` |

---

## 📁 Project Structure

```
AgroSense_Indore_Simple/
│
├── backend/
│   ├── database/
│   │   ├── models/Recommendation.js     # MongoDB/Mongoose schema for consultation history
│   │   └── mongodb_service.js           # Connection manager + in-memory resilience buffer
│   ├── ml_service/
│   │   ├── ml_bridge.js                 # Node.js → Python subprocess bridge (IPC via JSON)
│   │   └── predictor_service.py         # Loads .pkl model, runs predict_proba, computes ICAR dosage
│   ├── routes/
│   │   └── api.js                       # REST endpoints: /api/recommend, /api/history, /api/status
│   ├── .env                             # PORT=5001, MONGODB_URI config
│   ├── package.json                     # Dependencies: express, mongoose, cors, dotenv
│   └── server.js                        # Entry point: Express app + static file server
│
├── data/
│   ├── climate_by_tehsil_season.csv     # NASA POWER 5-year averages per tehsil & season
│   ├── crop_rules.csv                   # ICAR/RVSKVV NPK targets & government MSP rates
│   ├── soil_profile.csv                 # Indore Vertisol district soil benchmarks
│   └── raw/
│       └── indore_crop_dataset.csv      # 1,500 synthesized training rows
│
├── diagrams/                            # All draw.io XML diagrams (open in diagrams.net)
│   ├── Database-Architecture.xml        # 3-tier MongoDB architecture (App → ODM → DB)
│   ├── Class-Diagram.xml                # UML classes: User, Farmer, Officer, SoilRecord, Recommendation
│   ├── Sequence-Diagram.xml             # Sequence Diagram 1: Crop Advisory & ML Prediction
│   ├── Sequence-Diagram-1-Prediction.xml
│   ├── Sequence-Diagram-2-DosageScaling.xml  # Tehsil Presets & Fertilizer Calculation
│   ├── Sequence-Diagram-3-HistoryResilience.xml  # Officer Verification & DB Resilience
│   ├── Activity-Diagram.xml             # Activity Diagram 1: Soil Advisory Lifecycle
│   ├── Activity-Diagram-1-Consultation.xml
│   ├── Activity-Diagram-2-TrainingPipeline.xml   # ML Data Pipeline & Model Training
│   ├── State-Machine-Diagram.xml        # Consultation request state transitions
│   ├── System-Architecture.xml          # 3-tier system architecture overview
│   ├── ER-Diagram.xml                   # Entity-Relationship diagram
│   ├── Use-Case-Diagram.xml             # Farmer & Officer use cases
│   ├── DFD-Level0.xml                   # Context-level data flow
│   └── DFD-Level1.xml                   # Detailed process data flow
│
├── frontend/
│   ├── index.html                       # Bilingual (Hindi/English) UI, sliders, advisory card
│   ├── style.css                        # Modern dark/light theme CSS design system
│   └── app.js                           # Tehsil presets, NASA auto-fill, API fetch, result render
│
├── ml/
│   ├── step1_download_nasa_climate.py   # Downloads NASA POWER climate data for 5 tehsils
│   ├── step2_scrape_govt_data.py        # Scrapes & parses ICAR / RVSKVV agronomic rules
│   ├── build_dataset.py                 # Generates the 1,500-row Indore-calibrated dataset
│   └── train_indore_model.py            # Trains, benchmarks & serializes the best ML model
│
├── models/
│   └── indore_crop_model.pkl            # Serialized Random Forest (80.0% accuracy)
│
├── AgroSense_Indore_Simple_Presentation_Guide.pdf   # Member-wise presentation guide
└── README.md
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/recommend` | Submit soil values → returns crop + fertilizer plan |
| `GET` | `/api/history` | Fetch past consultation records from MongoDB |
| `GET` | `/api/status` | Check server & MongoDB connection health |

### Example Request — `/api/recommend`
```json
POST /api/recommend
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

### Example Response
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

## 🗺️ Diagrams Quick Reference

All diagrams are in `diagrams/` and can be opened in **[draw.io / diagrams.net](https://app.diagrams.net)** (File → Open from Device).

| Diagram | File | What It Shows |
|---|---|---|
| Database Architecture | `Database-Architecture.xml` | App → Mongoose ODM → MongoDB collection schema |
| Class Diagram | `Class-Diagram.xml` | `User`, `Farmer`, `AgriculturalOfficer`, `SoilRecord`, `Recommendation`, `FertilizerAdvisory` |
| Sequence 1 | `Sequence-Diagram-1-Prediction.xml` | Farmer submits soil → ML inference → advisory returned |
| Sequence 2 | `Sequence-Diagram-2-DosageScaling.xml` | Tehsil auto-preset → acreage input → ICAR dosage scaling |
| Sequence 3 | `Sequence-Diagram-3-HistoryResilience.xml` | Officer verifies records → DB resilience fallback |
| Activity 1 | `Activity-Diagram-1-Consultation.xml` | Full advisory lifecycle with fork/join parallel paths |
| Activity 2 | `Activity-Diagram-2-TrainingPipeline.xml` | NASA ingestion → NumPy synthesis → parallel model training |
| State Machine | `State-Machine-Diagram.xml` | Consultation states: IDLE → PENDING → PROCESSING → SAVED/ERROR |
| ER Diagram | `ER-Diagram.xml` | Entity relationships between farmers, records, recommendations |
| Use Case | `Use-Case-Diagram.xml` | Farmer and Agricultural Officer use case flows |
| DFD Level 0 | `DFD-Level0.xml` | System context view |
| DFD Level 1 | `DFD-Level1.xml` | Internal process data flows |
| System Architecture | `System-Architecture.xml` | 3-tier: Frontend → Express → ML → MongoDB |
