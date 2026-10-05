# views/guest_scout.py
import streamlit as st

def render_guest_scout():
    # --- Navigation Logic ---
    if 'step' not in st.session_state:
        st.session_state.step = 1
    if 'user_data' not in st.session_state:
        st.session_state.user_data = {}

    # --- THE MASTER UI OVERHAUL ---
    st.markdown("""
        <style>
        /* Sleek Typography */
        .scout-title {
            font-family: 'Inter', -apple-system, sans-serif !important;
            font-size: 3.2rem !important;
            font-weight: 700 !important;
            letter-spacing: -1px !important;
            margin-bottom: 0 !important;
            padding-bottom: 0 !important;
            line-height: 1.1 !important;
            text-shadow: 0px 4px 20px rgba(0, 0, 0, 0.6), 0px 0px 40px rgba(16, 185, 129, 0.2) !important;
        }
        .scout-subtitle {
            font-family: 'Inter', -apple-system, sans-serif !important;
            color: #D4AF37 !important; /* Metallic Gold */
            font-size: 0.95rem !important;
            letter-spacing: 3px !important;
            font-weight: 600 !important;
            margin-top: 5px !important;
            text-shadow: 0px 2px 5px rgba(0, 0, 0, 0.8) !important;
        }

        /* MASTER GLASSMORPHISM CONTAINER */
        [data-testid="stVerticalBlockBorderWrapper"] {
            background: linear-gradient(145deg, rgba(10, 20, 15, 0.6), rgba(4, 13, 8, 0.8)) !important;
            backdrop-filter: blur(12px) !important;
            border: 1px solid rgba(52, 211, 153, 0.2) !important;
            border-radius: 16px !important;
            box-shadow: 0 10px 40px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.05) !important;
            transition: transform 0.3s ease, box-shadow 0.3s ease, border 0.3s ease !important;
            padding: 10px !important;
        }
        [data-testid="stVerticalBlockBorderWrapper"]:hover {
            border: 1px solid rgba(212, 175, 55, 0.4) !important;
            box-shadow: 0 10px 40px rgba(0,0,0,0.6), 0 0 20px rgba(212, 175, 55, 0.15) !important;
        }

        /* Gold tint for all input labels */
        label[data-testid="stWidgetLabel"] p {
            color: #D4AF37 !important; 
            font-weight: 600 !important;
            letter-spacing: 0.5px !important;
            font-size: 0.95rem !important;
        }

        /* ----------------------------------------------------------- */
        /* --- THE PERFECT INPUT FIELD FIX --- */
        
        div[data-baseweb="input"],
        div[data-baseweb="select"] > div,
        [data-testid="stNumberInputStepDown"],
        [data-testid="stNumberInputStepUp"] {
            background-color: rgba(10, 15, 20, 0.75) !important; 
            backdrop-filter: blur(6px) !important; 
            border-color: rgba(255, 255, 255, 0.15) !important;
            transition: all 0.3s ease !important;
        }
        
        div[data-baseweb="select"] > div { border-radius: 8px !important; }
        
        div[data-baseweb="input"]:hover,
        div[data-baseweb="select"] > div:hover,
        div[data-baseweb="input"]:focus-within {
            border-color: #34D399 !important; 
            background-color: rgba(15, 22, 28, 0.85) !important;
            box-shadow: 0 0 8px rgba(52, 211, 153, 0.3) !important;
        }

        div[data-baseweb="base-input"],
        div[data-baseweb="base-input"] > input,
        div[data-baseweb="base-input"] > textarea {
            background-color: transparent !important;
            background: transparent !important;
            border: none !important;
        }
        
        input, .stSelectbox div, [data-testid="stNumberInputStepDown"], [data-testid="stNumberInputStepUp"] { 
            color: #F8FAFC !important; 
        }

        [data-testid="stNumberInputStepDown"]:hover,
        [data-testid="stNumberInputStepUp"]:hover {
            color: #34D399 !important;
            background-color: rgba(52, 211, 153, 0.15) !important;
            border-color: #34D399 !important;
        }
        /* ----------------------------------------------------------- */

        /* ----------------------------------------------------------- */
        /* --- NATIVE BUTTON SIZING --- */
        
        button[kind="secondary"], button[kind="primary"] {
            border-radius: 30px !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
        }

        /* Secondary Buttons (Top Nav, Add Category, Edit Profile) */
        button[kind="secondary"] {
            background: rgba(4, 13, 8, 0.6) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            color: #F8FAFC !important;
        }
        button[kind="secondary"]:hover {
            border-color: #D4AF37 !important;
            background: rgba(212, 175, 55, 0.15) !important;
            color: #FFFFFF !important;
        }

        /* Primary Buttons (Next Step, Back, Battle Now) */
        button[kind="primary"] {
            background: #08100C !important; 
            border: 1px solid #D4AF37 !important; 
            color: #F8FAFC !important;
            box-shadow: 0 4px 15px rgba(212, 175, 55, 0.1) !important;
        }
        button[kind="primary"]:hover {
            border-color: #F2D249 !important;
            background: #111A15 !important;
            color: #FFFFFF !important;
            box-shadow: 0 4px 20px rgba(212, 175, 55, 0.25) !important;
        }

        /* ----------------------------------------------------------- */
        /* --- DASHBOARD INTELLIGENCE HUB STYLING --- */

        /* Glassmorphism for the Loading Status Box */
        [data-testid="stStatusWidget"] {
            background: linear-gradient(145deg, rgba(10, 20, 15, 0.6), rgba(4, 13, 8, 0.8)) !important;
            backdrop-filter: blur(12px) !important;
            border: 1px solid rgba(52, 211, 153, 0.2) !important;
            border-radius: 12px !important;
            box-shadow: 0 10px 40px rgba(0,0,0,0.4) !important;
        }
        
        /* Force inner layers of the status box to be transparent */
        [data-testid="stStatusWidget"] details,
        [data-testid="stStatusWidget"] summary {
            background-color: transparent !important;
            background: transparent !important;
            color: #F8FAFC !important;
        }
        
        [data-testid="stStatusWidget"] summary:hover {
            background-color: rgba(52, 211, 153, 0.1) !important;
        }

        /* Error Box Styling */
        [data-testid="stNotification"] {
            background-color: rgba(220, 38, 38, 0.15) !important;
            backdrop-filter: blur(6px) !important;
            border: 1px solid rgba(220, 38, 38, 0.5) !important;
            color: #F8FAFC !important;
            border-radius: 8px !important;
        }

        /* Metric Numbers Styling */
        [data-testid="stMetricValue"] {
            color: #F8FAFC !important;
            font-weight: 800 !important;
        }

        /* Neon Multiselect tags */
        span[data-baseweb="tag"] {
            background-color: rgba(52, 211, 153, 0.15) !important;
            color: #34D399 !important;
            border: 1px solid rgba(52, 211, 153, 0.3) !important;
        }
        </style>
    """, unsafe_allow_html=True)

# --- PAGE 1: PROFILE SCOUT ---
    if st.session_state.step == 1:
        data = st.session_state.user_data
        
        _, center_column, _ = st.columns([1, 2, 1]) 
        
        with center_column:
            with st.container(border=True):
                st.markdown("""
                <div style="text-align: center; margin-bottom: 25px;">
                    <h1 class='scout-title'>
                        <span style='color: #FFFFFF;'>Card</span><span style='color: #34D399;'>Scout</span>
                    </h1>
                    <p class='scout-subtitle'>SMART DECISIONS, SMARTER REWARDS.</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("""
                    <div style="background: linear-gradient(90deg, rgba(52, 211, 153, 0.15), rgba(4, 13, 8, 0)); border-left: 4px solid #34D399; padding: 12px 20px; border-radius: 4px; margin-bottom: 25px;">
                        <span style="color: #34D399; font-weight: 700; font-size: 1.1rem; letter-spacing: 1px;">STEP 1 //</span>
                        <span style="color: #F8FAFC; font-weight: 500; font-size: 1.1rem; margin-left: 8px;">BASIC PROFILE</span>
                    </div>
                """, unsafe_allow_html=True)
                
                name = st.text_input("What should we call you?", value=data.get('name', ""), placeholder="Enter your name")
                age = st.number_input("Age", min_value=18, max_value=75, value=data.get('age', 18))
                
                occ_options = ["Salaried", "Self-employed Professional (Doc/CA)", "Business Owner", "Student", "Other..."]
                prev_occ = data.get('occ')
                occ_index = occ_options.index(prev_occ) if prev_occ in occ_options else None
                
                occ_choice = st.selectbox(
                    "Professional Profile",
                    options=occ_options,
                    index=occ_index,
                    placeholder="Select Profile...",
                )
                
                if occ_choice == "Other...":
                    occ = st.text_input("Please specify your occupation:", value=data.get('occ', "") if prev_occ not in occ_options else "")
                else:
                    occ = occ_choice

                tenure_options = ["Less than 6 Months", "6 - 12 Months", "1 - 2 Years", "More than 2 Years"]
                prev_tenure = data.get('tenure', "Less than 6 Months")
                tenure_index = tenure_options.index(prev_tenure) if prev_tenure in tenure_options else 0
                tenure = st.selectbox("Employment Stability", tenure_options, index=tenure_index)

                income = st.number_input("Monthly In-hand Salary (₹)", min_value=10000, value=data.get('income', 50000), step=5000)
                
                credit_options = ["< 700", "700 - 750", "> 750","Don't Know"]
                prev_credit = data.get('credit', "< 700")
                credit_index = credit_options.index(prev_credit) if prev_credit in credit_options else 0
                credit = st.radio("Estimated Credit Score", credit_options, index=credit_index, horizontal=True)

                st.divider()
                
                col_space, col_btn = st.columns([7, 3])
                if col_btn.button("Next Step", type="primary", use_container_width=True):
                    if not name: 
                        st.error("Please enter your name.")
                    elif occ_choice is None:
                        st.error("Please select a Professional Profile to proceed.")
                    elif occ_choice == "Other..." and not occ:
                        st.error("Please specify your occupation.")
                    else:
                        st.session_state.user_data.update({
                            "name": name, 
                            "age": age, 
                            "occ": occ, 
                            "tenure": tenure,
                            "income": income, 
                            "credit": credit
                        })
                        st.session_state.step = 2
                        st.rerun()

    # --- PAGE 2: REWARDS BLUEPRINT ---
    elif st.session_state.step == 2:
        data = st.session_state.user_data
        _, center_column, _ = st.columns([1, 2, 1])
        
        with center_column:
            with st.container(border=True):
                st.markdown("""
                <div style="text-align: center; margin-bottom: 25px;">
                    <h1 class='scout-title'>
                        <span style="color: #FFFFFF;">Expense </span><span style="color: #34D399;">Blueprint</span>
                    </h1>
                    <p class='scout-subtitle'>MAP YOUR REWARD POTENTIAL.</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("""
                    <div style="background: linear-gradient(90deg, rgba(212, 175, 55, 0.15), rgba(4, 13, 8, 0)); border-left: 4px solid #D4AF37; padding: 12px 20px; border-radius: 4px; margin-bottom: 25px;">
                        <span style="color: #D4AF37; font-weight: 700; font-size: 1.1rem; letter-spacing: 1px;">STEP 2 //</span>
                        <span style="color: #F8FAFC; font-weight: 500; font-size: 1.1rem; margin-left: 8px;">SPENDING HABITS</span>
                    </div>
                """, unsafe_allow_html=True)
                
                spend_values = data.get('spending_categories', {})

                st.markdown("<h3 style='color: #F8FAFC; font-size: 1.2rem; margin-bottom: 10px;'>🔍 Select Main Preferences</h3>", unsafe_allow_html=True)
                categories = {
                    "Travel & Forex": "t_in",
                    "Online Shopping": "s_in",
                    "Lifestyle (Dining & Movies)": "l_in",
                    "Essentials (Groceries & Quick Commerce)": "e_in",
                    "Utilities & Rent": "u_in",
                    "Transport (Fuel & UPI)": "tr_in"
                }

                for label, key in categories.items():
                    if st.checkbox(label, key=f"cb_{key}", value=label in spend_values):
                        spend_values[label] = st.number_input(
                            f"Monthly {label} Spend (₹)", min_value=0, value=spend_values.get(label, 2000), step=500, key=key
                        )

                st.divider()
                st.markdown("<h3 style='color: #F8FAFC; font-size: 1.2rem; margin-bottom: 10px;'>➕ Custom Categories</h3>", unsafe_allow_html=True)
                
                if "custom_rows" not in st.session_state:
                    st.session_state.custom_rows = 0

                for i in range(st.session_state.custom_rows):
                    col1, col2 = st.columns([2, 1])
                    custom_name = col1.text_input(f"Category Name {i+1}", key=f"cust_name_{i}")
                    custom_amt = col2.number_input(f"Spend (₹)", min_value=0, value=1000, step=500, key=f"cust_amt_{i}")
                    if custom_name:
                        spend_values[custom_name] = custom_amt

                if st.button("Add Other Category"):
                    st.session_state.custom_rows += 1
                    st.rerun()

                st.divider()
                st.markdown("<h3 style='color: #F8FAFC; font-size: 1.2rem; margin-bottom: 10px;'>🏦 Banking & Existing Cards</h3>", unsafe_allow_html=True)
                bank_col, card_col = st.columns(2)
                
                with bank_col:
                    existing_bank = st.multiselect(
                        "Current Bank Relation(s)",
                        ["HDFC", "ICICI", "SBI", "Axis", "Kotak", "Other"],
                        default=data.get('existing_banks', []),
                        help="Bank where you already have a Savings/Salary account."
                    )
                
                with card_col:
                    has_card = st.radio("Do you own a credit card?", ["No", "Yes"], index=1 if data.get('existing_card', "None") != "None" else 0, horizontal=True)
                    if has_card == "Yes":
                        current_card_name = st.text_input("Enter the name of your current card:", value=data.get('existing_card', ""))
                    else:
                        current_card_name = "None"

                st.divider()
                st.markdown("<h3 style='color: #F8FAFC; font-size: 1.2rem; margin-bottom: 10px;'>🎯 Reward Type Priority</h3>", unsafe_allow_html=True)

                base_rewards = ["Direct Cashback", "Air Miles & Travel", "Reward Points (Shopping)", "Premium Lounge Access"]
                
                def select_all_rewards():
                    if "All of the above" in st.session_state.reward_key:
                        st.session_state.reward_key = base_rewards

                if "reward_key" not in st.session_state:
                    st.session_state.reward_key = data.get('reward_type', [])

                reward_type = st.multiselect(
                    "How do you prefer to be rewarded?",
                    options=base_rewards + ["All of the above"],
                    key="reward_key",
                    on_change=select_all_rewards
                )

                st.divider()
                st.markdown("<h3 style='color: #F8FAFC; font-size: 1.2rem; margin-bottom: 10px;'>💰 Fee Preference</h3>", unsafe_allow_html=True) 
                pref_options = ["Lifetime Free (LTF) Only", "High Rewards (Willing to pay fees)", "Any"]
                prev_pref = data.get('pref', "Any")
                pref_index = pref_options.index(prev_pref) if prev_pref in pref_options else 2
                pref = st.radio("Select your priority:", pref_options, index=pref_index, horizontal=True, label_visibility="collapsed")

                st.divider()
                col_back, col_space, col_next = st.columns([3, 4, 3])
                
                if col_back.button("Back", type="primary", use_container_width=True):
                    st.session_state.step = 1
                    st.rerun()
                    
                if col_next.button("Next Step", type="primary", use_container_width=True):
                    st.session_state.user_data.update({
                        "spending_categories": spend_values,
                        "existing_banks": existing_bank,
                        "existing_card": current_card_name,
                        "reward_type": reward_type,
                        "pref": pref
                    })
                    st.session_state.step = 3
                    st.rerun()
                    
    # --- PAGE 3: THE PODIUM & AI DASHBOARD ---
    elif st.session_state.step == 3:
        from core.ai_agent import generate_card_roadmap, generate_battle_analysis
        import time
        
        data = st.session_state.user_data
        spends = data.get('spending_categories', {})
        
        _, center_column, _ = st.columns([0.5, 3, 0.5])
        with center_column:
            st.markdown("""
                <div style="text-align: center; margin-bottom: 25px;">
                    <h1 class='scout-title'>
                        <span style="color: #FFFFFF;">Intelligence </span><span style="color: #34D399;">Hub</span>
                    </h1>
                    <p class='scout-subtitle'>YOUR PERSONALIZED ROADMAP.</p>
                </div>
            """, unsafe_allow_html=True)

            if "final_recommendation" not in st.session_state:
                time.sleep(0.1) 
                status_container = st.empty()
                
                with status_container.status("🔍 Analyzing your financial roadmap...", expanded=True) as status_bar:
                    result = generate_card_roadmap(data)
                    
                    if "Error" in result:
                        st.error(result)
                        st.stop()
                    else:
                        st.session_state.final_recommendation = result
                        status_bar.update(label="✅ Roadmap Generated!", state="complete", expanded=False)
                        status_container.empty()
                        st.rerun()

        # Sidebar Snapshot
        with st.sidebar:
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, rgba(52, 211, 153, 0.1), rgba(4, 13, 8, 0.4)); border: 1px solid rgba(52, 211, 153, 0.3); border-radius: 12px; padding: 15px; margin-bottom: 20px; text-align: center;">
                    <div style="font-size: 2.5rem; margin-bottom: 5px;">👤</div>
                    <div style="color: #F8FAFC; font-weight: 700; font-size: 1.2rem; letter-spacing: 0.5px;">{data.get('name', 'User').upper()}</div>
                    <div style="display: inline-block; background: #D4AF37; color: #0b121e; font-size: 0.7rem; font-weight: 800; padding: 2px 8px; border-radius: 20px; text-transform: uppercase; margin-top: 5px;">Verified Profile</div>
                </div>
            """, unsafe_allow_html=True)
            
            st.subheader("👤 Profile Snapshot")
            with st.container(border=True):
                st.write(f"**Name:** {data.get('name', 'User')}")
                st.write(f"**Monthly Income:** ₹{data.get('income', 0):,}")

            if st.button("Edit Profile", use_container_width=True):
                if "final_recommendation" in st.session_state:
                    del st.session_state.final_recommendation
                st.session_state.step = 1
                st.rerun()

        # Top Metrics
        col_rewards, col_odds, col_battle = st.columns(3, gap="medium")

        with col_rewards:
            with st.container(border=True):
                st.markdown("<h3 style='color: #34D399; font-size: 1.1rem; margin-bottom: 5px;'>💰 Reward Potential</h3>", unsafe_allow_html=True)
                total_monthly_spend = sum(spends.values()) if spends else 0
                annual_savings = (total_monthly_spend * 0.03) * 12 
                st.metric(label="Total Annual Savings", value=f"₹{int(annual_savings):,}", delta="Optimized Rewards")

        with col_odds:
            with st.container(border=True):
                st.markdown("<h3 style='color: #34D399; font-size: 1.1rem; margin-bottom: 5px;'>🎯 Approval Odds</h3>", unsafe_allow_html=True)
                score = data.get('credit', '< 700')
                odds, status, color = ("35%", "Challenging", "inverse") if score == "< 700" else ("85%", "Strong", "normal")
                st.metric(label="Likelihood for Top Pick", value=odds, delta=status, delta_color=color)

        @st.dialog("⚔️ Card Battle: Peer-to-Peer Analysis", width="large")
        def battle_popup(entered_card, original_recommendation, user_context):
            st.write(f"### 🏆 Our Top Pick vs. {entered_card}")
            with st.spinner("Analyzing battle metrics..."):
                analysis = generate_battle_analysis(entered_card, original_recommendation, user_context)
                st.markdown(analysis)
            if st.button("Close Analysis", use_container_width=True):
                st.rerun()

        with col_battle:
            with st.container(border=True):
                st.markdown("<h3 style='color: #D4AF37; font-size: 1.1rem; margin-bottom: 5px;'>🤖 The Battleground</h3>", unsafe_allow_html=True)
                st.write("Compare cards vs. Our Top pick.")
                user_card = st.text_input("Enter card name:", key="battle_input", label_visibility="collapsed")
                if st.button("Battle Now", type="primary", use_container_width=True):
                    if user_card:
                        battle_popup(user_card, st.session_state.final_recommendation, data)

        # Render Roadmap
        st.markdown("---")
        if "final_recommendation" in st.session_state:
            st.markdown("""
                <h2 style="color: #F8FAFC; border-left: 5px solid #D4AF37; padding-left: 15px;">Strategic Credit Acquisition Roadmap</h2>
            """, unsafe_allow_html=True)
            st.markdown(st.session_state.final_recommendation)
            
        # --- EXPORT & SHARE HUB ---
        st.markdown("---")
        from utils.export_tools import generate_pdf_report, get_share_links
        
        c1, c2, c3 = st.columns(3)
        
        if c1.button("Start New Scout", use_container_width=True, key="reset_p3"):
            if "final_recommendation" in st.session_state:
                del st.session_state.final_recommendation
            st.session_state.step = 1
            st.rerun()

        if "final_recommendation" in st.session_state:
            pdf_bytes = generate_pdf_report(data.get('name', 'User'), st.session_state.final_recommendation)
            if pdf_bytes:
                c2.download_button(
                    "📥 Download Report", 
                    data=pdf_bytes, 
                    file_name=f"CardScout_{data.get('name', 'User')}.pdf", 
                    mime="application/pdf", 
                    use_container_width=True
                )
            else:
                c2.button("⚠️ PDF Error", disabled=True, use_container_width=True)

        deploy_url, wa_url, mail_url = get_share_links(data.get('occ', 'Professional'))
        
        with c3.popover("Share link with friends", use_container_width=True):
            st.markdown("### 📢 Share CardScout")
            st.write("🔗 **Copy Link:**")
            st.code(deploy_url, language=None)
            st.divider()
            st.link_button("🟢 Share via WhatsApp", wa_url, use_container_width=True)
            st.link_button("📧 Share via Email", mail_url, use_container_width=True)