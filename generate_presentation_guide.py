"""
================================================================================
SCRIPT: generate_presentation_guide.py
PROJECT: AgroSense Indore (Simple Edition)
PURPOSE: Generates the official presentation guide & viva preparation PDF
         with balanced 5-page layout, complete team scripts, architecture
         breakdowns, model efficiency analysis, mathematical formulas,
         and master examiner Q&A defense.
================================================================================
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

PDF_PATH = "AgroSense_Indore_Simple_Presentation_Guide.pdf"

# Numbered canvas for total page count & running headers/footers
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#64748b"))

        # Running Top Header (pages 2+)
        if self._pageNumber > 1:
            self.drawString(36, 755, "AGROSENSE INDORE (SIMPLE EDITION) — MINOR PROJECT VIVA GUIDE")
            self.drawRightString(576, 755, "DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING")
            self.setStrokeColor(colors.HexColor("#cbd5e1"))
            self.setLineWidth(0.5)
            self.line(36, 748, 576, 748)

        # Running Bottom Footer
        self.setFont("Helvetica", 8)
        self.drawString(36, 22, "Academic Minor Project Presentation • Precision Agronomic Engine • Indore Vertisols Zone X")
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(576, 22, page_text)
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(36, 30, 576, 30)

        self.restoreState()


def build_pdf():
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=40,
        bottomMargin=38
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#065f46'),
        spaceAfter=3
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor('#059669'),
        spaceAfter=8
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=colors.HexColor('#0f172a'),
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#065f46'),
        spaceBefore=5,
        spaceAfter=2,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.2,
        leading=11.2,
        textColor=colors.HexColor('#1e293b'),
        spaceAfter=4
    )

    body_bold = ParagraphStyle(
        'Body_Bold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor('#0f172a')
    )

    quote_style = ParagraphStyle(
        'Quote_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=7.8,
        leading=10.8,
        textColor=colors.HexColor('#065f46'),
        backColor=colors.HexColor('#ecfdf5'),
        borderColor=colors.HexColor('#a7f3d0'),
        borderWidth=0.8,
        borderPadding=5,
        spaceBefore=2,
        spaceAfter=5
    )

    story = []

    # =========================================================================
    # PAGE 1: COVER & EXECUTIVE SUMMARY + TEAM OVERVIEW + LUV (FRONTEND)
    # =========================================================================
    story.append(Paragraph("🌾 AGROSENSE INDORE (SIMPLE EDITION)", title_style))
    story.append(Paragraph("Comprehensive Project Presentation, Architecture & Viva Defense Guide", subtitle_style))
    story.append(Paragraph(
        "<b>Project Focus:</b> Precision AI Crop & Fertilizer Advisory Engine for Indore District (Malwa Zone X Vertisols)<br/>"
        "<b>Full Stack:</b> Vanilla HTML/CSS/JS (Bilingual & Dark Mode) • Node.js Express REST API • MongoDB NoSQL (Resilient Memory Buffer) • Scikit-Learn Random Forest Classifier (80.0% Accuracy) • NASA POWER Satellite Climatology & ICAR-IISR Indore Agronomic Rules",
        body_style
    ))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#10b981'), spaceBefore=5, spaceAfter=8))

    story.append(Paragraph("1. Team Roles & Module Ownership", h1_style))
    roles_data = [
        [Paragraph("<b>Member</b>", body_bold), Paragraph("<b>Domain & Responsibility</b>", body_bold), Paragraph("<b>Core Source Files</b>", body_bold), Paragraph("<b>Key Demo Action</b>", body_bold)],
        [
            Paragraph("<b>Luv</b>", body_style),
            Paragraph("Frontend & UI Engineering (HTML, CSS, JS, Themes, Bilingual)", body_style),
            Paragraph("<code>frontend/index.html</code><br/><code>frontend/style.css</code><br/><code>frontend/app.js</code>", code_style),
            Paragraph("Live slider demo, theme toggle, Hindi switch, atlas presets", body_style)
        ],
        [
            Paragraph("<b>Kunal</b>", body_style),
            Paragraph("Backend Architecture & REST Services (Node.js & Express)", body_style),
            Paragraph("<code>backend/server.js</code><br/><code>backend/routes/api.js</code><br/><code>backend/package.json</code>", code_style),
            Paragraph("Show <code>/api/recommend</code>, input validation, land acreage scaling", body_style)
        ],
        [
            Paragraph("<b>Naman</b>", body_style),
            Paragraph("Database Persistence (MongoDB) & ML Inter-Process Bridge", body_style),
            Paragraph("<code>backend/database/</code><br/><code>backend/ml_service/ml_bridge.js</code><br/><code>predictor_service.py</code>", code_style),
            Paragraph("Explain Mongoose schema, resilient buffer, and Python IPC bridge", body_style)
        ],
        [
            Paragraph("<b>Arhaan</b>", body_style),
            Paragraph("System Architecture, DFD, ER & Database UML Modeling", body_style),
            Paragraph("<code>diagrams/Database-Architecture.xml</code><br/><code>System-Architecture.xml</code><br/><code>ER-Diagram.xml</code>, <code>DFD 0/1</code>", code_style),
            Paragraph("Walkthrough 3-Tier flow, DFD processes, and MongoDB collections", body_style)
        ],
        [
            Paragraph("<b>Kuldeep</b>", body_style),
            Paragraph("Data Pipeline (NASA & Govt), Dataset Gen & Model Training", body_style),
            Paragraph("<code>ml/step1_download_nasa_climate.py</code><br/><code>ml/step2_scrape_govt_data.py</code><br/><code>ml/build_dataset.py</code>, <code>train_...</code>", code_style),
            Paragraph("Explain 1,500 rows gen, NASA API parameters, 80.0% Random Forest", body_style)
        ],
    ]

    t_roles = Table(roles_data, colWidths=[65, 175, 155, 145])
    t_roles.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f1f5f9')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
    ]))
    story.append(t_roles)
    story.append(Spacer(1, 8))

    # LUV (FRONTEND)
    story.append(Paragraph("2. Member 1: Luv — Frontend & UI Engineering", h1_style))
    story.append(Paragraph(
        "\"I designed and developed the frontend user interface for AgroSense Indore. My goal was to make complex scientific agronomic decisions intuitive for both farmers and field officers. "
        "The interface is built using pure, high-performance HTML5, CSS3, and modern JavaScript without heavy client-side frameworks, ensuring instantaneous loading even on rural mobile connections. "
        "Key highlights include: an official MP Government banner, an instant English/Hindi bilingual toggle, a zero-flicker True-Black dark mode, real-time reactive sliders for 7 soil and climate parameters, "
        "and automated NASA climate presets for all 5 Indore tehsils. On submission, it renders the top recommended crop, match percentage bar, official MSP market rate, and an ICAR fertilizer schedule scaled to the farmer's acreage.\"",
        quote_style
    ))
    story.append(Paragraph(
        "• <b>Zero-Flicker Dark Mode:</b> In <code>frontend/index.html</code>, an inline script in <code>&lt;head&gt;</code> reads <code>localStorage</code> before body rendering.<br/>"
        "• <b>Real-Time Slider Sync:</b> In <code>frontend/app.js</code>, <code>updateSlider()</code> binds to the <code>oninput</code> event of range inputs to update numerical badges.<br/>"
        "• <b>Bilingual Engine:</b> In <code>frontend/app.js</code>, the <code>I18N</code> dictionary contains complete English and Hindi translations applied via <code>data-i18n</code>.<br/>"
        "• <b>Tehsil Presets:</b> In <code>frontend/app.js</code>, <code>applyTehsilPreset()</code> auto-populates seasonal NASA baseline averages for Indore, Sanwer, Depalpur, Mhow, Hatod.",
        body_style
    ))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: KUNAL (BACKEND) + NAMAN (DATABASE) + ARHAAN (ARCHITECTURE)
    # =========================================================================
    story.append(Paragraph("3. Member 2: Kunal — Backend Architecture & REST Services", h1_style))
    story.append(Paragraph(
        "\"I developed the server-side REST application using Node.js and Express. The backend acts as the central orchestrator connecting the browser client, Naman's database layer, and Kuldeep's machine learning model. "
        "I implemented modular routes for <code>/api/recommend</code>, <code>/api/history</code>, <code>/api/status</code>, and <code>/api/atlas</code>. "
        "The server validates incoming soil test numbers, converts inputs to numeric types, delegates inference to our ML service, maps official Government MSP price tags to each recommendation, "
        "and computes customized farm-wide fertilizer dosages scaled by land acreage. It also serves the frontend statically and includes CORS headers and environment-driven port configuration.\"",
        quote_style
    ))
    story.append(Paragraph(
        "• <b>Server Setup:</b> In <code>backend/server.js</code>, Express middleware handles CORS, <code>express.json()</code>, and mounts routes under <code>/api/</code>.<br/>"
        "• <b>Dosage Acreage Scaling:</b> In <code>backend/routes/api.js</code>, computes total farm fertilizer: <code>Total = Dose_per_acre * Farmer_Acreage</code>.<br/>"
        "• <b>MSP Integration:</b> Attaches current 2024-25 government minimum support prices (Soybean: ₹4,892/q, Wheat: ₹2,275/q, Gram: ₹5,440/q).<br/>"
        "• <b>Diagnostics:</b> <code>GET /api/status</code> provides live health status of the application and reports the active database engine.",
        body_style
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("4. Member 3: Naman — Database Persistence & ML Bridge", h1_style))
    story.append(Paragraph(
        "\"I architected the database layer using MongoDB NoSQL and engineered the inter-process ML bridge connecting Node.js with Python. "
        "Farmer consultation records are inherently hierarchical—each consultation contains multi-field soil readings, alternative crop predictions, and dynamic fertilizer dosage plans. "
        "Using Mongoose ODM, I created a strongly typed schema with subdocuments and B-Tree indexes on <code>created_at</code> and <code>tehsil</code> for rapid queries. "
        "To ensure zero downtime, I designed a resilient in-memory buffer fallback: if MongoDB is unreachable, the system automatically buffers consultations in RAM so farmers always receive advice. "
        "For ML integration, I developed <code>ml_bridge.js</code> using Node's <code>child_process.spawn</code> to execute <code>predictor_service.py</code> with JSON streaming and safety timeouts.\"",
        quote_style
    ))
    story.append(Paragraph(
        "• <b>Document Schema:</b> In <code>backend/database/models/Recommendation.js</code>, defined <code>SoilInputSchema</code> and <code>FertilizerPlanSchema</code> as subdocuments.<br/>"
        "• <b>Resilience Layer:</b> In <code>backend/database/mongodb_service.js</code>, if MongoDB connection fails within 4 seconds, operations redirect to <code>inMemoryHistory</code> (FIFO buffer of 50 records).<br/>"
        "• <b>ML Inter-Process Communication:</b> In <code>backend/ml_service/ml_bridge.js</code>, Node spawns Python, sends stringified JSON arguments, listens to <code>stdout</code>, and handles 5-second timeouts.<br/>"
        "• <b>Dosage Calculation:</b> In <code>backend/ml_service/predictor_service.py</code>, computes required nutrient gaps: <code>Need_N = max(0, Target_N - Soil_N)</code>, converting into DAP, Urea, and MOP.",
        body_style
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("5. Member 4: Arhaan — System Architecture & UML Modeling", h1_style))
    story.append(Paragraph(
        "\"I engineered the software architecture models, data flow specifications, and technical documentation following standard IEEE and UML guidelines. "
        "I created complete architectural diagrams in the <code>diagrams/</code> directory: the 3-Tier System Architecture, the Entity-Relationship (ER) model, Context Level DFD (Level 0), "
        "Detailed Process DFD (Level 1), the Use Case Model, and the MongoDB Database Architecture diagram. "
        "These models formalize how unstructured farmer inputs transition through validation, feature normalization, Scikit-Learn matrix inference, and persistence into our document store.\"",
        quote_style
    ))
    story.append(Paragraph(
        "• <b>Database Architecture XML:</b> In <code>diagrams/Database-Architecture.xml</code>, mapped Layer 1 (API Ingestion), Layer 2 (Mongoose ODM & Resilience Buffer), Layer 3 (MongoDB Collections & B-Tree Indexes).<br/>"
        "• <b>3-Tier Architecture:</b> Tier 1 (Client Browser / Responsive Web) $\\leftrightarrow$ Tier 2 (Express REST Controller) $\\leftrightarrow$ Tier 3 (Python Scikit-Learn & MongoDB).<br/>"
        "• <b>DFD Level 0 & Level 1:</b> Traced input data flow from Farmer through Process 1.0 (Validation), Process 2.0 (Model Prediction), Process 3.0 (Dosage Scaling), to Data Store D1 (Recommendations Ledger).<br/>"
        "• <b>ER Model:</b> Clarified entity cardinality: Farmer (1) $\\rightarrow$ submits $\\rightarrow$ Recommendation (N), Recommendation (1) $\\rightarrow$ contains $\\rightarrow$ Crop Prediction (1) and Fertilizer Advisory (1).",
        body_style
    ))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: KULDEEP (ML PIPELINE) + SECTION 7 (MODEL EFFICIENCY & TABLE)
    # =========================================================================
    story.append(Paragraph("6. Member 5: Kuldeep — ML Training, Data Pipeline & Cleaning", h1_style))
    story.append(Paragraph(
        "\"I engineered the machine learning pipeline, data sourcing scripts, and model training. Generic agricultural datasets from online repositories do not represent Indore's deep black Vertisols. "
        "I established a rigorous 4-step pipeline: (1) Downloaded 5 years of daily satellite climatological data from NASA POWER API across all 5 tehsils; (2) Scraped and extracted verified agronomic rules from ICAR-IISR Indore and RVSKVV Gwalior; "
        "(3) Synthesized a clean, balanced 1,500-sample dataset using numpy and pandas (250 rows each for 6 crops); (4) Benchmarked 4 classifiers using 5-fold Stratified Cross-Validation. "
        "Our Random Forest model achieved 80.00% test accuracy and an exceptional 96.1% F1-score on Soybean, our region's most vital cash crop.\"",
        quote_style
    ))
    story.append(Paragraph(
        "• <b>NASA Climate Script:</b> In <code>ml/step1_download_nasa_climate.py</code>, queries satellite parameters: <code>T2M</code> (temperature), <code>RH2M</code> (relative humidity), and <code>PRECTOTCORR</code> (precipitation).<br/>"
        "• <b>Government Provenance:</b> In <code>ml/step2_scrape_govt_data.py</code>, documents guidelines from ICAR-IISR (Soybean 25:60:40 NPKS), RVSKVV Malwa wheat guide, and GOI Soil Health Card ratings.<br/>"
        "• <b>Dataset Synthesis:</b> In <code>ml/build_dataset.py</code>, generates 1,500 balanced rows with Gaussian micro-climate noise anchored strictly in Indore district Vertisol pH (6.8–8.2).<br/>"
        "• <b>Training & Serialization:</b> In <code>ml/train_indore_model.py</code>, trains 200 decision trees with max depth 14 and exports artifact to <code>models/indore_crop_model.pkl</code>.",
        body_style
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph("7. Model Efficiency Analysis & Performance Metrics", h1_style))
    story.append(Paragraph(
        "<b>Core Question: What is our model efficiency, and how was it calculated?</b><br/>"
        "Our multi-class model was evaluated on a 20% holdout test set (300 unseen samples, exactly 50 per crop) and verified via 5-Fold Stratified Cross-Validation:",
        body_style
    ))

    metrics_table_data = [
        [Paragraph("<b>Metric Name</b>", body_bold), Paragraph("<b>Score / Value</b>", body_bold), Paragraph("<b>Technical Meaning & Interpretation</b>", body_bold)],
        [
            Paragraph("<b>Overall Test Accuracy</b>", body_style),
            Paragraph("<b>80.00%</b>", body_style),
            Paragraph("240 out of 300 unseen holdout test samples classified correctly across 6 competing crops.", body_style)
        ],
        [
            Paragraph("<b>5-Fold Stratified CV</b>", body_style),
            Paragraph("<b>79.00% ± 2.34%</b>", body_style),
            Paragraph("Evaluated across 5 independent dataset splits. Low std dev (±2.34%) confirms stability and zero overfitting.", body_style)
        ],
        [
            Paragraph("<b>Weighted F1-Score</b>", body_style),
            Paragraph("<b>0.7967</b> (~80%)", body_style),
            Paragraph("Harmonic mean balancing precision and recall across all crop categories.", body_style)
        ],
        [
            Paragraph("<b>Soybean F1-Score</b>", body_style),
            Paragraph("<b>96.08%</b>", body_style),
            Paragraph("Near-perfect classification for Indore's principal Kharif cash crop (Precision: 94.2%, Recall: 98.0%).", body_style)
        ],
        [
            Paragraph("<b>Maize F1-Score</b>", body_style),
            Paragraph("<b>95.92%</b>", body_style),
            Paragraph("Precision: 97.9%, Recall: 94.0%. Clean boundary separation from pulse crops.", body_style)
        ],
        [
            Paragraph("<b>Wheat F1-Score</b>", body_style),
            Paragraph("<b>82.22%</b>", body_style),
            Paragraph("Indore's dominant Rabi cereal. High precision (92.5%) prevents incorrect winter recommendations.", body_style)
        ],
        [
            Paragraph("<b>Gram F1-Score</b>", body_style),
            Paragraph("<b>80.73%</b>", body_style),
            Paragraph("High-value pulse crop (Precision: 74.6%, Recall: 88.0%). Reliably captures pulse soil conditions.", body_style)
        ],
        [
            Paragraph("<b>Potato F1-Score</b>", body_style),
            Paragraph("<b>66.67%</b>", body_style),
            Paragraph("Precision: 56.2%, Recall: 82.0%. Tuber crop tailored for high phosphorus & potash in Mhow ridge.", body_style)
        ],
        [
            Paragraph("<b>Onion F1-Score</b>", body_style),
            Paragraph("<b>56.41%</b>", body_style),
            Paragraph("Precision: 78.6%, Recall: 44.0%. Conservative commercial bulb crop; high potash requirement.", body_style)
        ],
    ]

    t_metrics = Table(metrics_table_data, colWidths=[120, 95, 325])
    t_metrics.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f1f5f9')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_metrics)

    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: MATHEMATICAL FORMULAS + CONFUSION MATRIX
    # =========================================================================
    story.append(Paragraph("8. Exact Mathematical Formulas & Confusion Matrix", h1_style))
    story.append(Paragraph(
        "Examiners frequently evaluate whether students understand the exact mathematics behind machine learning metrics:",
        body_style
    ))

    formula_data = [
        [
            Paragraph("<b>Metric</b>", body_bold),
            Paragraph("<b>Mathematical Formula</b>", body_bold),
            Paragraph("<b>Calculation on AgroSense Model</b>", body_bold)
        ],
        [
            Paragraph("<b>Accuracy</b>", body_style),
            Paragraph("<code>Accuracy = (TP + TN) / (TP + TN + FP + FN)</code>", code_style),
            Paragraph("<code>240 correct / 300 total = 0.8000 (80.0%)</code>", body_style)
        ],
        [
            Paragraph("<b>Precision</b>", body_style),
            Paragraph("<code>Precision = TP / (TP + FP)</code>", code_style),
            Paragraph("Soybean: <code>49 / (49 + 3) = 94.23%</code><br/>Maize: <code>47 / (47 + 1) = 97.92%</code>", body_style)
        ],
        [
            Paragraph("<b>Recall (Sensitivity)</b>", body_style),
            Paragraph("<code>Recall = TP / (TP + FN)</code>", code_style),
            Paragraph("Soybean: <code>49 / (49 + 1) = 98.00%</code><br/>Maize: <code>47 / (47 + 3) = 94.00%</code>", body_style)
        ],
        [
            Paragraph("<b>F1-Score</b>", body_style),
            Paragraph("<code>F1 = 2 * (Precision * Recall) / (Precision + Recall)</code>", code_style),
            Paragraph("Harmonic mean balancing precision and recall. Soybean: <code>96.08%</code>; Maize: <code>95.92%</code>", body_style)
        ],
        [
            Paragraph("<b>5-Fold Stratified Cross-Validation</b>", body_style),
            Paragraph("<code>Mean = (1/K) * Σ Score_k<br/>StdDev = sqrt((1/K) * Σ (Score_k - Mean)^2)</code>", code_style),
            Paragraph("Dataset partitioned into K=5 stratified folds (240 samples each). Mean = <code>79.00% ± 2.34%</code>.", body_style)
        ]
    ]

    t_formulas = Table(formula_data, colWidths=[100, 200, 240])
    t_formulas.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f1f5f9')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
    ]))
    story.append(t_formulas)
    story.append(Spacer(1, 8))

    story.append(Paragraph("Confusion Matrix Breakdown (300 Test Samples, 50 per Class)", h2_style))
    story.append(Paragraph("Rows represent Actual Ground Truth crops; Columns represent Predicted crops. The diagonal contains True Positives (TP):", body_style))

    cm_data = [
        [Paragraph("<b>Actual \\ Predicted</b>", body_bold), Paragraph("<b>Gram</b>", body_bold), Paragraph("<b>Maize</b>", body_bold), Paragraph("<b>Onion</b>", body_bold), Paragraph("<b>Potato</b>", body_bold), Paragraph("<b>Soybean</b>", body_bold), Paragraph("<b>Wheat</b>", body_bold), Paragraph("<b>Total</b>", body_bold)],
        [Paragraph("<b>Gram (Chickpea)</b>", body_style), "<b>44</b> (TP)", "0", "4", "2", "0", "0", "50"],
        [Paragraph("<b>Maize (Corn)</b>", body_style), "0", "<b>47</b> (TP)", "0", "0", "3", "0", "50"],
        [Paragraph("<b>Onion</b>", body_style), "7", "0", "<b>22</b> (TP)", "18", "0", "3", "50"],
        [Paragraph("<b>Potato</b>", body_style), "8", "0", "1", "<b>41</b> (TP)", "0", "0", "50"],
        [Paragraph("<b>Soybean</b>", body_style), "0", "1", "0", "0", "<b>49</b> (TP)", "0", "50"],
        [Paragraph("<b>Wheat</b>", body_style), "0", "0", "1", "12", "0", "<b>37</b> (TP)", "50"],
    ]

    t_cm = Table(cm_data, colWidths=[120, 60, 60, 60, 60, 60, 60, 60])
    t_cm.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f1f5f9')),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('BACKGROUND', (1, 1), (1, 1), colors.HexColor('#dcfce7')),
        ('BACKGROUND', (2, 2), (2, 2), colors.HexColor('#dcfce7')),
        ('BACKGROUND', (3, 3), (3, 3), colors.HexColor('#dcfce7')),
        ('BACKGROUND', (4, 4), (4, 4), colors.HexColor('#dcfce7')),
        ('BACKGROUND', (5, 5), (5, 5), colors.HexColor('#dcfce7')),
        ('BACKGROUND', (6, 6), (6, 6), colors.HexColor('#dcfce7')),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(t_cm)
    story.append(Paragraph("<b>Diagonal Sum (Correct Predictions):</b> 44 + 47 + 22 + 41 + 49 + 37 = <b>240 / 300 = 80.00% Overall Accuracy</b>.", body_style))
    story.append(Paragraph(
        "<b>Why 80% is high performance:</b> In a 6-class problem, pure random guessing gives 16.6% accuracy (1/6). 80% is nearly <b>5x better than chance</b>. "
        "More importantly, for Indore's principal cash crops (Soybean and Maize), accuracy exceeds 95%. Crops like Onion and Potato share tuber/bulb nutrient profiles (high potash/phosphorus), which natural agronomic overlap accounts for.",
        body_style
    ))

    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: MASTER VIVA QUESTIONS & DEFENSE CHEATSHEET
    # =========================================================================
    story.append(Paragraph("9. Master Viva Defense Questions & Answers", h1_style))
    story.append(Paragraph("Rehearse these 6 standard examiner questions to defend the technical implementation with full confidence:", body_style))

    qas = [
        (
            "Q1: Why did you pick Random Forest over Decision Tree or Deep Learning?",
            "Answer: A single Decision Tree achieved only 76.3% accuracy because individual trees easily overfit noisy soil readings. Random Forest trains 200 diverse trees using bootstrap aggregation (bagging), drastically reducing variance. Deep Learning (ANN/MLP) requires tens of thousands of rows and acts as an uninterpretable black box. Random Forest provides probabilistic confidence outputs that directly fit our advisory interface."
        ),
        (
            "Q2: Why MongoDB over MySQL for storing consultations?",
            "Answer: Consultations have a document-centric, polymorphic shape: each record contains nested subdocuments for soil test values, alternative crop arrays, and fertilizer schedules. In relational MySQL, this requires 3 normalized tables with foreign keys and multi-table JOIN queries. MongoDB stores the entire consultation as a single atomic BSON document, delivering faster read/write speeds and schema flexibility."
        ),
        (
            "Q3: What happens if MongoDB daemon crashes during a farmer's live consultation?",
            "Answer: Our backend features an automated In-Memory Buffer fallback in `mongodb_service.js`. If MongoDB becomes unreachable, the server continues processing recommendations without crashing and saves records in a circular RAM cache (up to 50 records), guaranteeing zero service interruption for farmers."
        ),
        (
            "Q4: How is fertilizer dosage computed?",
            "Answer: We use ICAR-IISR nutrient balance formulas: DAP is applied first to satisfy Phosphorus demand ($P_2O_5 / 0.46$). Because DAP also contains 18% Nitrogen, we subtract the DAP nitrogen contribution from total nitrogen demand, and fulfill the remainder with Urea ($N_{rem} / 0.46$). Potassium is satisfied with MOP ($K_2O / 0.60$). All values are scaled by farmer land acreage."
        ),
        (
            "Q5: How did you ensure data provenance without access to thousands of manual soil samples?",
            "Answer: We constructed a semi-synthetic dataset where the boundaries are 100% verified real data: climate averages come from 5 years of daily satellite readings from NASA POWER API, soil parameters are anchored in Government of India Soil Health Card Vertisol baselines (pH 6.8–8.2), and crop assignments are governed by ICAR-IISR and RVSKVV agricultural packages."
        ),
        (
            "Q6: How does Node.js communicate with Python?",
            "Answer: We use standard inter-process communication (IPC) via `child_process.spawn`. Node writes the input JSON as process arguments, and reads Python's prediction output through standard output (`stdout`). A safety timer ensures that if Python hangs, a fallback answer is returned within 5 seconds."
        ),
    ]

    for q, a in qas:
        story.append(Paragraph(f"<b>{q}</b>", body_bold))
        story.append(Paragraph(a, body_style))
        story.append(Spacer(1, 3))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"\n[SUCCESS] Generated Presentation Guide PDF: {PDF_PATH}\n")

if __name__ == '__main__':
    build_pdf()
