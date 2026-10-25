// ============================================================
// FILE: api.js  (inside backend/routes/)
// WHO MADE THIS: Kunal (REST Routes) + Naman (DB Integration)
// WHAT IT DOES: Defines Express endpoints:
//               POST /api/recommend   -> AI Crop & Dosage recommendation
//               GET  /api/history     -> Ledger of past consultations
//               GET  /api/status      -> Health & DB connection diagnostics
//               GET  /api/atlas       -> Indore 5-tehsil regional benchmarks
// ============================================================

const express  = require('express');
const router   = express.Router();
const db       = require('../database/mongodb_service');
const mlBridge = require('../ml_service/ml_bridge');

// Government MSP Benchmarks (2024-25 Season)
const MSP_BENCHMARKS = {
    'Soybean':          '₹4,892 / quintal',
    'Wheat':            '₹2,275 / quintal',
    'Gram (Chickpea)':  '₹5,440 / quintal',
    'Maize (Corn)':     '₹2,090 / quintal',
    'Onion':            '₹1,800 - ₹2,400 / quintal (Mandi)',
    'Potato':           '₹1,200 - ₹1,800 / quintal (Cold Storage)'
};

// ============================================================
// ROUTE 1: POST /api/recommend
// ============================================================
router.post('/recommend', async (req, res) => {
    const { N, P, K, ph, rainfall, temperature, humidity, tehsil, farmer_name, village, land_area, contact_no } = req.body;

    if (N === undefined || P === undefined || K === undefined || ph === undefined) {
        return res.status(400).json({
            success: false,
            error: 'Please provide N, P, K, and pH values.'
        });
    }

    const acres = parseFloat(land_area) > 0 ? parseFloat(land_area) : 1.0;

    const soilData = {
        N:           parseFloat(N),
        P:           parseFloat(P),
        K:           parseFloat(K),
        ph:          parseFloat(ph),
        rainfall:    parseFloat(rainfall)    || 850,
        temperature: parseFloat(temperature) || 28,
        humidity:    parseFloat(humidity)    || 70,
        tehsil:      tehsil || 'Indore'
    };

    try {
        // Step 1: Predict with Python Random Forest model
        const aiResult = await mlBridge.predictCrop(soilData);

        // Step 2: Attach MSP benchmark to recommendations
        const enhancedRecommendations = aiResult.recommendations.map(rec => ({
            ...rec,
            msp: MSP_BENCHMARKS[rec.crop] || 'Market Mandi Rate'
        }));

        // Step 3: Scale fertilizer dosage by land acreage
        const basePlan = aiResult.fertilizer_plan;
        const totalPlan = {
            per_acre: basePlan,
            total_farm: {
                acres: acres,
                urea_total_kg: Math.round(basePlan.urea_kg * acres * 10) / 10,
                dap_total_kg:  Math.round(basePlan.dap_kg * acres * 10) / 10,
                mop_total_kg:  Math.round(basePlan.mop_kg * acres * 10) / 10,
                organic_ton:   Math.round(basePlan.organic_ton * acres * 10) / 10
            },
            remarks: basePlan.remarks
        };

        // Step 4: Persist in MongoDB
        const savedRecord = await db.saveRecommendation({
            farmer_name:    farmer_name || 'Farmer Guest',
            farmer_village: village     || '',
            tehsil:         soilData.tehsil,
            land_area:      acres,
            contact_no:     contact_no  || '',
            soil_inputs:    soilData,
            primary_crop:      enhancedRecommendations[0].crop,
            confidence:        enhancedRecommendations[0].confidence,
            alternative_crops: enhancedRecommendations.slice(1).map(r => r.crop),
            fertilizer_plan:   basePlan
        });

        res.json({
            success: true,
            recommendations:  enhancedRecommendations,
            fertilizer_plan:  totalPlan,
            record_id:        savedRecord ? savedRecord._id : null
        });

    } catch (error) {
        console.error('Recommendation failed:', error.message);
        res.status(500).json({ success: false, error: 'Server error. Please try again.' });
    }
});

// ============================================================
// ROUTE 2: GET /api/history
// ============================================================
router.get('/history', async (req, res) => {
    try {
        const records = await db.getHistory(20);
        res.json({ success: true, count: records.length, data: records });
    } catch (error) {
        res.status(500).json({ success: false, error: 'Could not fetch history.' });
    }
});

// ============================================================
// ROUTE 3: GET /api/status
// ============================================================
router.get('/status', (req, res) => {
    res.json({
        success: true,
        project: 'AgroSense Indore (Simple Edition)',
        database: db.getStatus()
    });
});

// ============================================================
// ROUTE 4: GET /api/atlas
// 5 Tehsil Verified Regional Benchmarks (NASA + ICAR)
// ============================================================
router.get('/atlas', (req, res) => {
    const atlasData = [
        {
            tehsil: 'Indore',
            soil: 'Deep Black Soil (Vertisol)',
            annual_rain_mm: 920,
            typical_temp_c: 28.5,
            primary_kharif: 'Soybean, Maize',
            primary_rabi: 'Wheat, Gram, Potato',
            ph_range: '7.4 - 8.1'
        },
        {
            tehsil: 'Sanwer',
            soil: 'Medium-to-Deep Black Vertisol',
            annual_rain_mm: 890,
            typical_temp_c: 28.1,
            primary_kharif: 'Soybean',
            primary_rabi: 'Wheat, Gram',
            ph_range: '7.5 - 8.2'
        },
        {
            tehsil: 'Depalpur',
            soil: 'Deep Clayey Vertisol (Heavy Soil)',
            annual_rain_mm: 880,
            typical_temp_c: 28.3,
            primary_kharif: 'Soybean, Maize',
            primary_rabi: 'Wheat, Gram, Onion',
            ph_range: '7.3 - 8.0'
        },
        {
            tehsil: 'Mhow',
            soil: 'Undulating Malwa Ridge Vertisol',
            annual_rain_mm: 960,
            typical_temp_c: 27.9,
            primary_kharif: 'Soybean, Maize',
            primary_rabi: 'Potato, Garlic, Wheat',
            ph_range: '7.2 - 7.9'
        },
        {
            tehsil: 'Hatod',
            soil: 'Medium Black Vertisol',
            annual_rain_mm: 870,
            typical_temp_c: 28.4,
            primary_kharif: 'Soybean',
            primary_rabi: 'Wheat, Gram, Onion',
            ph_range: '7.4 - 8.2'
        }
    ];
    res.json({ success: true, tehsils: atlasData });
});

module.exports = router;
