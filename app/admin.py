import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from src.memory import load_chat

st.set_page_config(
    page_title="Admin Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────
#  ADVANCED MINIMALIST STYLES (BRIGHT MODE)
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Base & Variables ── */
:root {
    --bg-main: #FAFAFA;
    --text-dark: #111827;
    --text-muted: #6B7280;
    --accent-blue: #2563EB;
    --accent-dark: #0F172A;
    --border-light: #E5E7EB;
    --white: #FFFFFF;
    --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    --shadow-float: 0 10px 25px -5px rgba(0, 0, 0, 0.08);
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp {
    background: var(--bg-main) !important;
    font-family: 'Inter', sans-serif;
    color: var(--text-dark);
}

/* Hide Streamlit Elements */
#MainMenu, header, footer, .stDeployButton, .viewerBadge_container__1QSob, div[data-testid="stToolbar"] { 
    display: none !important; 
}

/* ── Container ── */
.block-container {
    max-width: 1100px !important;
    padding: 0 1.5rem 3rem !important;
    margin: 0 auto !important;
}

/* ── Modern Header ── */
.cs-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 2rem 0 1.5rem;
    background: transparent;
    border-bottom: 1px solid var(--border-light);
    margin-bottom: 2rem;
}
.cs-logo {
    display: flex;
    align-items: center;
    gap: 12px;
}
.cs-logo-icon {
    width: 42px; height: 42px;
    background: linear-gradient(135deg, #0F172A, #3b82f6);
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 20px;
    color: var(--white);
    box-shadow: var(--shadow-sm);
}
.cs-logo-text {
    font-size: 20px;
    font-weight: 700;
    color: var(--text-dark);
    letter-spacing: -0.02em;
}
.cs-logo-sub {
    font-size: 13px;
    color: var(--text-muted);
    font-weight: 500;
}
.cs-status {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 13px;
    font-weight: 500;
    color: var(--text-dark);
    background: var(--white);
    padding: 8px 14px;
    border-radius: 20px;
    border: 1px solid var(--border-light);
    box-shadow: var(--shadow-sm);
}
.cs-status-dot {
    width: 8px; height: 8px;
    background: #10B981;
    border-radius: 50%;
    box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.2);
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4); }
    70% { box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
    100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
}

/* ── Dashboard Cards & Animations ── */
.cs-card {
    background: var(--white);
    border: 1px solid var(--border-light);
    border-radius: 20px;
    padding: 24px;
    box-shadow: var(--shadow-sm);
    margin-bottom: 24px;
    animation: springUp 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.1) forwards;
    opacity: 0;
    transform: translateY(15px);
}
.cs-card-title {
    font-size: 16px;
    font-weight: 600;
    color: var(--text-dark);
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 8px;
}
@keyframes springUp {
    to { opacity: 1; transform: translateY(0); }
}

/* ── Custom KPI Metrics ── */
.cs-kpi-grid {
    display: flex;
    gap: 16px;
    margin-bottom: 24px;
    animation: springUp 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.1) forwards;
}
.cs-kpi-box {
    flex: 1;
    background: var(--white);
    border: 1px solid var(--border-light);
    border-radius: 16px;
    padding: 20px;
    box-shadow: var(--shadow-sm);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.cs-kpi-box:hover {
    transform: translateY(-3px);
    box-shadow: var(--shadow-md);
    border-color: var(--accent-blue);
}
.cs-kpi-label { font-size: 13px; color: var(--text-muted); font-weight: 500; }
.cs-kpi-val { font-size: 28px; font-weight: 700; color: var(--text-dark); margin-top: 4px; }

/* ── Empty State ── */
.cs-empty {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 12px;
    padding: 4rem 0;
}
.cs-empty-icon { font-size: 40px; }
.cs-empty-title { font-size: 20px; font-weight: 700; color: var(--text-dark); }
.cs-empty-sub   { font-size: 14px; color: var(--text-muted); text-align: center; }

/* Adjust Streamlit native elements */
div[data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden; border: 1px solid var(--border-light); }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="cs-header">
  <div class="cs-logo">
    <div class="cs-logo-icon">📊</div>
    <div>
      <div class="cs-logo-text">Admin Center</div>
      <div class="cs-logo-sub">Support AI Analytics</div>
    </div>
  </div>
  <div class="cs-status">
    <div class="cs-status-dot"></div>
    Live Data Connected
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  LOAD DATA
# ─────────────────────────────────────────────
df = load_chat()

# ─────────────────────────────────────────────
#  DASHBOARD CONTENT
# ─────────────────────────────────────────────
if not df.empty:
    
    # 1. KPI Metrics Row
    total_messages = len(df)
    unique_queries = df["Message"].nunique() if "Message" in df.columns else 0
    
    st.markdown(f"""
    <div class="cs-kpi-grid">
        <div class="cs-kpi-box">
            <div class="cs-kpi-label">Total Messages Logged</div>
            <div class="cs-kpi-val">{total_messages}</div>
        </div>
        <div class="cs-kpi-box">
            <div class="cs-kpi-label">Unique User Queries</div>
            <div class="cs-kpi-val">{unique_queries}</div>
        </div>
        <div class="cs-kpi-box">
            <div class="cs-kpi-label">System Status</div>
            <div class="cs-kpi-val" style="color: #10B981;">Healthy</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. Layout columns for Chart and Data
    col_chart, col_data = st.columns([1, 1], gap="large")

    with col_chart:
        st.markdown("""
        <div class="cs-card" style="animation-delay: 0.1s;">
            <div class="cs-card-title">📈 Top Message Intents</div>
        """, unsafe_allow_html=True)
        
        # Native Streamlit Chart (looks great inside our white card)
        st.bar_chart(df["Message"].value_counts().head(10), use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

    with col_data:
        st.markdown("""
        <div class="cs-card" style="animation-delay: 0.2s;">
            <div class="cs-card-title">🗂️ Raw Chat Logs</div>
        """, unsafe_allow_html=True)
        
        # Native Streamlit Dataframe
        st.dataframe(df, use_container_width=True, height=350)
        
        st.markdown("</div>", unsafe_allow_html=True)

else:
    # Beautiful Empty State
    st.markdown("""
    <div class="cs-card">
        <div class="cs-empty">
          <div class="cs-empty-icon">📭</div>
          <div class="cs-empty-title">No chat data available yet</div>
          <div class="cs-empty-sub">Once users start interacting with Support AI, the logs and analytics will appear here automatically.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div style="text-align: center; font-size: 12px; color: #6B7280; padding: 2rem 0; font-weight: 500;">
    Secure Admin Dashboard • Data updates on refresh
</div>
""", unsafe_allow_html=True)