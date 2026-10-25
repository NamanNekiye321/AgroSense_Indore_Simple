# 🌾 AgroSense Indore (Simple & Clean Edition)

AI-Powered Precision Agronomic Engine for Indore District & Malwa Plateau (Zone X).

---

## 👥 Team Roles & Responsibilities

| Member | Role | Files Responsible For |
|---|---|---|
| **Luv** | Frontend & UI | `frontend/index.html`, `frontend/style.css`, `frontend/app.js` |
| **Kunal** | Backend & Server | `backend/server.js`, `backend/routes/api.js`, `backend/package.json` |
| **Naman** | Database & ML Bridge | `backend/database/`, `backend/ml_service/ml_bridge.js`, `predictor_service.py` |
| **Kuldeep** | ML Training & Data Pipeline | `ml/step1_download_nasa_climate.py`, `ml/step2_scrape_govt_data.py`, `ml/build_dataset.py`, `ml/train_indore_model.py` |
| **Arhaan** | Architecture & Diagrams | `diagrams/` (`Database-Architecture.xml`, `System-Architecture.xml`, `ER-Diagram.xml`, `DFD-Level0.xml`, `DFD-Level1.xml`) |

---

## 🚀 How to Run the Project (Step-by-Step)

### 1. Requirements
* **Node.js** (v16+)
* **Python** (v3.8+) with `pandas`, `numpy`, `scikit-learn`, `joblib`
* **MongoDB** (Local daemon on port `27017` or Atlas cloud URI in `.env`)

### 2. Start the Backend Server
```bash
cd backend
npm install
node server.js
```
The server will start at: **`http://localhost:5001`**

### 3. Open in Browser
Open your browser and navigate to:
```
http://localhost:5001
```

---

## 🔬 Data Pipeline & Provenance (How Data Was Sourced)

1. **NASA POWER Climatology (`ml/step1_download_nasa_climate.py`)**:
   - Downloads 5 years (2019-2023) of daily satellite weather for all 5 tehsils (Indore, Sanwer, Depalpur, Mhow, Hatod).
   - Parameters: Temperature (`T2M`), Relative Humidity (`RH2M`), Precipitation (`PRECTOTCORR`).
   - Sourced into: `data/climate_by_tehsil_season.csv`.

2. **Official Government Portals (`ml/step2_scrape_govt_data.py`)**:
   - **ICAR-IISR Indore** (Soybean Package of Practices & NPKS 25:60:40 standards).
   - **RVSKVV Gwalior / CoA Indore** (Wheat, Gram, Maize Package of Practices for Malwa Vertisols).
   - **Soil Health Card Portal (GOI)** (Indore District soil test rating chart).
   - **NHRDF & CPRI** (Onion and Potato commercial cultivation guides).
   - Sourced into: `data/crop_rules.csv` & `data/soil_profile.csv`.

3. **Dataset Generation (`ml/build_dataset.py`)**:
   - Uses `numpy` & `pandas` to generate 1,500 balanced rows (exactly 250 samples for each of the 6 crops).
   - Sourced into: `data/raw/indore_crop_dataset.csv`.

4. **Model Training (`ml/train_indore_model.py`)**:
   - Evaluates Random Forest, Extra Trees, Gradient Boosting, and Decision Tree via 5-Fold Stratified Cross-Validation.
   - Saves trained model to: `models/indore_crop_model.pkl`.

---

## 📁 Project Structure

```
AgroSense_Indore_Simple/
├── backend/
│   ├── database/
│   │   ├── models/Recommendation.js       # MongoDB schema for farmer consultation history
│   │   └── mongodb_service.js             # Mongoose connection & resilient in-memory buffer
│   ├── ml_service/
│   │   ├── ml_bridge.js                   # Node.js child_process bridge to Python
│   │   └── predictor_service.py           # Python script that loads model & computes ICAR fertilizer
│   ├── routes/
│   │   └── api.js                         # Express REST routes (/api/recommend, /api/history, /api/status, /api/atlas)
│   ├── .env                               # Server configuration (PORT, MONGODB_URI)
│   ├── package.json                       # Node.js project manifest & dependencies
│   └── server.js                          # Main Express server entry point & static file server
├── data/
│   ├── climate_by_tehsil_season.csv       # NASA POWER 5-year averages per tehsil
│   ├── crop_rules.csv                     # ICAR-IISR & RVSKVV nutrient requirements & MSP
│   ├── soil_profile.csv                   # Indore Vertisols district benchmarks
│   └── raw/
│       └── indore_crop_dataset.csv        # 1,500 balanced rows generated from NASA & ICAR data
├── diagrams/
│   ├── Database-Architecture.xml          # draw.io XML for MongoDB architecture & collections
│   ├── System-Architecture.xml            # 3-Tier system architecture
│   ├── ER-Diagram.xml                     # Entity-Relationship diagram
│   ├── Use-Case-Diagram.xml               # Actor and user workflow diagram
│   ├── DFD-Level0.xml                     # Context level data flow
│   └── DFD-Level1.xml                     # Detailed process data flow
├── frontend/
│   ├── index.html                         # Semantic HTML5 layout with Gov topbar, hero, sliders & atlas
│   ├── style.css                          # Modern dark/light theme CSS design system
│   └── app.js                             # Sliders, bilingual engine, NASA presets, API fetch
├── ml/
│   ├── step1_download_nasa_climate.py     # NASA POWER climate downloader with documentation
│   ├── step2_scrape_govt_data.py          # Government data sourcing & PDF extraction script
│   ├── build_dataset.py                   # Generates Indore-calibrated 1,500 row dataset
│   └── train_indore_model.py              # Evaluates 4 ML models & saves best to .pkl
├── models/
│   └── indore_crop_model.pkl              # Trained Random Forest model binary
└── README.md                              # Complete documentation & viva reference
```

---

## 🎯 Key Viva Concepts

* **Model Used**: Random Forest Multi-Class Classifier trained on 7 agro-climatic inputs (N, P, K, Temperature, Humidity, pH, Rainfall).
* **Database**: MongoDB (NoSQL) with Mongoose ODM and automatic graceful in-memory fallback if the database daemon is offline.
* **Fertilizer Formula**: Tailored for Indore Vertisols. DAP is applied first for Phosphorus ($P_2O_5 / 0.46$), Urea covers remaining Nitrogen ($N_{rem} / 0.46$), and MOP covers Potassium ($K_2O / 0.60$), scaled to the farmer's land acreage.
