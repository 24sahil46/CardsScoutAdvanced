# main.py
import streamlit as st
from config.settings import APP_SETTINGS

# 1. Page Configuration
st.set_page_config(page_title="CardScout AI", page_icon="🕵️", layout="wide")

# PREMIUM FINTECH UI INJECTION & SIDEBAR NAVIGATION POLISH
st.markdown("""
    <style>
    /* Modern App Background */
    .stApp {
        background-color: #0B0F19;
    }
    
    /* Sleek Input Boxes */
    div[data-baseweb="input"] > div {
        background-color: #1A2235 !important;
        border: 1px solid #2D3748 !important;
        border-radius: 8px !important;
        color: #E2E8F0 !important;
    }
    div[data-baseweb="input"] > div:focus-within {
        border-color: #06B6D4 !important;
        box-shadow: 0 0 0 1px #06B6D4 !important;
    }
    
    /* Premium Buttons */
    button[kind="primary"] {
        background: linear-gradient(135deg, #0284C7 0%, #06B6D4 100%) !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    button[kind="primary"]:hover {
        opacity: 0.9 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(6, 182, 212, 0.4) !important;
    }
    
    /* Glowing Metric Cards */
    [data-testid="stMetric"] {
        background-color: #111827 !important;
        border: 1px solid #1F2937 !important;
        padding: 15px !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06) !important;
    }
    [data-testid="stMetricValue"] {
        color: #F8FAFC !important;
        font-weight: 700 !important;
    }
    
    /* Styled Expanders (Digital Wallet) */
    [data-testid="stExpander"] {
        border: 1px solid #1E293B !important;
        border-radius: 10px !important;
        background-color: #0F172A !important;
    }
    
    /* Sidebar Polish */
    [data-testid="stSidebar"] {
        background-color: #080C14 !important;
        border-right: 1px solid #1E293B !important;
    }

/* =========================================
       SIDEBAR NAVIGATION PILL SHAPE POLISH
       ========================================= */
       
    /* 1. Header styling */
    [data-testid="stSidebar"] div[role="radiogroup"] > label:first-of-type {
        text-transform: uppercase !important;
        font-size: 11px !important;
        letter-spacing: 1.5px !important;
        color: #64748B !important;
        font-weight: 700 !important;
    }

    /* 2. Style each option as a rounded pill card */
    [data-testid="stSidebar"] div[role="radiogroup"] label {
        background-color: #111827 !important;
        border: 1px solid #1F2937 !important;
        border-radius: 30px !important;
        padding: 10px 16px !important;
        margin-bottom: 8px !important;
        width: 100% !important;
        transition: all 0.25s ease-in-out !important;
    }

    /* 3. Hover effect */
    [data-testid="stSidebar"] div[role="radiogroup"] label:hover {
        background-color: #1F2937 !important;
        border-color: #06B6D4 !important;
    }

    /* 4. Active/Selected pill styling with glowing effect */
    [data-testid="stSidebar"] div[role="radiogroup"] label[aria-checked="true"] {
        background: linear-gradient(135deg, rgba(2,132,199,0.25) 0%, rgba(6,182,212,0.2) 100%) !important;
        border: 1px solid #06B6D4 !important;
        box-shadow: 0 0 12px rgba(6, 182, 212, 0.3) !important;
    }

    /* 5. Text styling & uppercase transformation for both options */
    [data-testid="stSidebar"] div[role="radiogroup"] label p {
        color: #94A3B8 !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    [data-testid="stSidebar"] div[role="radiogroup"] label[aria-checked="true"] p {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }
    
    /* Glowing Effect for The Obsidian Vault Title */
    .obsidian-glow {
        background: linear-gradient(135deg, #38BDF8 0%, #06B6D4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(0 0 25px rgba(6, 182, 212, 0.5));
    }
    </style>
""", unsafe_allow_html=True)

# 2. Dynamic CSS Loading
def load_css():
    try:
        with open("utils/theme.css", "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("theme.css not found. Running without custom styles.")

load_css()

# 3. Sidebar Navigation Gateway
st.sidebar.title("🕵️ CardScout")
st.sidebar.markdown("---")

app_mode = st.sidebar.radio(
    "Navigation Gateway",
    ["🚀 Guest Scout (Card Discovery)", "🔒 Optimization Hub (Login)"]
)

# 4. Global Sidebar Co-Pilot
st.sidebar.markdown("---")
with st.sidebar.expander("💬 Ask CardScout AI: Swipe or Hold?", expanded=False):
    st.caption("Ask quick purchase questions (e.g., 'Spending ₹4,500 on Swiggy')")

    if not st.session_state.get('logged_in', False):
        st.warning("🔒 Please login to The Vault and add your cards to use the Co-Pilot.")
    else:
        if "copilot_messages" not in st.session_state:
            st.session_state.copilot_messages = []

        # Display recent chat history
        for msg in st.session_state.copilot_messages[-4:]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        user_query = st.chat_input("Ask Co-Pilot...", key="sidebar_copilot_input")
        if user_query:
            # Display user query
            st.session_state.copilot_messages.append({"role": "user", "content": user_query})
            
            # Pull cards and limits from wallet
            active_wallet = st.session_state.get("wallet", [])
            active_limits = st.session_state.get("card_limits", {})
            
            from core.ai_agent import get_copilot_verdict
            with st.spinner("Analyzing yield..."):
                advice = get_copilot_verdict(user_query, active_wallet, active_limits)
                st.session_state.copilot_messages.append({"role": "assistant", "content": advice})
            st.rerun()

# 5. Page Routing Logic
if app_mode == "🚀 Guest Scout (Card Discovery)":
    from views.guest_scout import render_guest_scout
    render_guest_scout()
    
elif app_mode == "🔒 Optimization Hub (Login)":
    from views.optimization_hub import render_optimization_hub
    render_optimization_hub()