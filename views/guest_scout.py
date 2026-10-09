# views/guest_scout.py
import streamlit as st

def render_guest_scout():
    # --- Navigation Logic ---
    if 'step' not in st.session_state:
        st.session_state.step = 1
    if 'user_data' not in st.session_state:
        st.session_state.user_data = {}

    # --- PAGE 1: PROFILE SCOUT ---
    if st.session_state.step == 1:
        data = st.session_state.user_data
        
        _, center_column, _ = st.columns([1, 2, 1]) 
        
        with center_column:
            with st.container(border=True):
                st.markdown("""
                <style>
                @keyframes glow {
                    0% { text-shadow: 0 0 10px rgba(6, 182, 212, 0.2), 0 0 20px rgba(6, 182, 212, 0.1); }
                    50% { text-shadow: 0 0 20px rgba(6, 182, 212, 0.5), 0 0 30px rgba(16, 185, 129, 0.3); }
                    100% { text-shadow: 0 0 10px rgba(6, 182, 212, 0.2), 0 0 20px rgba(6, 182, 212, 0.1); }
                }
                .glow-text {
                    font-size: 2.5rem; /* <-- Adjusted to a normal, clean size */
                    font-weight: 900; 
                    margin-bottom: 0; 
                    padding-bottom: 0; 
                    background: linear-gradient(90deg, #06B6D4, #10B981); 
                    -webkit-background-clip: text; 
                    -webkit-text-fill-color: transparent;
                    animation: glow 3s ease-in-out infinite;
                    filter: drop-shadow(0px 4px 8px rgba(0,0,0,0.5));
                }
                </style>
                
                <div style="text-align: center; margin-bottom: 25px;">
                    <h1 class="glow-text">🕵️ CardScout</h1>
                    <p style="font-size: 1.1rem; color: #94a3b8; letter-spacing: 2px; font-weight: 500; margin-top: 5px; opacity: 0.9;">
                        SMART DECISIONS, SMARTER REWARDS.
                    </p>
                </div>
            """, unsafe_allow_html=True)
                st.info("Step 1: Basic Information")
                
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
                
                col1, col2 = st.columns([5, 1])
                if col2.button("Next", icon=":material/arrow_forward:"):
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
            <h4 style="font-size: 2.5rem; font-weight: 800; margin-bottom: 0; padding-bottom: 0;">
                📊 <span style="background: linear-gradient(90deg, #3b82f6, #06B6D4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; color: transparent !important;">Expense Blueprint</span>
            </h4>
        </div>
    """, unsafe_allow_html=True)
                
                st.info("Step 2: Map your primary spending categories to help in calculating your maximum potential rewards.")
                
                spend_values = data.get('spending_categories', {})

                st.markdown("### 🔍 Select Main Preferences")
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
                st.markdown("### ➕ Custom Categories")
                
                if "custom_rows" not in st.session_state:
                    st.session_state.custom_rows = 0

                for i in range(st.session_state.custom_rows):
                    col1, col2 = st.columns([2, 1])
                    custom_name = col1.text_input(f"Category Name {i+1}", key=f"cust_name_{i}")
                    custom_amt = col2.number_input(f"Spend (₹)", min_value=0, value=1000, step=500, key=f"cust_amt_{i}")
                    if custom_name:
                        spend_values[custom_name] = custom_amt

                if st.button("Add Other Category", icon=":material/add:"):
                    st.session_state.custom_rows += 1
                    st.rerun()

                st.divider()
                st.markdown("### 🏦 Banking & Existing Cards")
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
                st.markdown("### 🎯 Reward Type Priority")

                reward_type = st.multiselect(
                    "How do you prefer to be rewarded?",
                    ["Direct Cashback", "Air Miles & Travel", "Reward Points (Shopping)", "Premium Lounge Access"],
                    default=data.get('reward_type', []) 
                )

                st.divider()
                st.markdown("### 💰 Fee Preference") 
                pref_options = ["Lifetime Free (LTF) Only", "High Rewards (Willing to pay fees)", "Any"]
                prev_pref = data.get('pref', "Any")
                pref_index = pref_options.index(prev_pref) if prev_pref in pref_options else 2
                pref = st.radio("Select your priority:", pref_options, index=pref_index, horizontal=True, label_visibility="collapsed")

                st.divider()
                col_back, col_next = st.columns([1, 5])
                
                if col_back.button("Back", icon=":material/arrow_back:"):
                    st.session_state.step = 1
                    st.rerun()
                    
                if col_next.button("Next", type="primary", icon=":material/arrow_forward:"):
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
        # Import our new AI agent
        from core.ai_agent import generate_card_roadmap, generate_battle_analysis
        import time
        
        data = st.session_state.user_data
        spends = data.get('spending_categories', {})

        # NEW: Edit Profile Button placed at the top left of Step 3
        col_back, _ = st.columns([2, 8])
        with col_back:
            if st.button("Edit Profile", icon=":material/arrow_back:", use_container_width=True):
                st.session_state.step = 2
                st.rerun()
        
        # 1. Title
        _, center_column, _ = st.columns([0.5, 3, 0.5])
        with center_column:
            st.markdown("""
                <div style="text-align: center; margin-bottom: 25px;">
                    <h4 style="font-size: 2.2rem; font-weight: 800; margin-bottom: 0; padding-bottom: 0;">
                        🧭 <span style="background: linear-gradient(90deg, #3b82f6, #06B6D4); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                            CardScout's Intelligence Hub
                        </span>
                    </h4>
                </div>
            """, unsafe_allow_html=True)

            # 2. Secure Execution of AI Generation
            if "final_recommendation" not in st.session_state:
                time.sleep(0.1) # UI Settle
                status_container = st.empty()
                
                with status_container.status("🔍 Analyzing your financial roadmap...", expanded=True) as status_bar:
                    # Call our isolated core function
                    result = generate_card_roadmap(data)
                    
                    if "Error" in result:
                        st.error(result)
                        st.stop()
                    else:
                        st.session_state.final_recommendation = result
                        status_bar.update(label="✅ Roadmap Generated!", state="complete", expanded=False)
                        status_container.empty()
                        st.rerun()

        # 3. Sidebar Snapshot
        with st.sidebar:
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(6, 182, 212, 0.1)); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 15px; margin-bottom: 20px; text-align: center;">
                    <div style="font-size: 2.5rem; margin-bottom: 5px;">👤</div>
                    <div style="color: #F8FAFC; font-weight: 700; font-size: 1.2rem; letter-spacing: 0.5px;">{data.get('name', 'User').upper()}</div>
                    <div style="display: inline-block; background: #06B6D4; color: #0b121e; font-size: 0.7rem; font-weight: 800; padding: 2px 8px; border-radius: 20px; text-transform: uppercase; margin-top: 5px;">Verified Profile</div>
                </div>
            """, unsafe_allow_html=True)
            
            st.subheader("👤 Profile Snapshot")
            with st.container(border=True):
                st.write(f"**Name:** {data.get('name', 'User')}")
                st.write(f"**Monthly Income:** ₹{data.get('income', 0):,}")

            if st.button("Edit Profile", icon=":material/edit:", use_container_width=True):
                if "final_recommendation" in st.session_state:
                    del st.session_state.final_recommendation
                st.session_state.step = 1
                st.rerun()

        # 4. Top Metrics
        col_rewards, col_odds, col_battle = st.columns(3, gap="medium")

        with col_rewards:
            with st.container(border=True):
                st.subheader("💰 Reward Potential")
                total_monthly_spend = sum(spends.values()) if spends else 0
                annual_savings = (total_monthly_spend * 0.03) * 12 
                st.metric(label="Total Annual Savings", value=f"₹{int(annual_savings):,}", delta="Optimized Rewards")

        with col_odds:
            with st.container(border=True):
                st.subheader("🎯 Approval Odds")
                score = data.get('credit', '< 700')
                odds, status, color = ("35%", "Challenging", "inverse") if score == "< 700" else ("85%", "Strong", "normal")
                st.metric(label="Likelihood for Top Pick", value=odds, delta=status, delta_color=color)

        # 5. Battleground Popup Definition
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
                st.subheader("🤖 The Battleground")
                st.write("Compare cards vs. Our Top pick.")
                user_card = st.text_input("Enter card name:", key="battle_input")
                if st.button("Battle Now", type="primary", use_container_width=True):
                    if user_card:
                        battle_popup(user_card, st.session_state.final_recommendation, data)

        # 6. Render Roadmap
        st.markdown("---")
        if "final_recommendation" in st.session_state:
            st.markdown("""
                <h2 style="color: #F8FAFC; border-left: 5px solid #06B6D4; padding-left: 15px;">Strategic Credit Acquisition Roadmap</h2>
            """, unsafe_allow_html=True)
            st.markdown(st.session_state.final_recommendation)
            
        # --- EXPORT & SHARE HUB ---
        st.markdown("---")
        from utils.export_tools import generate_pdf_report, get_share_links
        
        c1, c2, c3 = st.columns(3)
        
        # 1. Reset Button
        if c1.button("Start New Scout", use_container_width=True, icon=":material/refresh:", key="reset_p3"):
            if "final_recommendation" in st.session_state:
                del st.session_state.final_recommendation
            st.session_state.step = 1
            st.rerun()

        # 2. PDF Download
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

        # 3. Share Menu
        deploy_url, wa_url, mail_url = get_share_links(data.get('occ', 'Professional'))
        
        with c3.popover("Share link with friends", use_container_width=True, icon=":material/share:"):
            st.markdown("### 📢 Share CardScout")
            st.write("🔗 **Copy Link:**")
            st.code(deploy_url, language=None)
            st.divider()
            st.link_button("🟢 Share via WhatsApp", wa_url, use_container_width=True)
            st.link_button("📧 Share via Email", mail_url, use_container_width=True)