
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge, Circle
from datetime import datetime, timedelta
import textwrap
import io

# ============================
# 🎯 Page Config & Theming
# ============================
st.set_page_config(
    page_title="NovoFertiScan",
    layout="wide",
    page_icon=r"C:\Users\Rishika Saha\Downloads\Minor Project Sem 9\NovoFertiScan\Logo.png",
    initial_sidebar_state="expanded",
)


CUSTOM_CSS = """
<style>
:root { 
--card-bg: #ffffff; 
--card-br: 14px; 
--soft-shadow: 0 6px 18px rgba(0,0,0,.06); 
--accent: #6366f1; 
--accent-light: #eef2ff; 
--text-dark: #0f172a; 
--text-muted: #475569; 
}

/***** Layout *****/
.block-container {padding-top: 1.3rem;}

/***** Titles *****/
.huge-title { 
font-size: 2.1rem; 
font-weight: 800; 
color: var(--text-dark) !important; 
letter-spacing: -0.5px;
}
.subtitle { 
color: var(--text-muted) !important; 
font-size: 1.05rem; 
}

/***** Cards *****/
.card { 
background: var(--card-bg); 
border-radius: var(--card-br); 
padding: 1.2rem 1.4rem; 
box-shadow: var(--soft-shadow); 
border: 1px solid #eef2f7; 
transition: all .25s ease;
}
.card:hover { 
transform: translateY(-3px); 
box-shadow: 0 10px 24px rgba(0,0,0,.08); 
}

/***** Pills & Badges *****/
.pill { 
display:inline-block; 
padding:.25rem .7rem; 
border-radius:999px; 
background:#f8fafc; 
border:1px solid #e2e8f0; 
margin:.15rem .3rem; 
font-size:.85rem; 
font-weight:500;
}
.badge { 
font-weight:600; 
padding:.3rem .6rem; 
border-radius:8px; 
background: var(--accent-light); 
color: #3730a3; 
border:1px solid #e0e7ff; 
}
.badge-gradient {
background: linear-gradient(90deg, #6366f1, #818cf8);
color: white;
border: none;
}

/***** KPIs *****/
.kpi { 
display:flex; 
align-items:center; 
justify-content:space-between; 
padding:.7rem 1rem; 
border:1px dashed #e5e7eb; 
border-radius:12px; 
background: #fafafa;
}
.kpi .value { font-weight:800; font-size:1.15rem; }

/***** Status Colors *****/
.warn { color: #b91c1c; font-weight:700; }
.ok { color: #065f46; font-weight:700; }
.small { font-size:0.9rem; color:var(--text-muted); }

/***** Footer Note *****/
.footer-note { color:#6b7280; font-size:.85rem; }

/***** Responsive *****/
@media (max-width: 640px) {
.card { padding: 1rem; }
.huge-title { font-size: 1.7rem; }
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

import base64
from PIL import Image
import streamlit as st

import base64
import streamlit as st

# =========================
# Logo + Title Card Header
# =========================
logo_path = r"C:\Users\Rishika Saha\Downloads\Minor Project Sem 9\NovoFertiScan\Logo.png"

# Convert image to base64
with open(logo_path, "rb") as f:
    img_base64 = base64.b64encode(f.read()).decode()

st.markdown(
    f"""
    <div class="card" style="display:flex; align-items:flex-start; margin-bottom:20px;">
        <img src="data:image/png;base64,{img_base64}" width="100" 
             style="margin-right:20px; margin-top:5px;">
        <div style="flex:1; min-width:0;">
            <div style="font-size:32px; font-weight:700; color:#1a1a1a; margin-bottom:8px;">
                NovoFerti-Scan — Infertility Diagnostic Tool
            </div>
            <div style="font-size:16px; line-height:1.6; color:#444;">
                NovoFerti-Scan is a next-generation infertility diagnostic platform combining clinical notes, 
                hormonal profiles, and transcriptomic data analysis to uncover underlying molecular mechanisms. 
                It integrates gene expression insights, predictive risk scoring, and evidence-based recommendations, 
                delivering personalized guidance on tests, treatments, and clinical decision-making for reproductive health.
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================
# Clinical ranges & gene extras
# ============================

NORMAL_RANGES = {
    "FSH_day3": (3.0, 9.0, "IU/L"),
    "LH_day3": (2.0, 12.0, "IU/L"),
    "AMH": (1.0, 3.5, "ng/mL"),
    "Estradiol_day3": (25, 75, "pg/mL"),
    "Progesterone_luteal": (10, None, "ng/mL"),
    "BMI": (18.5, 24.9, "kg/m²"),
    "Age": (18, 35, "years"),
}


# Extend gene info with mock variants and literature

GENE_INFO = {
    "FOXP3": "Immune tolerance; Treg function; implantation immune balance.",
    "STAT3": "Cytokine signaling; endometrial receptivity; inflammation control.",
    "COL1A1": "Major fibrillar collagen; ECM remodeling; uterine structure.",
    "COL3A1": "Collagen type III; tissue elasticity; uterine support.",
    "RPL13A": "Ribosomal protein; housekeeping gene; translational control.",
    "RPL3": "Ribosomal protein; structural component; translational fidelity.",
    "GATA4": "Ovarian development & steroidogenesis.",
    "LHX1-AS1": "LHX1 antisense RNA; possible regulatory noncoding role.",
    "TDRD7": "RNA-binding protein; germ cell development.",
    "PDGFRB": "Platelet-derived growth factor receptor; angiogenesis; stromal signaling.",
    "ZEB2": "EMT regulator; implantation and remodeling.",
    "BCL6": "Transcriptional repressor; implicated in endometriosis and implantation failure.",
    "EEF1A1": "Elongation factor; protein synthesis; stress response regulation.",
    "MT-CO1": "Mitochondrial cytochrome c oxidase subunit I; oxidative phosphorylation.",
    "MT-CO2": "Mitochondrial cytochrome c oxidase subunit II; respiratory chain function.",
    "MT-CO3": "Mitochondrial cytochrome c oxidase subunit III; electron transport.",
    "MT-ND4": "Mitochondrial NADH dehydrogenase subunit 4; Complex I activity.",
    "SFRP4": "Secreted frizzled-related protein; Wnt signaling modulation; ovarian function."
}

KNOWN_VARIANTS = {
    "FOXP3": ["c.1010A>G (rsXXXXX) — reported in implantation failure cohorts"],
    "STAT3": ["p.R382W — altered STAT signaling (preclinical)"],
    "COL1A1": ["rs1800012 — collagen structural variant, connective tissue disorders"],
    "COL3A1": ["rs1800255 — associated with tissue elasticity issues"],
    "RPL13A": ["Rare ribosomal protein polymorphisms; usually stable housekeeping role"],
    "RPL3": ["Variants rarely reported; mostly conserved"],
    "GATA4": ["rsXXXX — associated with ovarian dysfunction"],
    "LHX1-AS1": ["No well-documented variants; exploratory research stage"],
    "TDRD7": ["Mutations linked with cataract/germline defects in families"],
    "PDGFRB": ["Exon 12 mutations — angiogenesis dysregulation"],
    "ZEB2": ["rs11598836 — linked with EMT modulation"],
    "BCL6": ["Polymorphisms linked with endometriosis and reproductive disorders"],
    "EEF1A1": ["Highly conserved; only rare variants reported in cancer studies"],
    "MT-CO1": ["Mitochondrial variants linked to oxidative phosphorylation defects"],
    "MT-CO2": ["Mitochondrial mutations associated with respiratory chain dysfunction"],
    "MT-CO3": ["Rare mitochondrial variants; respiratory chain studies"],
    "MT-ND4": ["Leber's hereditary optic neuropathy (LHON)-associated variants"],
    "SFRP4": ["Polymorphisms linked to Wnt signaling modulation; limited fertility evidence"]
}

LITERATURE_SNIPPETS = {
    "FOXP3": "Treg imbalance linked with recurrent implantation failure; immunotherapy studies ongoing.",
    "STAT3": "JAK/STAT signaling crucial for endometrial receptivity; targeted modulation under study.",
    "COL1A1": "Collagen remodeling impacts uterine structure during implantation.",
    "COL3A1": "Collagen III variants may affect uterine elasticity and implantation mechanics.",
    "RPL13A": "Stable housekeeping gene; minimal association with reproductive pathology.",
    "RPL3": "Highly conserved ribosomal protein; variant studies limited.",
    "GATA4": "Important in ovarian follicular development; studied in ovarian dysfunction.",
    "LHX1-AS1": "Emerging evidence for regulatory noncoding RNAs in implantation biology.",
    "TDRD7": "Linked with germline development and fertility in animal models.",
    "PDGFRB": "Angiogenesis regulator; stromal signaling critical in endometrium.",
    "ZEB2": "Key EMT regulator during implantation and tissue remodeling.",
    "BCL6": "Aberrant BCL6 expression observed in endometriosis and implantation failure.",
    "EEF1A1": "Translation elongation factor; stress response; limited infertility evidence.",
    "MT-CO1": "Mitochondrial gene; oxidative phosphorylation; linked to energy supply in oocytes.",
    "MT-CO2": "Respiratory chain function; mutations linked to metabolic dysfunction.",
    "MT-CO3": "Mitochondrial respiration subunit; potential role in embryo viability.",
    "MT-ND4": "Complex I subunit; mitochondrial dysfunction linked to oocyte quality.",
    "SFRP4": "Wnt signaling modulator; dysregulation implicated in ovarian dysfunction and PCOS."
}

def parse_notes(text: str):
    text_low = text.lower()
    flags = {
        'pcos': any(k in text_low for k in ["pcos", "polycystic", "cysts", "androgen", "hirsutism"]),
        'endometriosis': any(k in text_low for k in ["endometriosis", "pelvic pain", "dyspareunia", "dysmenorrhea"]),
        'irregular_cycles': any(k in text_low for k in ["irregular", "oligomenorrhea", "amenorrhea"]),
        'thyroid': any(k in text_low for k in ["tsh", "thyroid", "hypothyroid", "hyperthyroid"]),
        'male_factor': any(k in text_low for k in ["semen", "sperm", "motility", "count", "morphology"]),
        'infection': any(k in text_low for k in ["infection", "uti", "pid", "inflammation", "discharge"]),
        'hyperprolactinemia': any(k in text_low for k in ["prolactin", "galactorrhea"]),
    }
    return flags

# ============================
# Session State Helpers
# ============================
if "history" not in st.session_state:
    st.session_state.history = []
if "chat" not in st.session_state:
    st.session_state.chat = []  # list of tuples (user, assistant)

def push_history(score):
    st.session_state.history.append((datetime.now(), float(score)))
    st.session_state.history = st.session_state.history[-20:]

def push_chat(user_msg, assistant_msg):
    st.session_state.chat.append(("user", user_msg))
    st.session_state.chat.append(("assistant", assistant_msg))

# ============================
# Sidebar — Inputs
# ============================
st.sidebar.header("📋 Patient Information")

patient_name = st.sidebar.text_input("Patient Name (optional)", placeholder="e.g., Riya Sharma")

# Sidebar — Patient Profile
# ============================
st.sidebar.header("📋 Patient Profile")

colA, colB = st.sidebar.columns(2)

with colA:
    age = int(st.sidebar.slider("Age (years)", 18, 50, 30))
    bmi = float(st.sidebar.slider("BMI", 15.0, 40.0, 22.0))
    duration_infertility = st.sidebar.slider("Infertility Duration (years)", 0, 15, 0)

with colB:
    amh = float(st.sidebar.number_input("AMH (ng/mL)", min_value=0.0, max_value=15.0, value=2.5, step=0.1))
    fsh = float(st.sidebar.number_input("FSH (IU/L)", min_value=0.0, max_value=50.0, value=6.0, step=0.1))
    lh = float(st.sidebar.number_input("LH (IU/L)", min_value=0.0, max_value=50.0, value=5.0, step=0.1))
    estradiol = float(st.sidebar.number_input("Estradiol (pg/mL)", min_value=0.0, max_value=1000.0, value=50.0, step=1.0))

# Additional clinical factors
st.sidebar.markdown("### 🧪 Clinical Details")

previous_treatments = st.sidebar.multiselect(
    "Previous Treatments", 
    ["None", "IVF", "IUI", "Medications", "Surgery"],
    default=["None"]
)

menstrual_history = st.sidebar.selectbox(
    "Menstrual Regularity", 
    ["Regular", "Irregular", "Oligomenorrhea", "Amenorrhea"]
)

marital_status = st.sidebar.selectbox(
    "Marital Status", 
    ["Not Provided", "Married", "Single", "Other"]
)




st.sidebar.markdown("### 🧠 Clinical Notes")
NOTE_TEMPLATES = {
"Regular cycles, no pain": "Regular cycles, no pain",
    "Irregular cycles / oligomenorrhea": "Irregular cycles present with oligomenorrhea over last 6 months",
    "Pelvic pain & dysmenorrhea (Endometriosis-like)": "Chronic pelvic pain, dysmenorrhea, dyspareunia suspected",
    "PCOS profile": "Features suggestive of PCOS: acne, hirsutism, weight gain",
    "Thyroid symptoms": "History of thyroid issues; fatigue, weight changes",
    "Male factor suspected": "Semen analysis pending; possible motility concerns",
    "Infection/inflammation": "Recurrent UTIs; discharge; pelvic inflammatory signs",
    "Hyperprolactinemia suspicion": "Galactorrhea episodes; menstrual irregularity; prolactin suspected high",
    "Thin endometrium": "Endometrial thickness persistently <7mm across cycles",
    "Low ovarian reserve": "AMH levels low; antral follicle count reduced",
    "Recurrent miscarriage": "≥2 spontaneous miscarriages; RPL evaluation indicated",
    "Hormonal imbalance": "Abnormal FSH/LH ratio, possible ovarian dysfunction",
    "Unexplained infertility": "No clear cause after basic workup; unexplained infertility suspected",
    "Tubal factor": "History of pelvic surgery/infection; possible tubal blockage",
    "Advanced maternal age": "Female age >35 years; diminished ovarian reserve risk",
    "Lifestyle/metabolic issues": "High BMI, insulin resistance, stress factors noted",
    "Genetic/Chromosomal concern": "Family history of infertility, chromosomal abnormalities suspected",
    "Previous ART failure": "Failed IVF/IUI attempts in past; requires advanced evaluation"
}
note_choice = st.sidebar.selectbox("Choose a note template", options=list(NOTE_TEMPLATES.keys()), index=0)
extra_notes = st.sidebar.text_area("Add/Modify Notes", value=NOTE_TEMPLATES[note_choice], height=90)


# --- Parse notes to get clinical flags ---
flags = parse_notes(extra_notes)

GENE_OPTIONS = [
    "FOXP3", "LHX1-AS1", "PDGFRB", "ZEB2", "GATA4", "TDRD7", "STAT3", "BCL6",
    "MT-CO1", "COL1A1", "EEF1A1", "COL3A1", "MT-CO3", "MT-ND4", "MT-CO2",
    "SFRP4", "RPL13A", "RPL3"
]
genes = st.sidebar.multiselect(
    "Select Genes of Interest", 
    options=GENE_OPTIONS, 
    help="Choose one or more genes detected/flagged in the patient."
)

st.sidebar.markdown("### 🗓️ Cycle Information")
cycle_length = int(st.sidebar.slider("Cycle Length (days)", 21, 35, 28))
last_menses_date = st.sidebar.date_input("Last Menstrual Period (LMP)",key="lmp_date")

run_btn = st.sidebar.button("🔮 Predict & Generate Plan", use_container_width=True)

# ============================
# Helper functions (validate, charts, mock predict)
# ============================

def parse_notes(text: str):
    text_low = text.lower()
    flags = {
        'pcos': any(k in text_low for k in ["pcos", "polycystic", "cysts", "androgen", "hirsutism"]),
        'endometriosis': any(k in text_low for k in ["endometriosis", "pelvic pain", "dyspareunia", "dysmenorrhea"]),
        'irregular_cycles': any(k in text_low for k in ["irregular", "oligomenorrhea", "amenorrhea"]),
        'thyroid': any(k in text_low for k in ["tsh", "thyroid", "hypothyroid", "hyperthyroid"]),
        'male_factor': any(k in text_low for k in ["semen", "sperm", "motility", "count", "morphology"]),
        'infection': any(k in text_low for k in ["infection", "uti", "pid", "inflammation", "discharge"]),
        'hyperprolactinemia': any(k in text_low for k in ["prolactin", "galactorrhea"]),
    }
    return flags

def validate_inputs(age, bmi, amh, fsh, lh, estradiol):
    """Return dict of (ok: bool, message: str) for each variable."""
    res = {}
    # Age
    a_min, a_max, _ = NORMAL_RANGES["Age"]
    res["Age"] = (a_min <= age <= a_max, f"Target reproductive age commonly considered {a_min}-{a_max} yrs")
    # BMI
    b_min, b_max, _ = NORMAL_RANGES["BMI"]
    res["BMI"] = (b_min <= bmi <= b_max, f"Optimal BMI: {b_min}-{b_max} kg/m² (obesity/underweight can affect fertility)")
    # AMH
    am_min, am_max, am_unit = NORMAL_RANGES["AMH"]
    res["AMH"] = (amh >= am_min, f"AMH < {am_min} ng/mL suggests diminished ovarian reserve; typical normal ~{am_min}-{am_max} ng/mL")
    # FSH
    f_min, f_max, f_unit = NORMAL_RANGES["FSH_day3"]
    res["FSH"] = (f_min <= fsh <= f_max, f"Day-3 FSH typically {f_min}-{f_max} {f_unit}; higher suggests decreased reserve")
    # LH
    l_min, l_max, l_unit = NORMAL_RANGES["LH_day3"]
    res["LH"] = (l_min <= lh <= l_max, f"Day-3 LH typically {l_min}-{l_max} {l_unit}; LH:FSH ratio may suggest PCOS")
    # Estradiol
    e_min, e_max, e_unit = NORMAL_RANGES["Estradiol_day3"]
    res["Estradiol"] = (e_min <= estradiol <= e_max, f"Day-3 Estradiol typical {e_min}-{e_max} {e_unit}; high early may mask FSH interpretation")
    return res

def mock_predict(features, genes_sel, flags):
    features = age, bmi, amh, fsh, lh, estradiol 
    score = 0
    score += np.interp(age, [18, 50], [5, 25])
    score += np.interp(bmi, [18.5, 35], [5, 20])
    score += np.interp(amh, [0.1, 6.0], [25, 2])
    score += np.interp(fsh, [1.0, 20.0], [2, 18])
    score += np.interp(lh, [1.0, 20.0], [2, 15])
    if estradiol < 30 or estradiol > 300:
        score += 8
    else:
        score += 3
    gene_risk = 0
    for g in ["FOXP3", "LHX1-AS1", "PDGFRB", "ZEB2", "GATA4", "TDRD7", "STAT3", "BCL6", "MT-CO1", "COL1A1", "EEF1A1", "COL3A1", "MT-CO3", "MT-ND4", "MT-CO2", "SFRP4", "RPL13A", "RPL3"]:
        if g in genes_sel:
            gene_risk += 2.5
    score += gene_risk
    if flags.get('pcos'): score += 6
    if flags.get('endometriosis'): score += 5
    if flags.get('thyroid'): score += 4
    if flags.get('hyperprolactinemia'): score += 4
    if flags.get('infection'): score += 3
    if flags.get('male_factor'): score += 2
    score = float(np.clip(score, 0, 100))
    label = "Likely Infertile" if score >= 55 else "Likely Fertile"
    confidence = 0.55 + (abs(score-55) / 100)
    confidence = float(np.clip(confidence, 0.55, 0.95))
    return label, confidence, score

def gauge_chart(score: float):
    fig, ax = plt.subplots(figsize=(5.8, 3.5))
    ax.axis('off')
    wedge_bg = Wedge((0.5, 0), 0.45, 0, 180, fc='#f4f5f7', ec='#e5e7eb')
    ax.add_patch(wedge_bg)
    zones = [(0, 35, '#d1fae5'), (35, 55, '#fef3c7'), (55, 100, '#fee2e2')]
    for start, end, color in zones:
        ax.add_patch(Wedge((0.5, 0), 0.45, np.interp(start,[0,100],[0,180]), np.interp(end,[0,100],[0,180]), fc=color, ec='white'))
    angle = np.interp(score, [0, 100], [0, 180])
    theta = np.deg2rad(angle)
    x, y = 0.5 + 0.40*np.cos(theta), 0.0 + 0.40*np.sin(theta)
    ax.plot([0.5, x], [0.0, y], linewidth=2)
    ax.add_patch(Circle((0.5, 0), 0.015, color='black'))
    band = "Low" if score < 35 else ("Moderate" if score < 55 else "High")
    ax.text(0.5, -0.1, f"Risk Index: {score:.0f}/100 ({band})", ha='center', va='center', fontsize=12)
    return fig

def gene_importance_chart(genes_list):
    rng = np.random.default_rng(42)
    imp = rng.random(len(genes_list))
    fig, ax = plt.subplots()
    ax.barh(genes_list, imp)
    ax.set_xlabel("Importance")
    ax.set_title("Gene Contribution to Infertility")
    return fig

def clinical_factors_chart(values_dict):
    fig, ax = plt.subplots()
    ax.bar(list(values_dict.keys()), list(values_dict.values()))
    ax.set_ylabel("Value")
    ax.set_title("Clinical Factors")
    return fig

def radar_chart(genes_list):
    if len(genes_list) < 3:
        return None
    rng = np.random.default_rng(7)
    values = rng.random(len(genes_list))
    angles = np.linspace(0, 2*np.pi, len(genes_list), endpoint=False)
    values = np.concatenate((values, [values[0]]))
    angles = np.concatenate((angles, [angles[0]]))
    fig = plt.figure(figsize=(5,5))
    ax = fig.add_subplot(111, polar=True)
    ax.plot(angles, values, 'o-', linewidth=2)
    ax.fill(angles, values, alpha=0.25)
    ax.set_thetagrids(np.degrees(angles[:-1]), genes_list)
    ax.set_title("Gene Pattern Radar")
    return fig

def fertile_window_heatmap(lmp: datetime, cycle_len: int):
    """Create a simple 28-35 day cycle probability curve."""
    days = np.arange(cycle_len)
    ov_day = int(cycle_len * 0.5)
    probs = np.exp(-0.5*((days-ov_day)/2.0)**2)  # Gaussian around ov_day
    probs = probs / probs.max()
    fig, ax = plt.subplots()
    ax.plot(days, probs)
    ax.set_xlabel("Day of Cycle")
    ax.set_ylabel("Conception Probability")
    ax.set_title("Fertile Window Predictor")
    return fig

def uterine_3d_plot(estradiol_val, fsh_val):
    from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
    fig = plt.figure(figsize=(5.5, 4.2))
    ax = fig.add_subplot(111, projection='3d')
    x = np.linspace(-2,2,50)
    y = np.linspace(-2,2,50)
    X, Y = np.meshgrid(x, y)
    base = np.exp(-(X**2+Y**2))
    thickness = np.interp(estradiol_val, [10, 300], [5.5, 10.5]) - np.interp(fsh_val, [1, 20], [0, 2.0])
    Z = base * (thickness/10.0)
    ax.plot_surface(X, Y, Z, linewidth=0, antialiased=True)
    ax.set_title("Endometrium Thickness Landscape")
    return fig
# --- Decision Support: Tests (CLINICALLY EXPANDED) ---
def suggest_tests(hormones, genes_sel, flags):
    age, bmi, amh, fsh, lh, estradiol = hormones
    tests = []

    # --- Hormone axis ---
    if estradiol < 30:
        tests.append("Estradiol Day-3 repeat (assess ovarian suppression)")
    if amh < 1.0:
        tests.append("Antral Follicle Count (AFC) via transvaginal ultrasound")
    if fsh > 10:
        tests.append("Repeat Day-3 FSH + Estradiol (assess ovarian reserve)")
    if bmi > 30:
        tests.append("Oral Glucose Tolerance Test (OGTT) + HbA1c")

    # --- PCOS pathway ---
    if flags.get('pcos') or lh > 12 or bmi >= 27:
        tests += [
            "Free testosterone + SHBG (androgen profile)",
            "DHEA-S (adrenal androgens)",
            "Fasting insulin + HOMA-IR",
            "Pelvic ultrasound (polycystic ovarian morphology)"
        ]

    # --- Endometriosis pathway ---
    if flags.get('endometriosis'):
        tests += [
            "Transvaginal USG / MRI pelvis",
            "CA-125 (supportive, not diagnostic)",
            "Laparoscopy with histopathology (gold standard if indicated)"
        ]

    # --- Thyroid & Endocrine ---
    if flags.get('thyroid'):
        tests += ["TSH", "Free T4", "Anti-TPO antibodies (autoimmune thyroiditis)"]
    if flags.get('hyperprolactinemia'):
        tests += [
            "Serum Prolactin (fasting, repeat if elevated)",
            "Pituitary MRI (if prolactin persistently >100 ng/mL)"
        ]

    # --- Male factor ---
    if flags.get('male_factor'):
        tests += [
            "Semen analysis (WHO 2021 parameters)",
            "DNA fragmentation index (if recurrent IVF/ICSI failure)",
            "Sperm morphology (strict Kruger criteria)"
        ]

    # --- Infections & Inflammation ---
    if flags.get('infection'):
        tests += [
            "Cervical/vaginal swab culture",
            "CRP/ESR (inflammation markers)"
        ]

    # --- Imaging & Structure ---
    tests += [
        "HSG (Fallopian tube patency – first line)",
        "Sonohysterogram / 3D ultrasound",
        "Hysteroscopy (if abnormality suspected)"
    ]

    # --- Gene-specific add-ons ---
    if "FOXP3" in genes_sel:
        tests.append("Immune profiling – Treg activity, ANA, antiphospholipid antibodies")
    if "LHX1-AS1" in genes_sel:
        tests.append("Endometrial receptivity transcriptomic panel (e.g., ERA)")
    if "PDGFRB" in genes_sel:
        tests.append("Endometrial Doppler blood flow, fibrosis markers")
    if "ZEB2" in genes_sel:
        tests.append("Endometrial biopsy – EMT markers (E-cadherin, vimentin)")
    if "GATA4" in genes_sel:
        tests.append("Ovarian reserve markers (AMH, inhibin B)")
    if "TDRD7" in genes_sel:
        tests.append("Oocyte morphology and maturation assessment (IVF lab)")
    if "STAT3" in genes_sel:
        tests.append("Inflammatory cytokine panel (IL-6, TNF-α)")
    if "BCL6" in genes_sel:
        tests.append("Endometriosis diagnostic IHC (BCL6, CD138)")
    if any(g in genes_sel for g in ["MT-CO1", "MT-CO2", "MT-CO3", "MT-ND4"]):
        tests.append("Mitochondrial function panel – ATP assay, mtDNA copy number")
    if any(g in genes_sel for g in ["COL1A1", "COL3A1"]):
        tests.append("Endometrial fibrosis panel (hysteroscopy, collagen markers)")
    if "EEF1A1" in genes_sel:
        tests.append("Protein synthesis/metabolic stress markers (ROS, UPR)")
    if "SFRP4" in genes_sel:
        tests.append("WNT signaling assay – endometrial receptivity markers")
    if any(g in genes_sel for g in ["RPL13A", "RPL3"]):
        tests.append("Ribosomal stress / translational control profiling")

    # De-duplicate
    tests = list(dict.fromkeys(tests))
    return tests


# --- Decision Support: Medicines  ---
def suggest_medicines(hormones, genes_sel, flags):
    age, bmi, amh, fsh, lh, estradiol = hormones
    recs = []

    # --- Ovulation induction / ovarian reserve ---
    if fsh > 12 or lh > 12:
        recs += [
            "Letrozole (first-line ovulation induction in PCOS, ASRM/ESHRE approved)",
            "Clomiphene Citrate (if Letrozole unavailable)",
            "hMG or recombinant FSH (if resistant cases, IVF protocol)"
        ]
    if amh < 1.5:
        recs += [
            "DHEA (75mg/day – ovarian reserve support)",
            "CoQ10 (200–600 mg/day – egg quality)",
            "Melatonin (3–5 mg nightly – oocyte quality support)"
        ]

    # --- PCOS & Metabolic ---
    if flags.get('pcos') or (bmi >= 27):
        recs += [
            "Metformin (500–1500 mg/day – insulin sensitizer)",
            "Myo-inositol + D-chiro-inositol (insulin signaling support)",
            "Lifestyle: Weight loss (5–10%) improves ovulation"
        ]

    # --- Luteal & Endometrium support ---
    if "PGR" in genes_sel or estradiol < 50:
        recs += ["Micronized Progesterone (luteal phase support)"]
    if "ESR1" in genes_sel:
        recs += ["Estrogen priming protocol for thin endometrium"]

    # --- Inflammation & Immune modulation ---
    if "STAT3" in genes_sel or flags.get('endometriosis') or flags.get('infection'):
        recs += [
            "Omega-3 fatty acids (anti-inflammatory support)",
            "Short NSAID course (for pain, not peri-ovulation)",
            "Consider GnRH analogues (endometriosis suppression)"
        ]
    if "FOXP3" in genes_sel:
        recs += [
            "Low-dose Prednisolone (immune modulation, short-term)",
            "Immunotherapy (specialist-guided, e.g., IVIG, G-CSF)"
        ]

    # --- Thyroid / Prolactin ---
    if flags.get('thyroid'):
        recs += ["Levothyroxine (TSH <2.5 mIU/L preconception)"]
    if flags.get('hyperprolactinemia'):
        recs += ["Cabergoline (first-line for hyperprolactinemia)"]

    # --- Gene-specific therapeutics ---
    if "LHX1-AS1" in genes_sel:
        recs.append("Endometrial receptivity–tailored embryo transfer")
    if "PDGFRB" in genes_sel:
        recs.append("Antifibrotic support – Pentoxifylline, Vitamin E")
    if "ZEB2" in genes_sel:
        recs.append("EMT-modulating support – possible role of statins, resveratrol")
    if "GATA4" in genes_sel:
        recs.append("Ovarian stimulation protocol tailoring (FSH dose adjustment)")
    if "TDRD7" in genes_sel:
        recs.append("Antioxidants for oocyte quality – CoQ10, melatonin")
    if "STAT3" in genes_sel:
        recs.append("JAK-STAT modulation (clinical trial context)")
    if "BCL6" in genes_sel:
        recs.append("GnRH agonist/antagonist pre-treatment for endometriosis-related failure")
    if any(g in genes_sel for g in ["MT-CO1", "MT-CO2", "MT-CO3", "MT-ND4"]):
        recs.append("Mitochondrial support – CoQ10, L-carnitine, NAD+ boosters")
    if any(g in genes_sel for g in ["COL1A1", "COL3A1"]):
        recs.append("Anti-fibrotic strategy – hysteroscopic adhesiolysis + estrogen therapy")
    if "EEF1A1" in genes_sel:
        recs.append("Metabolic stabilizers – antioxidant + stress-targeted supplements")
    if "SFRP4" in genes_sel:
        recs.append("Endometrium priming with estrogen/progesterone")
    if any(g in genes_sel for g in ["RPL13A", "RPL3"]):
        recs.append("Nutritional optimization for protein translation (B-complex, amino acids)")

    # --- General Fertility Health ---
    recs += [
        "Folic acid 400–800 µg/day",
        "Vitamin D repletion if <30 ng/mL",
        "Antioxidants (Vit C, Vit E – supportive)"
    ]

    # De-duplicate
    recs = list(dict.fromkeys(recs))
    return recs

def agentic_next_steps(score, flags, tests, meds):
    """
    Steps To Follow
    """

    steps = []

    # 🔹 High-risk pathway
    if score >= 55:
        steps.append("🔹 **Immediate Clinical Plan (High-Risk):**")
        steps.append("- Reassess baseline hormones (FSH, LH, AMH, Estradiol, TSH, Prolactin) on Day 2–4 of next cycle")
        steps.append("- Schedule **transvaginal ultrasound**: antral follicle count (AFC) + endometrial thickness/vascularity")
        
        if flags.get('pcos'):
            steps.append("- PCOS pathway: metabolic screening (HbA1c, fasting insulin/glucose) + initiate lifestyle + ovulation induction planning")
        if flags.get('endometriosis'):
            steps.append("- Endometriosis suspicion: consider referral for **diagnostic laparoscopy** if pain/implantation failure persists")
        if flags.get('thin_endometrium'):
            steps.append("- Thin endometrium detected: consider **estrogen priming** ± adjuvants (sildenafil, G-CSF)")

        steps.append("- Begin structured **12-week lifestyle protocol** (diet, exercise, sleep hygiene)")
        steps.append("- Re-evaluate in **6–8 weeks** to monitor ovarian/uterine response before ART cycle")

    # 🔹 Low-to-moderate pathway
    else:
        steps.append("🔹 **Conservative Management Plan (Low-to-Moderate Risk):**")
        steps.append("- Continue lifestyle optimization (Mediterranean-style diet, moderate exercise, stress reduction)")
        steps.append("- Track ovulation for 3 cycles (BBT charting, LH kits, or follicular scan)")
        steps.append("- Optimize natural conception/IUI by targeting fertile window")
        
        if flags.get('thyroid'):
            steps.append("- Endocrine support: **TSH optimization** (target <2.5 mIU/L) with endocrinology input")
        if flags.get('autoimmune'):
            steps.append("- Autoimmune flag: screen ANA, antiphospholipid antibodies (if RPL/implantation failure history)")

    # 🔹 Tests & Medications integration
    if len(tests) > 0:
        steps.append(f"🧪 **Recommended Investigations:** {', '.join(tests[:5])}{'…' if len(tests) > 5 else ''}")
    if len(meds) > 0:
        steps.append(f"💊 **Therapeutic Considerations:** {', '.join(meds[:5])}{'…' if len(meds) > 5 else ''}")

    # 🔹 Final check-in
    steps.append("📅 **Follow-up:** Ensure regular review with fertility specialist; escalate to ART (IUI/IVF) if no improvement after 6 months.")

    return steps


def plot_cycle_vs_normal(cycle_len, patient_name="Patient", patient_ov_day=None, lab_values=None):
    """
Visualizes a patient's menstrual cycle vs. reference .
    """
    import numpy as np, matplotlib.pyplot as plt

    # ---- hormone profile generator ----
    def hormone_profile(days, ov_day, peak_width=3):
        days = np.array(days)
        fsh = np.exp(-0.5*((days - (ov_day-1))/4.0)**2) * 0.6
        lh  = np.exp(-0.5*((days - ov_day)/1.2)**2) * 1.0
        e2  = np.exp(-0.5*((days - (ov_day-2))/3.0)**2) * 0.9
        p   = np.where(days > ov_day, np.exp(-0.5*((days - (ov_day+7))/5.0)**2)*0.8, 0.05)
        return fsh, lh, e2, p

    # ---- Reference profile (28-day) ----
    days_norm = np.arange(1,29)
    f_fsh, f_lh, f_e2, f_p = hormone_profile(days_norm, 14)

    # ---- Patient profile ----
    days_pat = np.arange(1, cycle_len+1)
    ov_pat = patient_ov_day if patient_ov_day else int(cycle_len*0.5)
    p_fsh, p_lh, p_e2, p_p = hormone_profile(days_pat, ov_pat)

    # ---- Plot ----
    fig, ax = plt.subplots(2,1, figsize=(10,6), sharex=False)

    # Gonadotropins
    ax[0].plot(days_norm, f_fsh, color="gray", alpha=0.5, label="FSH (ref)")
    ax[0].plot(days_pat, p_fsh, color="blue", lw=2, label=f"FSH ({patient_name})")
    ax[0].plot(days_norm, f_lh, color="gray", alpha=0.5, label="LH (ref)")
    ax[0].plot(days_pat, p_lh, color="red", lw=2, label=f"LH ({patient_name})")
    ax[0].set_title(f"🧬 Gonadotropin Peaks (Reference vs {patient_name})")
    ax[0].legend(loc='upper right')

    # Sex Steroids
    ax[1].plot(days_norm, f_e2, color="gray", alpha=0.5, label="E2 (ref)")
    ax[1].plot(days_pat, p_e2, color="green", lw=2, label=f"E2 ({patient_name})")
    ax[1].plot(days_norm, f_p, color="gray", alpha=0.5, label="Prog (ref)")
    ax[1].plot(days_pat, p_p, color="purple", lw=2, label=f"Prog ({patient_name})")
    ax[1].set_title(f"💊 Sex Steroids Across Cycle (Ref vs {patient_name})")
    ax[1].legend(loc='upper right')

    # Personalization → add ovulation marker
    for a in ax:
        a.axvline(x=ov_pat, color="orange", ls="--", lw=1.5, label="Ovulation")
        a.set_xlabel("Cycle Day")
        a.set_ylabel("Relative Hormone Level")
    
    # Add measured lab values (if given)
    if lab_values:
        markers = {"FSH":"o", "LH":"s", "E2":"^", "Prog":"D"}
        colors  = {"FSH":"blue", "LH":"red", "E2":"green", "Prog":"purple"}
        for hormone, vals in lab_values.items():
            for d,v in vals:
                ax[0 if hormone in ["FSH","LH"] else 1].scatter(d, v, 
                    marker=markers[hormone], color=colors[hormone], s=80, zorder=5,
                    label=f"{hormone} test")
    
    # Footer annotation with patient name
    fig.text(0.5, -0.02, f"Personalized Hormone Profile for {patient_name}", 
             ha="center", fontsize=11, style="italic", color="darkblue")

    plt.tight_layout()
    return fig


# ============================
# Simple rule-based chat assistant (with placeholder LLM support)
# ============================
def assistant_answer(message):
    """Rule-based assistant fallback. If message contains gene name, return gene insight.
       For common queries, return curated answers. Otherwise generic help.
       (No external LLM call here.)"""
    text = message.lower()
    # gene-focused
    for g in GENE_INFO.keys():
        if g.lower() in text:
            role = GENE_INFO.get(g, "No curated insight")
            variants = KNOWN_VARIANTS.get(g, ["No common variants recorded here."])
            lit = LITERATURE_SNIPPETS.get(g, "No literature snippet available.")
            reply = f"**{g}** — {role}\n\nKnown variants / notes:\n- " + "\n- ".join(variants) + f"\n\nResearch note: {lit}"
            return reply
    # PCOS
    if "pcos" in text or "polycystic" in text:
        return textwrap.dedent(
            """PCOS (Polycystic Ovary Syndrome) — quick summary:
            - Typical features: irregular cycles, hyperandrogenism (acne/hirsutism), polycystic ovaries on ultrasound.
            - Common labs: elevated LH:FSH ratio in some cases, insulin resistance markers (fasting insulin, HOMA-IR).
            - Clinical approach: lifestyle (weight loss), metformin if insulin resistance, ovulation induction (letrozole/clomiphene) when required.
            Always confirm with clinician evaluation and tailored tests."""
        )
    # AMH/FSH questions
    if "amh" in text:
        return "AMH (Anti-Müllerian Hormone) estimates ovarian reserve. Values <1 ng/mL often indicate reduced ovarian reserve; values >3–4 ng/mL may be high (seen in PCOS). Interpret with age and ultrasound (AFC)."
    if "fsh" in text:
        return "FSH on day 2–4 helps assess ovarian reserve. Higher FSH suggests reduced ovarian reserve. Always interpret with estradiol and AMH."
    if "ovulation" in text or "fertile window" in text:
        return "Ovulation typically occurs ~14 days prior to the next period. The fertile window is ~5 days before ovulation + day of ovulation. Track with LMP and cycle length; ovulation predictors (LH kit) give a closer window."
    # default fallback
    return "I can help explain tests, hormones, gene roles, or suggest what to discuss with a clinician. Try asking: 'Explain PCOS risk factors', 'What does high FSH mean?', or 'Tell me about FOXP3'."

# ============================
# Main layout
# ============================
# Left column: guidance + validation; Center: central analytics; Right: chat assistant
left_col, center_col, right_col = st.columns([1.2, 2.6, 1.2])



# Validation summary
#val = validate_inputs(age, bmi, amh, fsh, lh, estradiol)
#st.markdown("<div class='card'><h3>⚠️ Validation Summary</h3>", unsafe_allow_html=True)
#for k,(ok,msg) in val.items():
 #       if ok:
  #          st.markdown(f"<div class='small'><span class='ok'>✔ {k} OK</span> — <span class='small'>{msg}</span></div>", unsafe_allow_html=True)
   #     else:
    #        st.markdown(f"<div class='small'><span class='warn'>✖ {k} OUTSIDE RANGE</span> — <span class='small'>{msg}</span></div>", unsafe_allow_html=True)
#st.markdown("</div>", unsafe_allow_html=True)

with center_col:
    # If not run: show placeholder + cycle visualization and inputs snapshot
    if not run_btn:
        st.info("Use the sidebar to enter patient data, then click **Predict & Generate Plan**.")
        with st.expander("🔎 Patient Snapshot"):
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("**Inputs Summary**")
            if patient_name:
                st.markdown(f"- Patient: **{patient_name}**")
            st.markdown(f"- Age: **{age}** | BMI: **{bmi}**")
            st.markdown(f"- AMH: **{amh}** ng/mL | FSH: **{fsh}** IU/L | LH: **{lh}** IU/L | Estradiol: **{estradiol}** pg/mL")
            if genes:
                st.markdown("**Genes Selected:** " + " ".join([f"<span class='pill'>{g}</span>" for g in genes]), unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("📈Cycle Pattern Overview (Reference vs Patient)")
        st.pyplot(plot_cycle_vs_normal(cycle_length), use_container_width=True)
        st.caption("Reference: 28-day cycle (ovulation day 14). Patient curve adapts to selected cycle length.")
        st.markdown("</div>", unsafe_allow_html=True)

    # If run, show full analytics
if run_btn:
    notes = extra_notes
    flags = parse_notes(notes)
    features = [age, bmi, amh, fsh, lh, estradiol]
    label, confidence, score = mock_predict(features, genes, flags)
    push_history(score)
    meds = suggest_medicines(features, genes, flags)
    tests = suggest_tests(features, genes, flags)

    # Top cards
    c1, c2, c3 = st.columns([1, 2, 1])  # center (Risk) is wider

    # Prediction card
    with c1:
        st.markdown(
            f"""
            <div class='card' style='text-align:center;'>
                <h3 style='margin:0;'>🔮 Prediction</h3>
                <div><span class='badge'>{label}</span></div>
                <div class='footer-note'>Confidence: {confidence:.2f}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Gauge chart card (bigger)
    with c2:
        fig_g = gauge_chart(score)
        fig_g.set_size_inches(2, 1.5)  # expand gauge size
        st.pyplot(fig_g, use_container_width=True)

    # Inputs card
    with c3:
        st.markdown(
            f"""
            <div class='card'>
                <h3>🧪 Inputs</h3>
                <p>→ Patient: {patient_name}</p>
                <p>→ Age: {age}  |  BMI: {bmi}</p>
                <p>→ AMH: {amh} ng/mL</p>
                <p>→ FSH: {fsh} IU/L  |  LH: {lh} IU/L</p>
                <p>→ Estradiol: {estradiol} pg/mL</p>
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown("---")

if st.button("Show Report In Detail"):
    st.session_state.run_clicked = True 
# ============================
# Only show AFTER prediction
# ============================

if st.session_state.get("run_clicked", False):
    section = st.radio(
        "📌 Select a section:",
        [
            "📊 Clinical Analytics",
            "🧬 Genomic Insights",
            "🗓️ Cycle Timeline",
            "🧠 Clinical Notes",
            "🧾 Plan & Reports"
        ],
        horizontal=True
    )

    # === Clinical Analytics ===
    if section == "📊 Clinical Analytics":
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("🧮 Feature Visualizations")
        c11, c12 = st.columns(2)
        with c11:
            if genes:
                st.pyplot(gene_importance_chart(genes), use_container_width=True)
                st.caption("Top gene-level predictors for this patient")
            else:
                st.info("No gene selected 🧬 — please pick from the sidebar to view insights.")
        with c12:
            st.pyplot(
                clinical_factors_chart({
                    "Age": age, "BMI": bmi, "FSH": fsh, "AMH": amh, "LH": lh
                }),
                use_container_width=True
            )
            st.caption("Clinical hormone and demographic profile")
        st.markdown("</div>", unsafe_allow_html=True)

    # === Genomic Insights ===
    elif section == "🧬 Genomic Insights":
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("🧬 Gene-Specific Insights")

        if not genes:
            st.info("No gene selected 🧬 — please pick from the sidebar to view insights.")
        else:
            for g in genes:
                role = GENE_INFO.get(g, "No curated insight yet.")
                variants = KNOWN_VARIANTS.get(g, ["No known variants recorded."])
                lit = LITERATURE_SNIPPETS.get(g, "No literature snippet available.")

                # Individual gene card
                with st.container():
                    st.markdown(f"### {g}")
                    st.markdown(f"🧬 **Role:** {role}")
                    st.markdown(f"🧾 **Variants:** {'; '.join(variants)}")
                    with st.expander("📖 Research Notes"):
                        st.write(lit)
                    st.divider()  # separator between genes

        st.markdown("</div>", unsafe_allow_html=True)

    # === Cycle Timeline ===
    elif section == "🗓️ Cycle Timeline":
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("📅 Fertility Timeline Predictor")

        if last_menses_date:
            lmp = pd.to_datetime(last_menses_date)
            cycle_days = int(cycle_length)

            # Estimate ovulation
            ovulation_est = lmp + pd.Timedelta(days=int(cycle_days * 0.5))
            fw_start = ovulation_est - pd.Timedelta(days=3)
            fw_end = ovulation_est + pd.Timedelta(days=1)
            next_cycle = lmp + pd.Timedelta(days=cycle_days)

            # Plot heatmap
            st.plotly_chart(
                fertile_window_heatmap(lmp, cycle_days),
                use_container_width=True
            )

            # Progress bar (days since LMP)
            days_passed = (pd.Timestamp.today() - lmp).days
            st.progress(min(days_passed / cycle_days, 1.0))

            # Cards
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("🟢 Fertile Window", f"{fw_start.date()} → {fw_end.date()}")
            with c2:
                st.metric("🔴 Ovulation", f"{ovulation_est.date()}")
            with c3:
                st.metric("🔵 Next Cycle", f"{next_cycle.date()}")

            # Countdown
            days_to_ovu = (ovulation_est - pd.Timestamp.today()).days
            if days_to_ovu > 0:
                st.info(f"⏳ {days_to_ovu} days until estimated ovulation")
            else:
                st.info("Ovulation estimate has passed in this cycle.")

            st.caption("⚠️ Predictions are approximate. Cycle variations, health, and stress can affect accuracy.")
        else:
            st.info("Provide Last Menstrual Period (LMP) in the sidebar to calculate timeline.")

        st.markdown("</div>", unsafe_allow_html=True)

    # === Clinical Notes ===
    elif section == "🧠 Clinical Notes":
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("🧠 Clinical Notes & Detections")

        colA, colB = st.columns(2)

        with colA:
            st.markdown("**✅ Detected Conditions / Risk Flags**")
            any_detected = False
            for k, v in flags.items():
                if v:
                    any_detected = True
                    st.success(f"- {k.replace('_',' ').title()}")
            if not any_detected:
                st.info("No significant risks flagged.")

        with colB:
            st.markdown("**⚠️ Potential Blindspots**")
            blindspots = [k.replace('_',' ').title() for k, v in flags.items() if not v]
            if blindspots:
                for b in blindspots:
                    st.warning(f"- {b}")
            else:
                st.write("All key areas checked.")

        st.markdown("</div>", unsafe_allow_html=True)

        # --- Decision Support ---
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Decision Support: Suggested Tests & Medicines")
        features = [age, bmi, amh, fsh, lh, estradiol]
        meds = suggest_medicines(features, genes, flags)
        tests = suggest_tests(features, genes, flags)

        c21, c22 = st.columns(2)
        with c21:
            with st.expander("🧪 Suggested Tests", expanded=True):
                if tests:
                    for t in tests:
                        st.markdown(f"- {t}")
                else:
                    st.write("No immediate tests suggested.")
        with c22:
            with st.expander("💊 Suggested Medicines", expanded=True):
                if meds:
                    for m in meds:
                        st.markdown(f"- {m}")
                else:
                    st.write("No medicine suggestions right now.")

        st.caption("⚠️ These are **educational insights only** and must be discussed with a licensed clinician.")
        st.markdown("</div>", unsafe_allow_html=True)

        # --- Workflow ---
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("📋 Personalized Workflow")
        label, confidence, score = mock_predict(features, genes, flags)
        steps = agentic_next_steps(score, flags, tests, meds)
        for i, stext in enumerate(steps, start=1):
            st.markdown(f"- [ ] {stext}")   # checkbox-style list

        st.markdown("</div>", unsafe_allow_html=True)

        # Extra disclaimer footer
        st.info("🔒 This workflow does not replace medical advice. Use results for guidance and structured discussion with your doctor.")

    # === Plan & Reports ===
    elif section == "🧾 Plan & Reports":
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("📌 Personalized Plan Summary")
        features = [age, bmi, amh, fsh, lh, estradiol]
        meds = suggest_medicines(features, genes, flags)
        tests = suggest_tests(features, genes, flags)
        label, confidence, score = mock_predict(features, genes, flags)
        steps = agentic_next_steps(score, flags, tests, meds)
        # --- Build Report ---
        lines = []
        lines.append("NoveFertiScan – Infertility Diagnostic Prototype\n")
        lines.append(f"📅 Date: {datetime.now().strftime('%d %B %Y')}\n\n")
        if patient_name: 
            lines.append(f"👤 Patient: {patient_name}\n")
        lines.append("--- 📝 Inputs ---\n")
        lines.append(f"Age: {age} yrs | BMI: {bmi}\n")
        lines.append(f"AMH: {amh} ng/mL | FSH: {fsh} IU/L | LH: {lh} IU/L | Estradiol: {estradiol} pg/mL\n")
        lines.append("Genes: " + (", ".join(genes) if genes else "None") + "\n")

        band = "🟢 Low" if score < 35 else ("🟡 Moderate" if score < 55 else "🔴 High")
        lines.append("--- 🔍 Prediction ---\n")
        lines.append(f"Label: {label}\n")
        lines.append(f"Confidence: {confidence:.2f}\n")
        lines.append(f"Risk Index: {score:.0f}/100 ({band})\n\n")

        lines.append("--- 🧪 Suggested Tests ---\n")
        if tests:
            for t in tests: 
                lines.append(f"- {t}\n")
        else:
            lines.append("- None suggested based on current inputs.\n")

        lines.append("\n--- 💊 Suggested Medicines (for clinician discussion) ---\n")
        if meds:
            for m in meds: 
                lines.append(f"- {m}\n")
        else:
            lines.append("- None at this stage.\n")

        lines.append("\n--- 🛠️ Next Steps ---\n")
        if steps:
            for stext in steps: 
                lines.append(f"- {stext}\n")
        else:
            lines.append("- Maintain healthy lifestyle, monitor regularly.\n")

        lines.append("\n⚠️ Disclaimer: This app is an educational prototype and not a substitute for professional medical advice.\n")

        # --- Display Report ---
        report_txt = "".join(lines)
        st.text_area("📄 Preview Report", value=report_txt, height=300)

        # --- Export Options ---
        df_tests = pd.DataFrame({"Suggested Tests": tests or []})
        df_meds  = pd.DataFrame({"Suggested Medicines": meds or []})
        df_steps = pd.DataFrame({"Next Steps": steps or []})

        cdl1, cdl2, cdl3, cdl4, cdl5 = st.columns([1,1,1,1,1])
        with cdl1:
            st.download_button("⬇️ Full Plan (TXT)", data=report_txt, file_name="genovive_plan.txt")
        with cdl2:
            st.download_button("⬇️ Tests (CSV)", data=df_tests.to_csv(index=False), file_name="suggested_tests.csv")
        with cdl3:
            st.download_button("⬇️ Medicines (CSV)", data=df_meds.to_csv(index=False), file_name="suggested_medicines.csv")
        with cdl4:
            st.download_button("⬇️ Next Steps (CSV)", data=df_steps.to_csv(index=False), file_name="next_steps.csv")

        # 🔥 Bonus: Export to PDF
        pdf_buffer = io.BytesIO()
        from reportlab.platypus import SimpleDocTemplate, Paragraph
        from reportlab.lib.styles import getSampleStyleSheet

        doc = SimpleDocTemplate(pdf_buffer)
        styles = getSampleStyleSheet()
        story = [Paragraph(line.replace("\n", "<br/>"), styles["Normal"]) for line in report_txt.split("\n")]
        doc.build(story)
        pdf_value = pdf_buffer.getvalue()

        with cdl5:
            st.download_button("⬇️ Full Plan (PDF)", data=pdf_value, file_name="genovive_plan.pdf", mime="application/pdf")

        st.caption("✅ Plan generated. Share with your clinician for informed decision-making.")
        st.markdown("</div>", unsafe_allow_html=True)

    

        


import streamlit as st
from Bio import Entrez

# Configure Entrez
Entrez.email = "your_email@example.com"  # Replace with your email

# Gene list for dropdown
genes =  [
    "FOXP3", "LHX1-AS1", "PDGFRB", "ZEB2", "GATA4", 
    "TDRD7", "STAT3", "BCL6", "MT-CO1", "COL1A1", 
    "EEF1A1", "COL3A1", "MT-CO3", "MT-ND4", "MT-CO2", 
    "SFRP4", "RPL13A", "RPL3"
]


# Clinical markers
clinical_markers = {
    "FSH_day3": (3.0, 9.0, "IU/L"),
    "LH_day3": (2.0, 12.0, "IU/L"),
    "AMH": (1.0, 3.5, "ng/mL"),
    "Estradiol_day3": (25, 75, "pg/mL"),
    "Progesterone_luteal": (10, None, "ng/mL"),
    "BMI": (18.5, 24.9, "kg/m²"),
    "Age": (18, 35, "years"),
}

st.title("💬 Clinical Chat Assistant")
st.markdown("Ask about infertility genes or lab markers.")

# Dropdown for gene selection
selected_gene = st.selectbox("🔬 Select a Gene:", genes)

# Dropdown for clinical markers
selected_marker = st.selectbox("🧪 Select a Clinical Marker:", list(clinical_markers.keys()))

# Function to fetch gene info
def fetch_gene_summary(gene_symbol):
    try:
        handle = Entrez.esearch(db="gene", term=gene_symbol + "[sym] AND Homo sapiens[orgn]")
        record = Entrez.read(handle)
        if record["IdList"]:
            gene_id = record["IdList"][0]
            summary_handle = Entrez.efetch(db="gene", id=gene_id, rettype="xml")
            summary_record = Entrez.read(summary_handle)
            summary = summary_record[0]["Entrezgene_summary"]
            return summary
        else:
            return "No gene summary found."
    except Exception as e:
        return f"Error fetching data: {e}"

# Show gene info
if st.button("Show Gene Info"):
    gene_summary = fetch_gene_summary(selected_gene)
    st.subheader(f"🧬 {selected_gene}")
    st.write(gene_summary)

# Show clinical marker info
if st.button("Show Clinical Marker Info"):
    ref_range = clinical_markers[selected_marker]
    st.subheader(f"🧪 {selected_marker}")
    if ref_range[1]:
        st.write(f"Reference Range: {ref_range[0]} - {ref_range[1]} {ref_range[2]}")
    else:
        st.write(f"Reference Value: > {ref_range[0]} {ref_range[2]}")

from Bio import Entrez

# ======================================================
# 🧬 Gene Insight (fetch PubMed summaries)
# ======================================================
st.subheader("🧬 Gene Literature Insight")

gene_name = st.text_input("Enter Gene Symbol (e.g., FSHR, AMHR2, LHCGR):")

if gene_name:
    Entrez.email = "your_email@example.com"  # Required by NCBI
    try:
        handle = Entrez.esearch(db="pubmed", term=f"{gene_name} AND infertility", retmax=10)
        record = Entrez.read(handle)
        id_list = record["IdList"]

        if not id_list:
            st.warning("No PubMed results found for this gene.")
        else:
            st.success(f"Top {len(id_list)} PubMed results for {gene_name}:")
            for pmid in id_list:
                fetch = Entrez.efetch(db="pubmed", id=pmid, rettype="abstract", retmode="text")
                summary = fetch.read()
                with st.expander(f"PMID {pmid}"):
                    st.write(summary)
    except Exception as e:
        st.error(f"Error fetching PubMed data: {e}")


# End of App
