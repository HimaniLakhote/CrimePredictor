import streamlit as st
from model import predict_all, data
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="NEXUS — Crime Intelligence",
    layout="wide",
    page_icon="assets/badge.png",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM CSS ---------------- #
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=Share+Tech+Mono&family=Exo+2:wght@300;400;600;700&display=swap');

/* ---- GLOBAL ---- */
html, body, [class*="css"] {
    font-family: 'Exo 2', sans-serif;
    background-color: #060A12;
    color: #C9D6E3;
}

.main .block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1400px;
}

/* ---- BACKGROUND GRID ---- */
.stApp {
    background-color: #060A12;
    background-image:
        linear-gradient(rgba(0,212,255,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,212,255,0.03) 1px, transparent 1px);
    background-size: 40px 40px;
}

/* ---- HERO BANNER ---- */
.hero-banner {
    background: linear-gradient(135deg, #0D1B2A 0%, #0A1628 50%, #091020 100%);
    border: 1px solid rgba(0,212,255,0.2);
    border-radius: 12px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(0,124,240,0.12) 0%, transparent 70%);
    pointer-events: none;
}
.hero-banner::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #00D4FF, #007CF0, transparent);
}
.hero-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: 2.6rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    background: linear-gradient(90deg, #00D4FF, #FFFFFF, #007CF0);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 0.3rem 0;
    text-transform: uppercase;
}
.hero-subtitle {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.78rem;
    color: #4A9EBF;
    letter-spacing: 0.2em;
    text-transform: uppercase;
}
.hero-badge {
    display: inline-block;
    background: rgba(0,212,255,0.1);
    border: 1px solid rgba(0,212,255,0.3);
    color: #00D4FF;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.15em;
    padding: 3px 10px;
    border-radius: 3px;
    margin-right: 8px;
    margin-top: 0.8rem;
    display: inline-flex;
    align-items: center;
    gap: 5px;
}
.status-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #00FF88;
    display: inline-block;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}

/* ---- METRIC CARDS ---- */
.metric-card {
    background: linear-gradient(135deg, #0D1B2A, #0A1420);
    border: 1px solid rgba(0,212,255,0.15);
    border-radius: 10px;
    padding: 1.2rem 1.4rem;
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    background: linear-gradient(180deg, #00D4FF, #007CF0);
    border-radius: 3px 0 0 3px;
}
.metric-label {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.18em;
    color: #4A7A8A;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}
.metric-value {
    font-family: 'Rajdhani', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: #00D4FF;
    line-height: 1;
}
.metric-sub {
    font-size: 0.7rem;
    color: #3A6A7A;
    margin-top: 0.2rem;
    font-family: 'Share Tech Mono', monospace;
}

/* ---- SECTION HEADERS ---- */
.section-header {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.1rem;
    font-weight: 600;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #6BBDD4;
    margin: 1.5rem 0 0.8rem 0;
    display: flex;
    align-items: center;
    gap: 10px;
}
.section-header::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, rgba(0,212,255,0.3), transparent);
}

/* ---- FORM PANEL ---- */
.form-panel {
    background: #0A1520;
    border: 1px solid rgba(0,212,255,0.1);
    border-radius: 10px;
    padding: 1.5rem;
}

/* ---- SELECTBOXES ---- */
.stSelectbox label {
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.12em !important;
    color: #4A7A9A !important;
    text-transform: uppercase !important;
}
.stSelectbox > div > div {
    background-color: #0D1B2A !important;
    border: 1px solid rgba(0,212,255,0.2) !important;
    border-radius: 6px !important;
    color: #C9D6E3 !important;
}
.stSelectbox > div > div:focus-within {
    border-color: #00D4FF !important;
    box-shadow: 0 0 0 1px rgba(0,212,255,0.3) !important;
}

/* ---- BUTTONS ---- */
.stButton > button {
    background: linear-gradient(135deg, #003D5C, #005080) !important;
    color: #00D4FF !important;
    border: 1px solid rgba(0,212,255,0.4) !important;
    border-radius: 6px !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    height: 3em !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #005080, #0070A0) !important;
    border-color: #00D4FF !important;
    box-shadow: 0 0 20px rgba(0,212,255,0.2) !important;
    transform: translateY(-1px) !important;
}

/* ---- RESULT CARD ---- */
.result-card {
    background: linear-gradient(135deg, #0A1A2A, #091525);
    border: 1px solid rgba(0,212,255,0.25);
    border-radius: 10px;
    padding: 1.5rem;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.result-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #00D4FF, transparent);
}
.result-verdict {
    font-family: 'Rajdhani', sans-serif;
    font-size: 2.4rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    color: #00D4FF;
    text-transform: uppercase;
    text-shadow: 0 0 30px rgba(0,212,255,0.4);
}
.result-confidence {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.85rem;
    color: #4A9EBF;
    letter-spacing: 0.1em;
    margin-top: 0.3rem;
}

/* ---- ALERT BOXES ---- */
.alert-high {
    background: rgba(255,50,50,0.1);
    border: 1px solid rgba(255,80,80,0.4);
    border-left: 3px solid #FF3232;
    border-radius: 6px;
    padding: 0.8rem 1rem;
    font-family: 'Rajdhani', sans-serif;
    font-weight: 600;
    color: #FF8080;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}
.alert-med {
    background: rgba(255,165,0,0.08);
    border: 1px solid rgba(255,165,0,0.35);
    border-left: 3px solid #FFA500;
    border-radius: 6px;
    padding: 0.8rem 1rem;
    font-family: 'Rajdhani', sans-serif;
    font-weight: 600;
    color: #FFB84D;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}
.alert-low {
    background: rgba(0,255,136,0.06);
    border: 1px solid rgba(0,255,136,0.3);
    border-left: 3px solid #00FF88;
    border-radius: 6px;
    padding: 0.8rem 1rem;
    font-family: 'Rajdhani', sans-serif;
    font-weight: 600;
    color: #00CC6A;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}

/* ---- DIVIDER ---- */
hr {
    border-color: rgba(0,212,255,0.1) !important;
    margin: 1.5rem 0 !important;
}

/* ---- SIDEBAR ---- */
section[data-testid="stSidebar"] {
    background-color: #070D18 !important;
    border-right: 1px solid rgba(0,212,255,0.1);
}
section[data-testid="stSidebar"] .stMetric {
    background: #0A1520;
    border: 1px solid rgba(0,212,255,0.12);
    border-radius: 8px;
    padding: 0.8rem;
    margin-bottom: 0.6rem;
}
section[data-testid="stSidebar"] label {
    color: #4A7A9A !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.65rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
}

/* ---- TABLE ---- */
.stTable table {
    background: #0A1520;
    border: 1px solid rgba(0,212,255,0.15);
    border-radius: 8px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.78rem;
}
.stTable th {
    background: rgba(0,212,255,0.08) !important;
    color: #00D4FF !important;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    font-size: 0.7rem !important;
}
.stTable td {
    color: #A0B8C8 !important;
    border-color: rgba(0,212,255,0.08) !important;
}

/* ---- SPINNER ---- */
.stSpinner > div {
    border-top-color: #00D4FF !important;
}

/* ---- PLOTLY CHART CONTAINER ---- */
.js-plotly-plot {
    border-radius: 8px;
    overflow: hidden;
}
</style>
""", unsafe_allow_html=True)

# ---- PLOTLY THEME ---- #
PLOT_BG = "rgba(10,21,32,0)"
PAPER_BG = "rgba(10,21,32,0)"
GRID_COLOR = "rgba(0,212,255,0.07)"
TEXT_COLOR = "#6BBDD4"
ACCENT = "#00D4FF"
ACCENT2 = "#007CF0"
FONT_MONO = "Share Tech Mono"

def plotly_layout(title=""):
    return dict(
        title=dict(text=title, font=dict(family=FONT_MONO, size=11, color=TEXT_COLOR), x=0.01),
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=PLOT_BG,
        font=dict(family=FONT_MONO, color=TEXT_COLOR, size=10),
        margin=dict(l=10, r=10, t=36, b=10),
        xaxis=dict(gridcolor=GRID_COLOR, linecolor=GRID_COLOR, tickfont=dict(size=9)),
        yaxis=dict(gridcolor=GRID_COLOR, linecolor=GRID_COLOR, tickfont=dict(size=9)),
        showlegend=False,
    )

# ============================================================
# HERO BANNER
# ============================================================
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">NEXUS Intelligence System</div>
    <div class="hero-subtitle">Predictive Crime Analysis &nbsp;|&nbsp; Bayesian Inference Engine &nbsp;|&nbsp; v2.4</div>
    <div style="margin-top:0.8rem; display:flex; gap:8px; flex-wrap:wrap;">
        <span class="hero-badge"><span class="status-dot"></span> SYSTEM ONLINE</span>
        <span class="hero-badge">CLASSIFICATION: LAW ENFORCEMENT USE</span>
        <span class="hero-badge">AI ENGINE: ACTIVE</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("""
    <div style="font-family:'Rajdhani',sans-serif; font-size:1.1rem; font-weight:700;
         letter-spacing:0.2em; color:#00D4FF; text-transform:uppercase;
         padding:0.5rem 0 1rem 0; border-bottom:1px solid rgba(0,212,255,0.15); margin-bottom:1rem;">
        System Status
    </div>
    """, unsafe_allow_html=True)

    crime_rate = (data['crime'] == 'yes').mean()
    st.metric("Total Records", f"{len(data):,}")
    st.metric("Feature Inputs", len(data.columns) - 2)
    st.metric("Crime Prevalence", f"{crime_rate*100:.1f}%")

    st.markdown("""
    <div style="margin-top:1.2rem; padding:0.8rem; background:rgba(0,255,136,0.05);
         border:1px solid rgba(0,255,136,0.2); border-radius:8px;
         font-family:'Share Tech Mono',monospace; font-size:0.68rem;
         color:#00CC6A; letter-spacing:0.12em; text-transform:uppercase;">
        <span style="display:inline-block; width:8px; height:8px; border-radius:50%;
              background:#00FF88; margin-right:6px;
              animation:pulse 2s infinite;"></span>
        AI MODEL ACTIVE
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-family:'Share Tech Mono',monospace; font-size:0.65rem;
         color:#2A4A5A; letter-spacing:0.08em; line-height:1.8;">
        NEXUS CRIME INTELLIGENCE<br>
        BAYESIAN NETWORK ENGINE<br>
        ACADEMIC DEMONSTRATION<br>
        &copy; 2025 NEXUS SYSTEMS
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# ANALYTICS SECTION
# ============================================================
st.markdown('<div class="section-header">Dataset Intelligence Overview</div>', unsafe_allow_html=True)

colA, colB = st.columns(2, gap="large")

with colA:
    crime_counts = data['crime'].value_counts().reset_index()
    crime_counts.columns = ['label', 'count']
    total = crime_counts['count'].sum()
    crime_counts['pct'] = crime_counts['count'] / total * 100

    colors = ['#FF4444' if l == 'yes' else '#00D4FF' for l in crime_counts['label']]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=crime_counts['label'].str.upper(),
        y=crime_counts['count'],
        marker=dict(
            color=colors,
            line=dict(color='rgba(0,0,0,0)', width=0),
            opacity=0.85,
        ),
        text=[f"{p:.1f}%" for p in crime_counts['pct']],
        textposition='outside',
        textfont=dict(family=FONT_MONO, size=11, color=TEXT_COLOR),
        hovertemplate='<b>%{x}</b><br>Count: %{y}<br>Share: %{text}<extra></extra>',
    ))
    layout = plotly_layout("CRIME DISTRIBUTION")
    layout['yaxis']['title'] = dict(text="RECORDS", font=dict(size=9))
    layout['xaxis']['title'] = dict(text="CLASSIFICATION", font=dict(size=9))
    fig.update_layout(**layout)
    fig.update_yaxes(rangemode='tozero')
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

with colB:
    sus_counts = data['suspect'].value_counts().reset_index()
    sus_counts.columns = ['label', 'count']

    palette = px.colors.sequential.Blues_r[:len(sus_counts)]
    if len(palette) < len(sus_counts):
        palette = ['#007CF0', '#00A8D4', '#00D4FF', '#4AE0FF', '#80EEFF'][:len(sus_counts)]

    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        x=sus_counts['label'].str.upper() if sus_counts['label'].dtype == object else sus_counts['label'],
        y=sus_counts['count'],
        marker=dict(
            color=palette,
            line=dict(color='rgba(0,0,0,0)', width=0),
            opacity=0.85,
        ),
        hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>',
    ))
    layout2 = plotly_layout("SUSPECT DISTRIBUTION")
    layout2['yaxis']['title'] = dict(text="RECORDS", font=dict(size=9))
    layout2['xaxis']['title'] = dict(text="SUSPECT CLASS", font=dict(size=9))
    fig2.update_layout(**layout2)
    fig2.update_yaxes(rangemode='tozero')
    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

st.divider()

# ============================================================
# DISPLAY RESULT FUNCTION
# ============================================================
def display_result(result_dict, variable_name):
    most_likely = max(result_dict, key=result_dict.get)
    prob = result_dict[most_likely]

    st.markdown(f"""
    <div class="result-card">
        <div style="font-family:'Share Tech Mono',monospace; font-size:0.65rem;
             color:#3A6A8A; letter-spacing:0.2em; text-transform:uppercase; margin-bottom:0.5rem;">
            PREDICTION OUTPUT
        </div>
        <div class="result-verdict">{most_likely.upper()}</div>
        <div class="result-confidence">CONFIDENCE &nbsp;|&nbsp; {prob*100:.2f}%</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Horizontal probability bar chart
    labels = [k.upper() for k in result_dict.keys()]
    values = list(result_dict.values())
    bar_colors = [ACCENT if k == most_likely else '#1A3A5A' for k in result_dict.keys()]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=labels,
        x=values,
        orientation='h',
        marker=dict(
            color=bar_colors,
            line=dict(color='rgba(0,0,0,0)', width=0),
        ),
        text=[f"{v*100:.1f}%" for v in values],
        textposition='inside',
        textfont=dict(family=FONT_MONO, size=10, color='#060A12'),
        hovertemplate='<b>%{y}</b>: %{x:.3f}<extra></extra>',
    ))
    layout = plotly_layout("PROBABILITY BREAKDOWN")
    layout['xaxis']['tickformat'] = '.0%'
    layout['xaxis']['range'] = [0, 1]
    layout['margin'] = dict(l=10, r=10, t=36, b=10)
    fig.update_layout(**layout)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # Risk alert
    if variable_name == "crime":
        if prob > 0.75:
            st.markdown('<div class="alert-high">THREAT LEVEL: HIGH &nbsp;—&nbsp; Immediate action advised</div>', unsafe_allow_html=True)
        elif prob > 0.45:
            st.markdown('<div class="alert-med">THREAT LEVEL: MODERATE &nbsp;—&nbsp; Monitor situation</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="alert-low">THREAT LEVEL: LOW &nbsp;—&nbsp; Situation nominal</div>', unsafe_allow_html=True)

# ============================================================
# EVIDENCE INPUT
# ============================================================
st.markdown('<div class="section-header">Case Evidence Input</div>', unsafe_allow_html=True)

target_cols = {'crime', 'suspect'}
feature_cols = [col for col in data.columns if col not in target_cols]

evidence = {}
cols = st.columns(3)
for i, feature in enumerate(feature_cols):
    unique_vals = sorted(data[feature].unique())
    with cols[i % 3]:
        evidence[feature] = st.selectbox(
            f"{feature.replace('_',' ').title()}",
            unique_vals
        )

st.divider()

# ============================================================
# PREDICTIONS
# ============================================================
st.markdown('<div class="section-header">Analysis Engines</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("""
    <div style="font-family:'Rajdhani',sans-serif; font-size:0.95rem; font-weight:600;
         letter-spacing:0.15em; color:#6BBDD4; text-transform:uppercase; margin-bottom:0.8rem;">
        Crime Prediction Engine
    </div>
    """, unsafe_allow_html=True)
    if st.button("ANALYZE CRIME", key="btn_crime"):
        with st.spinner("Running Bayesian inference..."):
            crime_dict, _ = predict_all(evidence)
            display_result(crime_dict, "crime")

with col2:
    st.markdown("""
    <div style="font-family:'Rajdhani',sans-serif; font-size:0.95rem; font-weight:600;
         letter-spacing:0.15em; color:#6BBDD4; text-transform:uppercase; margin-bottom:0.8rem;">
        Suspect Identification
    </div>
    """, unsafe_allow_html=True)
    if st.button("IDENTIFY SUSPECT", key="btn_suspect"):
        with st.spinner("Analyzing suspect patterns..."):
            _, suspect_dict = predict_all(evidence)
            display_result(suspect_dict, "suspect")

st.divider()

# ============================================================
# CASE HISTORY
# ============================================================
st.markdown('<div class="section-header">Case History Log</div>', unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = []

if st.button("SAVE THIS CASE", key="btn_save"):
    crime_dict, suspect_dict = predict_all(evidence)
    st.session_state.history.append({
        "crime": max(crime_dict, key=crime_dict.get),
        "suspect": max(suspect_dict, key=suspect_dict.get)
    })

if st.session_state.history:
    df_hist = pd.DataFrame(st.session_state.history)
    df_hist.index = [f"CASE-{str(i+1).zfill(3)}" for i in range(len(df_hist))]
    df_hist.columns = [c.upper() for c in df_hist.columns]
    st.table(df_hist)

st.divider()

# ============================================================
# FOOTER
# ============================================================
st.markdown("""
<div style="text-align:center; padding:1.5rem 0 0.5rem 0;">
    <div style="font-family:'Rajdhani',sans-serif; font-size:1.1rem; font-weight:700;
         letter-spacing:0.25em; color:#1A4A6A; text-transform:uppercase;">
        NEXUS CRIME INTELLIGENCE SYSTEM
    </div>
    <div style="font-family:'Share Tech Mono',monospace; font-size:0.65rem;
         color:#1A3A4A; letter-spacing:0.12em; margin-top:0.4rem;">
        BAYESIAN NETWORK ENGINE &nbsp;|&nbsp; FOR ACADEMIC DEMONSTRATION ONLY
    </div>
</div>
""", unsafe_allow_html=True)