# main.py
import streamlit as st
import base64
import os
from config.settings import APP_SETTINGS

# 1. Page Configuration
st.set_page_config(page_title="CardScout AI", page_icon="🧭", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""
    <style>
    /* 1. Hide the empty default Streamlit header */
    [data-testid="stHeader"] {
        display: none !important;
    }
    
    /* 2. Pull the entire main container flush to the top */
    .block-container {
        padding-top: 2rem !important; /* Change to 1rem if you want it even higher! */
    }
    </style>
""", unsafe_allow_html=True)

# 2. Dynamic CSS Loading
def load_css():
    try:
        with open("utils/theme.css", "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass

load_css()

# --- 3. UNIVERSAL APP BACKGROUND (WITH BLUR) ---
def set_main_background():
    bg_file = "app_bg.png"
    if os.path.exists(bg_file):
        with open(bg_file, "rb") as f:
            encoded_bg = base64.b64encode(f.read()).decode().replace('\n', '')
        
        st.markdown(f"""
            <style>
            /* Creates a dedicated background layer that we can safely blur */
            [data-testid="stAppViewContainer"]::before {{
                content: "";
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-image: url(data:image/png;base64,{encoded_bg}) !important;
                background-size: cover !important;
                background-position: center center !important;
                background-repeat: no-repeat !important;
                /* Applies the light blur and drops brightness slightly so cards pop */
                filter: blur(6px) brightness(0.85); 
                /* Scales up slightly to hide blurry transparent edges around the monitor */
                transform: scale(1.03); 
                z-index: -1; /* Pushes this layer firmly behind your app content */
            }}
            /* Forces Streamlit's default background containers to be completely transparent */
            [data-testid="stAppViewContainer"], [data-testid="stHeader"], .stApp {{
                background: transparent !important;
            }}
            </style>
        """, unsafe_allow_html=True)
    else:
        st.error(f"🚨 Background image '{bg_file}' not found! Please ensure it is renamed correctly.")

set_main_background()

# 4. State Management for Routing
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Home"

# 5. Global Top Navigation Bar

# --- Top Navigation Line ---
st.markdown("""
    <style>
    .nav-divider {
        height: 1px;
        background: linear-gradient(90deg, rgba(16, 185, 129, 0), rgba(16, 185, 129, 0.5), rgba(16, 185, 129, 0));
        margin: 10px 0 15px 0;
    }
    </style>
    <div class='nav-divider'></div>
""", unsafe_allow_html=True)

# --- Navigation CSS (Includes fixes for dropdown arrow) ---
st.markdown("""
    <style>
    button[data-testid="stPopoverButton"] span.material-symbols-rounded,
    button[data-testid="stPopoverButton"] [data-testid="stIconMaterial"],
    button[data-testid="stPopoverButton"] svg {
        display: none !important;
        opacity: 0 !important;
        width: 0 !important;
        height: 0 !important;
        visibility: hidden !important;
        overflow: hidden !important;
    }

    div[data-testid="column"]:nth-child(3) button,
    div[data-testid="column"]:nth-child(4) button,
    div[data-testid="column"]:nth-child(5) button {
        border-radius: 30px !important;
        min-height: 42px !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
        transition: all 0.3s ease !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
    }

    div[data-testid="column"]:nth-child(3) button {
        background-color: rgba(16, 185, 129, 0.08) !important;
        border: 1px solid rgba(16, 185, 129, 0.4) !important;
        color: #E2E8F0 !important;
    }
    div[data-testid="column"]:nth-child(3) button:hover {
        background-color: rgba(16, 185, 129, 0.15) !important;
        border-color: #10B981 !important;
    }

    div[data-testid="column"]:nth-child(4) button {
        background-color: rgba(191, 166, 122, 0.15) !important;
        border: 1px solid rgba(191, 166, 122, 0.6) !important;
        color: #F8FAFC !important;
    }
    div[data-testid="column"]:nth-child(4) button:hover {
        background-color: rgba(191, 166, 122, 0.25) !important;
    }

    div[data-testid="column"]:nth-child(5) button {
        background-color: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        color: #BFA67A !important;
    }
    div[data-testid="column"]:nth-child(5) button:hover {
        background-color: rgba(255, 255, 255, 0.08) !important;
        border-color: rgba(191, 166, 122, 0.5) !important;
    }
    </style>
""", unsafe_allow_html=True)

nav_brand, nav_space, nav_home, nav_hub, nav_copilot = st.columns([3.5, 3.5, 1.2, 1.2, 2.5])

with nav_brand:
    st.markdown("""
        <div style='display: flex; align-items: center; height: 100%; margin-top: -12px; cursor: default;'>
            <h2 style='margin: 0; font-weight: 700; font-size: 1.7rem; letter-spacing: -0.5px; font-family: "Inter", sans-serif;'>
                <span style='color: #FFFFFF;'>Card</span><span style='color: #34D399;'>Scout</span>
            </h2>
        </div>
    """, unsafe_allow_html=True)
with nav_home:
    if st.button("Home", use_container_width=True):
        st.session_state.current_page = "Home"
        st.rerun()

with nav_hub:
    hub_label = "Vault" if st.session_state.get('logged_in', False) else "Vault"
    if st.button(hub_label, use_container_width=True):
        st.session_state.current_page = "Optimization Hub"
        st.rerun()

with nav_copilot:
    with st.popover("Ask CardScout AI", use_container_width=True):
        st.markdown("**Quick Purchase Advice**")
        st.caption("Ask quick purchase questions (e.g., 'Spending ₹4,500 on Swiggy')")

        if not st.session_state.get('logged_in', False):
            st.warning("🔒 Please login to The Vault and add your cards to use the Co-Pilot.")
        else:
            if "copilot_messages" not in st.session_state:
                st.session_state.copilot_messages = []

            for msg in st.session_state.copilot_messages[-4:]:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

            user_query = st.chat_input("Ask Co-Pilot...", key="top_copilot_input")
            if user_query:
                st.session_state.copilot_messages.append({"role": "user", "content": user_query})
                active_wallet = st.session_state.get("wallet", [])
                active_limits = st.session_state.get("card_limits", {})
                
                from core.ai_agent import get_copilot_verdict
                with st.spinner("Analyzing yield..."):
                    advice = get_copilot_verdict(user_query, active_wallet, active_limits)
                    st.session_state.copilot_messages.append({"role": "assistant", "content": advice})
                st.rerun()

# --- Bottom Navigation Line ---
st.markdown("<div class='nav-divider' style='margin-top: 15px;'></div>", unsafe_allow_html=True)

# 6. Page Routing Logic
if st.session_state.current_page == "Home":
    
    # --- FOOLPROOF BUTTON STYLING ---
    st.markdown("""
        <style>
        .block-container {
            padding-top: 1.5rem !important;
            padding-bottom: 1rem !important;
        }

        /* Universally targets primary buttons so it never fails on different screens */
        button[kind="primary"] {
            border-radius: 30px !important;
            background-color: rgba(4, 13, 8, 0.95) !important;
            border: 1px solid rgba(212, 175, 55, 0.5) !important;
            color: #E2E8F0 !important;
            font-size: 0.9rem !important;
            font-weight: 500 !important;
            min-height: 42px !important;
            width: 65% !important; 
            margin: 0 auto !important; 
            display: block !important;
            position: relative !important;
            z-index: 10 !important; 
            box-shadow: 0 4px 20px rgba(0,0,0,0.8) !important;
            transition: all 0.3s ease !important;
        }

        button[kind="primary"]:hover {
            border-color: rgba(212, 175, 55, 0.9) !important;
            background-color: rgba(212, 175, 55, 0.15) !important;
            color: #FFFFFF !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    _, center_col, _ = st.columns([1, 3, 1])
    
    with center_col:
        st.markdown("""
            <style>
            .hero-title-sleek {
                font-family: 'Inter', -apple-system, sans-serif !important;
                font-size: 3.7rem !important;
                font-weight: 590 !important;
                letter-spacing: -1px !important;
                margin-bottom: 0 !important;
                padding-bottom: 0 !important;
                line-height: 1.1 !important;
                text-shadow: 0px 4px 20px rgba(0, 0, 0, 0.6), 0px 0px 40px rgba(16, 185, 129, 0.2) !important;
            }
            .hero-subtitle-sleek {
                font-family: 'Inter', -apple-system, sans-serif !important;
                color: #D4AF37 !important; /* Premium Metallic Gold */
                font-size: 1.05rem !important;
                letter-spacing: 3px !important;
                font-weight: 600 !important; /* Bumped up slightly to make the gold stand out */
                margin-top: 5px !important;
                text-shadow: 0px 2px 5px rgba(0, 0, 0, 0.8) !important;
            }
            </style>
            <div style='text-align: center; position: relative; z-index: 10; margin-top: -10px; margin-bottom: 40px;'>
                <h1 class='hero-title-sleek'>
                    <span style='color: #FFFFFF;'>Card</span><span style='color: #34D399;'>Scout</span>
                </h1>
                <p class='hero-subtitle-sleek'>SMART DECISIONS, SMARTER REWARDS.</p>
            </div>
        """, unsafe_allow_html=True)
        
        # --- LOAD CARD IMAGES ---
        guest_file = "card.png"
        vault_file = "vault.png"
        guest_bg = ""
        vault_bg = ""
        
        if os.path.exists(guest_file):
            with open(guest_file, "rb") as f:
                guest_bg = base64.b64encode(f.read()).decode().replace('\n', '')
        
        if os.path.exists(vault_file):
            with open(vault_file, "rb") as f:
                vault_bg = base64.b64encode(f.read()).decode().replace('\n', '')

        c1, c2 = st.columns(2, gap="large")
        
        # --- CARD 1: GUEST SCOUT ---
        with c1:
            st.markdown(f"""
                <div style="
                    background-image: url(data:image/png;base64,{guest_bg});
                    background-size: 115% 125%;
                    background-position: center;
                    background-repeat: no-repeat;
                    border: 1px solid rgba(212, 175, 55, 0.6);
                    border-radius: 16px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.8);
                    margin-bottom: -75px; 
                    position: relative;
                    z-index: 1;
                    width: 100%;
                    aspect-ratio: 1.586 / 1;
                    overflow: hidden;
                ">
                    <div style="
                        background-color: rgba(4, 13, 8, 0.6);
                        height: 100%; 
                        width: 100%; 
                        box-sizing: border-box;
                        padding: 0 35px 75px 35px;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                        align-items: center;
                        text-align: center;
                    ">
                        <h3 style='margin:0 0 8px 0; font-size: 1.4rem; font-weight: 700; color: #F8FAFC; text-shadow: 0 2px 6px rgba(0,0,0,1);'>🚀 Guest Scout</h3>
                        <p style='color: #E2E8F0; font-size: 0.95rem; line-height: 1.5; margin: 0; text-shadow: 0 2px 6px rgba(0,0,0,1);'>Analyze your expenditure profile to discover your highest-yielding credit card match.</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button("Enter Discovery Mode", key="btn_guest_scout", use_container_width=True, type="primary"):
                st.session_state.current_page = "Guest Scout"
                st.rerun()
                    
        # --- CARD 2: OBSIDIAN VAULT ---
        with c2:
            st.markdown(f"""
                <div style="
                    background-image: url(data:image/png;base64,{vault_bg});
                    background-size: 115% 125%;
                    background-position: center;
                    background-repeat: no-repeat;
                    border: 1px solid rgba(212, 175, 55, 0.6);
                    border-radius: 16px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.8);
                    margin-bottom: -75px; 
                    position: relative;
                    z-index: 1;
                    width: 100%;
                    aspect-ratio: 1.586 / 1;
                    overflow: hidden;
                ">
                    <div style="
                        background-color: rgba(4, 13, 8, 0.65);
                        height: 100%;
                        width: 100%;
                        box-sizing: border-box; 
                        padding: 0 35px 75px 35px; 
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                        align-items: center;
                        text-align: center;
                    ">
                        <h3 style='margin:0 0 8px 0; font-size: 1.4rem; font-weight: 700; color: #F8FAFC; text-shadow: 0 2px 6px rgba(0,0,0,1);'>💎 The Obsidian Vault</h3>
                        <p style='color: #E2E8F0; font-size: 0.95rem; line-height: 1.5; margin: 0; text-shadow: 0 2px 6px rgba(0,0,0,1);'>Access your secure portfolio to track rewards, monitor yields, and optimize benefits.</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button("Access The Vault", key="btn_obsidian_vault", use_container_width=True, type="primary"):
                st.session_state.current_page = "Optimization Hub"
                st.rerun()

elif st.session_state.current_page == "Guest Scout":
    from views.guest_scout import render_guest_scout
    render_guest_scout()
    
elif st.session_state.current_page == "Optimization Hub":
    from views.optimization_hub import render_optimization_hub
    render_optimization_hub()