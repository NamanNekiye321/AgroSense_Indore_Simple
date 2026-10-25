/* ==========================================================================
   FILE: app.js
   PROJECT: AgroSense Indore (Simple Edition)
   DEVELOPERS: Luv (Frontend Interactivity) & Naman (API Integration)
   PURPOSE: Complete client logic:
            1. Sliders & real-time badge syncing
            2. Verified NASA POWER climate presets for 5 Tehsils
            3. English / Hindi bilingual localization
            4. Dark / Light theme toggling
            5. AI Recommendation request & rendering
            6. Acreage-scaled fertilizer dosage calculation
            7. Live MongoDB Consultation Ledger & DB Status
   ========================================================================== */

// ==========================================================================
// 1. BILINGUAL LOCALIZATION DICTIONARY (English & Hindi)
// ==========================================================================
const I18N = {
    en: {
        gov_dept:           'Kisan Kalyan & Krishi Vikas Dept, Govt. of MP',
        gov_zone:           'Minor Project • Malwa Plateau (Zone X)',
        tagline:            'AI-Powered Precision Agronomic Engine for Indore & Malwa',
        nav_advisor:        'Crop Advisor',
        nav_fert:           'Fertilizer Plan',
        nav_atlas:          'Indore Region',
        nav_history:        'History Ledger',
        hero_chip:          '🌾 Smart Agriculture & Precision Agronomy',
        hero_title:         'Tailored Crop Intelligence for <span class="highlight-text">Indore & Malwa\'s</span> Black Soils',
        hero_desc:          'Leverage Scikit-Learn Machine Learning & verified ICAR-IISR Indore agronomic standards for Malwa\'s Vertisols to optimize yield, soil health, and farm profitability.',
        soil_title:         'Soil & Climate Details',
        soil_desc:          'Enter soil test values or select your tehsil for verified baselines.',
        tehsil_label:       'Select Tehsil',
        season_label:       'Agricultural Season',
        land_label:         'Land Area (Acres)',
        farmer_name_label:  'Farmer Name',
        village_label:      'Village',
        recommend_btn:      'Generate AI Crop & Fertilizer Recommendation',
        loading_title:      'Processing Agronomic Engine...',
        loading_text:       'Analyzing soil nutrient compatibility against ICAR-IISR standards',
        empty_title:        'Ready for Agronomic Advisory',
        empty_desc:         'Select your Tehsil preset or adjust soil sliders on the left, then click "Generate AI Recommendation".',
        result_title:       'Recommended Crop',
        confidence_label:   'Model Confidence',
        alt_label:          'Viable Crop Alternatives',
        fert_title:         'Nutrient Plan (ICAR Dosage)',
        history_title:      'Consultation Ledger & Database',
        history_desc:       'Records persisted across consultations in MongoDB database.',
    },
    hi: {
        gov_dept:           'किसान कल्याण एवं कृषि विकास विभाग, म.प्र. शासन',
        gov_zone:           'माइनर प्रोजेक्ट • मालवा पठार (जोन X)',
        tagline:            'इंदौर एवं मालवा के लिए एआई-सटीक कृषि अनुशंसा प्रणाली',
        nav_advisor:        'फसल परामर्श',
        nav_fert:           'उर्वरक योजना',
        nav_atlas:          'इंदौर क्षेत्र',
        nav_history:        'इतिहास बहीखाता',
        hero_chip:          '🌾 स्मार्ट कृषि एवं सटीक तकनीक',
        hero_title:         'इंदौर एवं मालवा की <span class="highlight-text">काली मिट्टी</span> के लिए सटीक फसल परामर्श',
        hero_desc:          'आईसीएआर-आईआईएसआर इंदौर एवं मशीन लर्निंग द्वारा मालवा की काली मिट्टी के अनुकूल फसलों एवं उर्वरकों की सटीक वैज्ञानिक अनुशंसा प्राप्त करें।',
        soil_title:         'मिट्टी एवं जलवायु विवरण',
        soil_desc:          'मृदा स्वास्थ्य कार्ड अनुसार मान दर्ज करें या प्रमाणित तहसील चुनें।',
        tehsil_label:       'अपनी तहसील चुनें',
        season_label:       'कृषि मौसम',
        land_label:         'भूमि क्षेत्रफल (एकड़)',
        farmer_name_label:  'किसान का नाम',
        village_label:      'गाँव',
        recommend_btn:      'एआई फसल एवं खाद अनुशंसा प्राप्त करें',
        loading_title:      'कृषि विज्ञान इंजन विश्लेषण कर रहा है...',
        loading_text:       'मृदा पोषक तत्वों की जांच आईसीएआर-आईआईएसआर मानकों अनुसार जारी है',
        empty_title:        'परामर्श हेतु तैयार',
        empty_desc:         'बाईं ओर तहसील चुनें या स्लाइडर्स को सेट करें, फिर अनुशंसा बटन दबाएं।',
        result_title:       'अनुशंसित सर्वश्रेष्ठ फसल',
        confidence_label:   'मॉडल विश्वास स्तर',
        alt_label:          'अन्य उपयुक्त फसल विकल्प',
        fert_title:         'उर्वरक खुराक (आईसीएआर मानक)',
        history_title:      'परामर्श इतिहास एवं डेटाबेस',
        history_desc:       'मोंगोडीबी (MongoDB) डेटाबेस में सहेजे गए परामर्श रिकॉर्ड।',
    }
};

let currentLang = localStorage.getItem('agrosense_lang') || 'en';

// Crop Icons and Descriptions for visual polish
const CROP_METADATA = {
    'Soybean': {
        icon: '🌱',
        desc: 'Ideal legume for Indore deep black Vertisols with good monsoon drainage. Fixes atmospheric nitrogen.'
    },
    'Maize (Corn)': {
        icon: '🌽',
        desc: 'High cereal feeder for Kharif. Requires good nitrogen balance and fertile well-drained soil.'
    },
    'Wheat': {
        icon: '🌾',
        desc: 'Major Malwa Rabi staple. Thrives in moderate-to-high nitrogen with cool winter temperatures.'
    },
    'Gram (Chickpea)': {
        icon: '🧆',
        desc: 'High-value Malwa pulse. Requires minimal synthetic nitrogen; thrives in Vertisol moisture retention.'
    },
    'Onion': {
        icon: '🧅',
        desc: 'Commercial bulb crop. Heavy potassium consumer; requires light, well-tilled soil.'
    },
    'Potato': {
        icon: '🥔',
        desc: 'Tuber cash crop prominent in Mhow/Malwa ridge. Demands balanced phosphorus and potash.'
    }
};

// ==========================================================================
// 2. VERIFIED TEHSIL PRESETS (NASA POWER 5-Year Climatology Averages)
// ==========================================================================
const TEHSIL_CLIMATE = {
    'Indore': {
        'Kharif': { N: 45, P: 35, K: 50, ph: 7.6, temperature: 28.5, humidity: 78, rainfall: 920 },
        'Rabi':   { N: 60, P: 40, K: 55, ph: 7.7, temperature: 19.8, humidity: 52, rainfall: 40  }
    },
    'Sanwer': {
        'Kharif': { N: 42, P: 32, K: 48, ph: 7.7, temperature: 28.1, humidity: 75, rainfall: 890 },
        'Rabi':   { N: 55, P: 38, K: 50, ph: 7.8, temperature: 19.4, humidity: 50, rainfall: 35  }
    },
    'Depalpur': {
        'Kharif': { N: 48, P: 36, K: 52, ph: 7.5, temperature: 28.3, humidity: 74, rainfall: 880 },
        'Rabi':   { N: 58, P: 42, K: 54, ph: 7.6, temperature: 20.1, humidity: 51, rainfall: 35  }
    },
    'Mhow': {
        'Kharif': { N: 40, P: 38, K: 55, ph: 7.4, temperature: 27.9, humidity: 80, rainfall: 960 },
        'Rabi':   { N: 55, P: 45, K: 60, ph: 7.5, temperature: 18.9, humidity: 55, rainfall: 45  }
    },
    'Hatod': {
        'Kharif': { N: 44, P: 34, K: 48, ph: 7.6, temperature: 28.4, humidity: 73, rainfall: 870 },
        'Rabi':   { N: 58, P: 38, K: 52, ph: 7.7, temperature: 20.3, humidity: 49, rainfall: 30  }
    }
};

// ==========================================================================
// 3. UI CONTROLLER: SLIDERS & PRESETS
// ==========================================================================
function updateSlider(param, value) {
    const el = document.getElementById(param.toLowerCase() + '-val');
    if (el) el.textContent = value;
}

function applyTehsilPreset() {
    const tehsil = document.getElementById('tehsil').value || 'Indore';
    const season = document.getElementById('season').value || 'Kharif';

    const baseline = TEHSIL_CLIMATE[tehsil] && TEHSIL_CLIMATE[tehsil][season];
    if (!baseline) return;

    // Apply baseline values to sliders
    Object.entries(baseline).forEach(([key, val]) => {
        const slider = document.getElementById('slider-' + key);
        if (slider) {
            slider.value = val;
            updateSlider(key, val);
        }
    });
}

function quickSelectTehsil(tehsil, season) {
    const tehsilSelect = document.getElementById('tehsil');
    const seasonSelect = document.getElementById('season');

    if (tehsilSelect) tehsilSelect.value = tehsil;
    if (seasonSelect) seasonSelect.value = season;

    applyTehsilPreset();

    // Smooth-scroll to advisor section
    const advisor = document.getElementById('advisor');
    if (advisor) {
        advisor.scrollIntoView({ behavior: 'smooth' });
    }
}

// ==========================================================================
// 4. API INTEGRATION: RECOMMENDATION ENGINE
// ==========================================================================
async function getRecommendation() {
    const landArea = parseFloat(document.getElementById('land-area').value) || 1.0;

    const payload = {
        N:           parseFloat(document.getElementById('slider-N').value),
        P:           parseFloat(document.getElementById('slider-P').value),
        K:           parseFloat(document.getElementById('slider-K').value),
        ph:          parseFloat(document.getElementById('slider-ph').value),
        temperature: parseFloat(document.getElementById('slider-temperature').value),
        humidity:    parseFloat(document.getElementById('slider-humidity').value),
        rainfall:    parseFloat(document.getElementById('slider-rainfall').value),
        tehsil:      document.getElementById('tehsil').value || 'Indore',
        season:      document.getElementById('season').value || 'Kharif',
        land_area:   landArea,
        farmer_name: document.getElementById('farmer-name').value.trim() || 'Farmer Guest',
        village:     document.getElementById('farmer-village').value.trim() || ''
    };

    // UI state: Show loading spinner
    document.getElementById('empty-state').classList.add('hidden');
    document.getElementById('result-area').classList.add('hidden');
    document.getElementById('loading').classList.remove('hidden');

    try {
        const response = await fetch('/api/recommend', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        if (data.success) {
            renderResults(data, landArea);
            loadHistory(); // Refresh history table automatically
        } else {
            alert('Recommendation Error: ' + (data.error || 'Server error occurred.'));
        }
    } catch (err) {
        console.error('Fetch error:', err);
        alert('Could not connect to AgroSense backend. Ensure server is running.');
    } finally {
        document.getElementById('loading').classList.add('hidden');
    }
}

// Render Results on the right panel
function renderResults(data, landArea) {
    const recs = data.recommendations;
    const fert = data.fertilizer_plan;
    const top = recs[0];

    const meta = CROP_METADATA[top.crop] || { icon: '🌱', desc: 'Suitable for regional black soil conditions.' };

    // Primary crop info
    document.getElementById('crop-avatar').textContent = meta.icon;
    document.getElementById('primary-crop-name').textContent = top.crop;
    document.getElementById('primary-crop-subtext').textContent = meta.desc;
    document.getElementById('primary-confidence').textContent = top.confidence + '%';
    document.getElementById('confidence-fill').style.width = top.confidence + '%';
    document.getElementById('primary-msp').textContent = 'MSP: ' + (top.msp || '₹4,892/q');

    // Alternatives list
    const altContainer = document.getElementById('alt-crops-list');
    altContainer.innerHTML = '';
    recs.slice(1, 3).forEach(r => {
        const altMeta = CROP_METADATA[r.crop] || { icon: '🌿' };
        const card = document.createElement('div');
        card.className = 'alt-card';
        card.innerHTML = `
            <span class="alt-crop-title">${altMeta.icon} ${r.crop}</span>
            <span class="alt-conf-tag">${r.confidence}% Match</span>
        `;
        altContainer.appendChild(card);
    });

    // Fertilizer plan scaled to farmer's acreage
    const perAcre = fert.per_acre || fert;
    const totalFarm = fert.total_farm || {
        urea_total_kg: Math.round(perAcre.urea_kg * landArea * 10) / 10,
        dap_total_kg:  Math.round(perAcre.dap_kg * landArea * 10) / 10,
        mop_total_kg:  Math.round(perAcre.mop_kg * landArea * 10) / 10,
        organic_ton:   Math.round((perAcre.organic_ton || 2.0) * landArea * 10) / 10
    };

    document.getElementById('fert-acre-tag').textContent = `Total for ${landArea} Acre${landArea > 1 ? 's' : ''}`;

    const fertGrid = document.getElementById('fert-grid');
    fertGrid.innerHTML = `
        <div class="fert-item">
            <div class="fert-name">Urea (46% N)</div>
            <div class="fert-val">${totalFarm.urea_total_kg}</div>
            <div class="fert-unit">kg total (${perAcre.urea_kg} kg/ac)</div>
        </div>
        <div class="fert-item">
            <div class="fert-name">DAP (18:46:0)</div>
            <div class="fert-val">${totalFarm.dap_total_kg}</div>
            <div class="fert-unit">kg total (${perAcre.dap_kg} kg/ac)</div>
        </div>
        <div class="fert-item">
            <div class="fert-name">MOP (60% K)</div>
            <div class="fert-val">${totalFarm.mop_total_kg}</div>
            <div class="fert-unit">kg total (${perAcre.mop_kg} kg/ac)</div>
        </div>
        <div class="fert-item">
            <div class="fert-name">Compost</div>
            <div class="fert-val">${totalFarm.organic_ton}</div>
            <div class="fert-unit">tons (${perAcre.organic_ton || 2.0} t/ac)</div>
        </div>
    `;

    document.getElementById('fert-remarks').innerHTML = `
        <i class="fa-solid fa-circle-info"></i> ${fert.remarks || perAcre.remarks || 'Apply DAP & MOP at sowing; split Urea in 2 top-dressings.'}
    `;

    document.getElementById('result-area').classList.remove('hidden');
}

// ==========================================================================
// 5. HISTORY & DATABASE LEDGER
// ==========================================================================
async function loadHistory() {
    const tbody = document.getElementById('history-tbody');
    try {
        const res = await fetch('/api/history');
        const data = await res.json();

        if (data.success && data.data && data.data.length > 0) {
            tbody.innerHTML = '';
            data.data.forEach(item => {
                const tr = document.createElement('tr');
                const dateStr = item.created_at ? new Date(item.created_at).toLocaleDateString('en-IN', {
                    day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit'
                }) : 'Just now';

                const soil = item.soil_inputs || {};
                const soilStr = `N:${soil.N || '-'} P:${soil.P || '-'} K:${soil.K || '-'} pH:${soil.ph || '-'}`;

                tr.innerHTML = `
                    <td>${dateStr}</td>
                    <td><strong>${item.farmer_name || 'Farmer Guest'}</strong><br><small style="color:var(--text-muted)">${item.farmer_village || 'Indore District'}</small></td>
                    <td>${item.tehsil || 'Indore'}</td>
                    <td>${item.land_area ? item.land_area + ' ac' : '1.0 ac'}</td>
                    <td><code>${soilStr}</code></td>
                    <td><strong style="color:var(--primary)">${item.primary_crop}</strong></td>
                    <td><span class="val-badge">${item.confidence}%</span></td>
                `;
                tbody.appendChild(tr);
            });
        } else {
            tbody.innerHTML = `
                <tr>
                    <td colspan="7" class="table-loading">No past consultations yet. Generate your first recommendation above!</td>
                </tr>
            `;
        }
    } catch (err) {
        tbody.innerHTML = `
            <tr>
                <td colspan="7" class="table-loading" style="color:#ef4444;">Could not load history from database.</td>
            </tr>
        `;
    }
}

// Check MongoDB status
async function checkDBStatus() {
    const badge = document.getElementById('db-status-badge');
    try {
        const res = await fetch('/api/status');
        const data = await res.json();
        if (data.success && data.database) {
            if (data.database.connected) {
                badge.innerHTML = `<i class="fa-solid fa-circle-check" style="color:#10b981;"></i> MongoDB: Connected`;
            } else {
                badge.innerHTML = `<i class="fa-solid fa-shield-halved" style="color:#f59e0b;"></i> Resilient In-Memory Buffer`;
            }
        }
    } catch (e) {
        badge.innerHTML = `<i class="fa-solid fa-circle-info"></i> Server Connecting...`;
    }
}

// ==========================================================================
// 6. THEME & LANGUAGE CONTROLLER
// ==========================================================================
function toggleTheme() {
    const html = document.documentElement;
    const current = html.getAttribute('data-theme') || 'dark';
    const next = current === 'dark' ? 'light' : 'dark';

    html.setAttribute('data-theme', next);
    localStorage.setItem('agrosense_theme', next);

    const themeLabel = document.getElementById('theme-label');
    const themeIcon = document.getElementById('theme-icon');

    if (next === 'light') {
        if (themeLabel) themeLabel.textContent = 'Dark Mode';
        if (themeIcon) themeIcon.className = 'fa-solid fa-moon';
    } else {
        if (themeLabel) themeLabel.textContent = 'Light Mode';
        if (themeIcon) themeIcon.className = 'fa-solid fa-sun';
    }
}

function toggleLanguage() {
    currentLang = currentLang === 'en' ? 'hi' : 'en';
    localStorage.setItem('agrosense_lang', currentLang);
    applyLanguage();
}

function applyLanguage() {
    const langBtn = document.getElementById('lang-label');
    if (langBtn) {
        langBtn.textContent = currentLang === 'en' ? 'हिंदी' : 'English';
    }

    const dict = I18N[currentLang];
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (dict[key]) {
            el.innerHTML = dict[key];
        }
    });
}

// ==========================================================================
// 7. INITIALIZATION ON PAGE LOAD
// ==========================================================================
window.addEventListener('DOMContentLoaded', () => {
    applyLanguage();
    applyTehsilPreset();
    loadHistory();
    checkDBStatus();
});
