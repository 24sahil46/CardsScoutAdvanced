# views/optimization_hub.py
import streamlit as st
import pandas as pd
import time
from core.ai_agent import (
    get_fee_waiver_target, 
    get_forex_markup, 
    fetch_live_card_offers, 
    get_hidden_milestones, 
    get_utility_cashback_rate,
    get_reward_point_values,     
    get_fee_and_penalty_audit    
)
from core.db_manager import (
    create_user, 
    verify_user, 
    add_subscription, 
    get_subscriptions,
    delete_subscription,
    add_wallet_card, 
    remove_wallet_card, 
    update_wallet_limit, 
    get_wallet_cards
)

def render_optimization_hub():
    # --- VAULT MASTER THEME INJECTION ---
    st.markdown("""
        <style>
        /* ISOLATED VAULT TYPOGRAPHY (Fixes CSS Bleed) */
        .vault-title {
            font-family: 'Inter', -apple-system, sans-serif !important;
            font-size: 3.2rem !important;
            font-weight: 700 !important;
            letter-spacing: -1px !important;
            margin-bottom: 0 !important;
            padding-bottom: 0 !important;
            line-height: 1.1 !important;
            color: #FFFFFF !important;
            text-shadow: 0px 4px 20px rgba(0, 0, 0, 0.6), 0px 0px 40px rgba(52, 211, 153, 0.2) !important;
        }
        .vault-subtitle {
            font-family: 'Inter', -apple-system, sans-serif !important;
            color: #D4AF37 !important; 
            font-size: 0.95rem !important;
            letter-spacing: 3px !important;
            font-weight: 600 !important;
            margin-top: 5px !important;
            text-shadow: 0px 2px 5px rgba(0, 0, 0, 0.8) !important;
            text-transform: uppercase !important;
        }

        /* 1. MASTER CONTAINER (Dark Frosted Glass Overlay) */
        [data-testid="stVerticalBlockBorderWrapper"] {
            background: rgba(0, 0, 0, 0.45) !important;
            backdrop-filter: blur(10px) !important;
            -webkit-backdrop-filter: blur(10px) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 12px !important;
            padding: 30px !important;
            box-shadow: 0 10px 40px rgba(0,0,0,0.5) !important;
        }

        /* 2. SOLID DARK INPUT FIELDS */
        .stTextInput > div > div > div,
        .stNumberInput > div > div > div,
        .stSelectbox > div > div > div,
        .stMultiSelect > div > div > div {
            background-color: #08100C !important; 
            background: #08100C !important;
            border: 1px solid rgba(52, 211, 153, 0.2) !important;
            border-radius: 8px !important;
            transition: all 0.2s ease !important;
        }

        .stTextInput input,
        .stNumberInput input,
        [data-baseweb="base-input"] {
            background-color: transparent !important;
            background: transparent !important;
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
        }

        div[data-baseweb="popover"] > div,
        ul[data-baseweb="menu"] {
            background-color: #08100C !important; 
            background: #08100C !important;
            border: 1px solid rgba(52, 211, 153, 0.3) !important;
            border-radius: 8px !important;
        }

        li[role="option"] {
            background-color: transparent !important;
            color: #FFFFFF !important;
        }

        li[role="option"]:hover,
        li[role="option"][aria-selected="true"] {
            background-color: rgba(52, 211, 153, 0.15) !important;
            color: #34D399 !important;
        }

        .stTextInput > div > div > div:hover,
        .stSelectbox > div > div > div:hover,
        .stTextInput > div > div > div:focus-within,
        .stSelectbox > div > div > div:focus-within {
            background-color: #0A1611 !important;
            border-color: #34D399 !important;
            box-shadow: 0 0 8px rgba(52, 211, 153, 0.2) !important;
        }

        /* 3. FIX OVERLAPPING ICON TEXT BUGS */
        [data-testid="stExpanderToggleIcon"] { 
            display: none !important; 
            font-size: 0px !important;
            color: transparent !important;
        }
        [data-testid="stExpander"] summary span {
            color: transparent !important; 
        }
        [data-testid="stTextInput"] div[data-baseweb="input"] > *:not([data-baseweb="base-input"]) {
            color: transparent !important; 
            font-size: 0px !important;
            line-height: 0 !important;
        }
        [data-testid="stTextInput"] div[data-baseweb="input"] > *:not([data-baseweb="base-input"]) svg {
            fill: #94A3B8 !important;
        }

        /* 4. PRIMARY & SECONDARY BUTTONS (FIXED PADDING AND SHAPE) */
        button[kind="primary"] {
            background-color: #34D399 !important; 
            color: #040D08 !important; 
            border: none !important;
            border-radius: 30px !important; 
            height: 48px !important;
            padding: 0 24px !important; /* Forces breathing room for text */
            font-weight: 700 !important;
            font-size: 1.05rem !important;
            box-shadow: 0 4px 15px rgba(52, 211, 153, 0.2) !important;
            transition: all 0.2s ease !important;
        }
        button[kind="primary"]:hover {
            background-color: #2bb381 !important; 
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(52, 211, 153, 0.4) !important;
            color: #000000 !important;
        }
        
        button[kind="secondary"] {
            background-color: rgba(255, 255, 255, 0.1) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            color: #FFFFFF !important;
            border-radius: 30px !important;
            padding: 0 24px !important; /* Forces breathing room for text */
            font-weight: 600 !important;
        }
        button[kind="secondary"]:hover {
            background-color: rgba(52, 211, 153, 0.15) !important;
            border-color: #34D399 !important;
            color: #34D399 !important;
        }

        /* 5. SLEEK TABS STYLING */
        button[data-baseweb="tab"] {
            background-color: transparent !important;
            color: #94A3B8 !important; 
            font-weight: 600 !important;
            font-size: 0.95rem !important;
            border-bottom: 2px solid transparent !important;
            padding: 10px 15px !important;
            transition: all 0.3s ease !important;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            color: #34D399 !important; 
            border-bottom: 2px solid #34D399 !important;
        }
        button[data-baseweb="tab"]:hover {
            color: #F8FAFC !important;
        }

        /* 6. EXPANDER STYLING (Digital Wallet Theme Match) */
        [data-testid="stExpander"] {
            background-color: #08100C !important;
            border: 1px solid rgba(52, 211, 153, 0.3) !important;
            border-radius: 8px !important;
        }
        [data-testid="stExpander"] summary {
            background-color: transparent !important;
        }
        [data-testid="stExpander"] summary p {
            color: #34D399 !important; 
            font-weight: 700 !important;
            font-size: 1.05rem !important;
            visibility: visible !important;
        }
        [data-testid="stExpander"] summary:hover p {
            color: #F8FAFC !important;
        }

        /* 7. AUTH RADIO BUTTONS */
        div[role="radiogroup"] {
            justify-content: center !important;
            gap: 15px !important;
            margin-bottom: 20px !important;
        }
        div[role="radiogroup"] > label {
            background-color: #08100C !important;
            padding: 10px 30px !important;
            border-radius: 50px !important;
            border: 1px solid rgba(52, 211, 153, 0.3) !important;
            transition: all 0.3s ease !important;
            cursor: pointer !important;
        }
        div[role="radiogroup"] > label:hover {
            border-color: #34D399 !important;
            box-shadow: 0 0 10px rgba(52, 211, 153, 0.2) !important;
        }
        div[role="radiogroup"] > label div[data-baseweb="radio"] > div:first-child {
            display: none !important;
        }
        div[role="radiogroup"] > label[aria-checked="true"] {
            background: #34D399 !important;
            border: none !important;
        }
        div[role="radiogroup"] > label p {
            color: #94A3B8 !important;
            font-weight: 600 !important;
            font-size: 15px !important;
            margin: 0 !important;
        }
        div[role="radiogroup"] > label[aria-checked="true"] p {
            color: #040D08 !important;
            font-weight: 700 !important;
        }
        
        /* 8. SUCCESS ALERTS */
        [data-testid="stAlert"] {
            background-color: rgba(52, 211, 153, 0.1) !important;
            border: 1px solid rgba(52, 211, 153, 0.3) !important;
            border-radius: 8px !important;
            color: #F8FAFC !important;
        }
        [data-testid="stAlert"] div[data-testid="stMarkdownContainer"] p {
            color: #F8FAFC !important;
            font-weight: 600 !important;
        }
        
        /* Password Masking Fallback */
        div[data-testid="stCheckbox"] input[aria-checked="false"] ~ * /* fallback styling */
        input[aria-label="Password"] {
            -webkit-text-security: disc;
        }
        </style>
    """, unsafe_allow_html=True)
    
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    # ==========================================
    # IF LOGGED IN: SHOW THE DYNAMIC DASHBOARD
    # ==========================================
    if st.session_state.logged_in:
        
        st.markdown("""
            <div style="text-align: center; margin-bottom: 30px; margin-top: 10px;">
                <h1 class='vault-title'>
                    <span>💎 The Obsidian </span><span style="color: #34D399;">Vault</span>
                </h1>
                <p class='vault-subtitle'>Active Yield & Subscription Command</p>
            </div>
        """, unsafe_allow_html=True)

        if 'wallet_loaded' not in st.session_state:
            saved_cards = get_wallet_cards(st.session_state.username)
            st.session_state.wallet = [card[0] for card in saved_cards]
            st.session_state.card_limits = {card[0]: card[1] for card in saved_cards}
            st.session_state.wallet_loaded = True

        # Top Header & Logout
        col_title, col_logout = st.columns([4, 1])
        col_title.success(f"Welcome back, {st.session_state.username.capitalize()}!")
        
        if col_logout.button("🚪 Secure Logout", use_container_width=True):
            st.session_state.logged_in = False
            for key in ['username', 'wallet', 'card_limits', 'wallet_loaded']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

        # --- DIGITAL WALLET SECTION ---
        with st.expander("💳 My Digital Wallet (Add & Manage your cards here)", expanded=len(st.session_state.wallet) == 0):
            
            c_input, c_limit, c_btn = st.columns([3, 2, 1])
            new_card = c_input.text_input("Enter a credit card:", placeholder="e.g., HDFC Regalia")
            card_limit = c_limit.number_input("Monthly Credit Limit (₹):", min_value=5000, step=10000, value=50000)
            
            c_btn.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
            if c_btn.button("Add to Wallet", type="secondary", use_container_width=True):
                if new_card and new_card not in st.session_state.wallet:
                    st.session_state.wallet.append(new_card)
                    st.session_state.card_limits[new_card] = card_limit
                    add_wallet_card(st.session_state.username, new_card, card_limit)
                    st.rerun()
            
            st.markdown("---")
            
            if st.session_state.wallet:
                st.write("**Your Active Cards (Modify limit or remove):**")
                
                for card in list(st.session_state.wallet):
                    col_name, col_edit, col_del = st.columns([3, 2, 1])
                    col_name.markdown(f"<div style='margin-top: 8px;'>💳 <b>{card}</b></div>", unsafe_allow_html=True)
                    
                    current_limit = int(st.session_state.card_limits.get(card, 50000))
                    new_limit = col_edit.number_input("Edit Limit", value=current_limit, step=10000, key=f"edit_limit_{card}", label_visibility="collapsed")
                    
                    if new_limit != current_limit:
                        st.session_state.card_limits[card] = new_limit
                        update_wallet_limit(st.session_state.username, card, new_limit)
                    
                    if col_del.button("❌ Remove", key=f"del_{card}", use_container_width=True):
                        st.session_state.wallet.remove(card)
                        if card in st.session_state.card_limits:
                            del st.session_state.card_limits[card]
                        remove_wallet_card(st.session_state.username, card)
                        st.rerun()

        st.markdown("---")

        tab_waiver, tab_offers, tab_milestones, tab_sub, tab_forex, tab_points, tab_audit = st.tabs([
            "⏳ Fee Waiver Pacing", 
            "📡 Live Offers Radar",
            "🏆 Milestone Rewards",
            "🔄 Subscription Saver", 
            "✈ Forex Engine",
            "💎 Point Valuation",    
            "⚖️ Penalty Audit"      
        ])

        # --- TAB 1: FEE WAIVER PACING ---
        with tab_waiver:
            st.markdown("<h3 style='color: #F8FAFC;'>Fee Waiver Pace Tracker</h3>", unsafe_allow_html=True)
            st.write("Track if you are spending enough to get your annual fee waived.")
            
            if not st.session_state.wallet:
                st.warning("⚠️ Please add a card to your Digital Wallet above.")
            else:
                c_sel, c_btn = st.columns([3, 1])
                selected_track_card = c_sel.selectbox("Select card to track:", st.session_state.wallet, key="waiver_card")
                
                c_btn.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
                if c_btn.button("Track Waiver", type="primary", use_container_width=True, key="btn_w"):
                    with st.spinner("AI fetching real fee waiver targets..."):
                        st.session_state[f"waiver_{selected_track_card}"] = get_fee_waiver_target(selected_track_card)
                
                target_spend = st.session_state.get(f"waiver_{selected_track_card}")
                
                if target_spend is not None:
                    if target_spend == 0:
                        st.info("ℹ️ **No Spend Target Required**")
                        st.write("The AI detects this card either does not offer a spend-based waiver (e.g., it charges a strict fixed fee but gives renewal bonus points) or it is Lifetime Free. You do not need to force unnecessary spending on this card just to chase a waiver!")
                    else:
                        col1, col2 = st.columns(2)
                        ytd_spend = col1.number_input("Your Actual Current Spend (₹)", min_value=0, max_value=target_spend*2, value=0, step=5000)
                        months_left = col2.slider("Months until card renewal", 1, 12, 6)
                        
                        amount_left = max(0, target_spend - ytd_spend)
                        
                        st.metric("Target Spend for Waiver", f"₹{target_spend:,}", delta=f"₹{amount_left:,} remaining", delta_color="inverse")
                        
                        if amount_left == 0:
                            st.success("🎉 You have already hit the waiver target! Don't stress about spending on this card.")
                        else:
                            req_monthly = amount_left / months_left
                            st.markdown("---")
                            st.markdown(f"**The Pacing Math:** You need to spend **₹{req_monthly:,.0f} / month** for the next {months_left} months to waive your fee.")
                            
                            card_limit = st.session_state.card_limits.get(selected_track_card, 50000)
                            utilization = req_monthly / card_limit if card_limit > 0 else 1.0
                            
                            if utilization > 0.30:
                                st.error(f"🔴 **VERDICT: HOLD.** This requires a **{utilization*100:.1f}% monthly utilization** of your ₹{card_limit:,} limit. Exceeding the 30% Golden Rule will damage your CIBIL score. Pay the fee or split spends across other cards.")
                            elif req_monthly > 25000:
                                st.warning(f"🟡 **VERDICT: CAUTION.** Your utilization is safe ({utilization*100:.1f}%), but ₹{req_monthly:,.0f}/month is a high cash flow requirement. Do not force unnecessary spending just to save a small fee.")
                            else:
                                st.success(f"🟢 **VERDICT: SWIPE.** Safe **{utilization*100:.1f}% utilization**. Route your regular groceries and utilities to this card to easily clear the waiver.")

        # --- TAB 2: LIVE OFFERS RADAR ---
        with tab_offers:
            st.markdown("<h3 style='color: #F8FAFC;'>Live Offers & Sales Radar</h3>", unsafe_allow_html=True)
            st.caption("AI-powered radar tracking active discounts across E-Commerce, Dining, Flights, IRCTC Trains, and Fuel pumps.")
            
            if not st.session_state.wallet:
                st.warning("⚠️ Please add a card to your Digital Wallet above to scan for offers.")
            else:
                c_sel, c_btn = st.columns([3, 1])
                selected_offer_card = c_sel.selectbox("Select card to scan:", st.session_state.wallet, key="offer_scan")
                
                c_btn.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
                if c_btn.button("📡 Scan Web", type="primary", use_container_width=True):
                    with st.spinner(f"Scanning web for flights, trains, fuel, dining & shopping deals on '{selected_offer_card}'..."):
                        offers_data = fetch_live_card_offers(selected_offer_card)
                        st.session_state[f"offers_{selected_offer_card}"] = offers_data

                saved_offers = st.session_state.get(f"offers_{selected_offer_card}")
                if saved_offers:
                    st.markdown("---")
                    st.markdown(saved_offers, unsafe_allow_html=True)

        # --- TAB 3: MILESTONE REWARDS ---
        with tab_milestones:
            st.markdown("<h3 style='color: #F8FAFC;'>Hidden Milestone Rewards</h3>", unsafe_allow_html=True)
            st.caption("Discover high-value bonuses (like flight tickets or hotel vouchers) triggered by hitting annual spending limits.")
            
            if not st.session_state.wallet:
                st.warning("⚠️ Please add a card to your Digital Wallet above.")
            else:
                c_sel, c_btn = st.columns([3, 1])
                milestone_card = c_sel.selectbox("Select card to analyze:", st.session_state.wallet, key="milestone_card")
                
                c_btn.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
                if c_btn.button("🔍 Scan Milestones", type="primary", use_container_width=True):
                    with st.spinner(f"Extracting milestone data for {milestone_card}..."):
                        milestones_data = get_hidden_milestones(milestone_card)
                        st.session_state[f"milestones_{milestone_card}"] = milestones_data
                
                saved_milestones = st.session_state.get(f"milestones_{milestone_card}")
                if saved_milestones:
                    st.markdown("---")
                    st.markdown(saved_milestones, unsafe_allow_html=True)

        # --- TAB 4: SUBSCRIPTION SAVER ---
        with tab_sub:
            st.markdown("<h3 style='color: #F8FAFC;'>Active Digital Subscriptions</h3>", unsafe_allow_html=True)
            st.write("Route your recurring bills to your highest-yielding cards.")
            
            if not st.session_state.wallet:
                st.warning("⚠ Please add at least one card to your Digital Wallet above to optimize subscriptions.")
            else:
                c1, c2, c3, c4 = st.columns([2, 1, 1.5, 1])
                sub_name = c1.text_input("Service Name", placeholder="e.g., Netflix")
                sub_amt = c2.number_input("Monthly Cost (₹)", min_value=0.0, step=100.0)
                sub_card = c3.selectbox("Pay Using:", st.session_state.wallet)
                
                c4.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
                if c4.button("Add Bill", type="primary", use_container_width=True):
                    if sub_name and sub_amt > 0:
                        add_subscription(st.session_state.username, sub_name, sub_amt, sub_card)
                        st.toast(f"Added {sub_name} routed to {sub_card}!")
                        st.rerun() 
                    else:
                        st.error("Please enter a valid service name and amount.")
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                raw_subs = get_subscriptions(st.session_state.username)
                valid_subs = []
                needs_sync_rerun = False
                
                if raw_subs:
                    for sub in raw_subs:
                        db_service, db_amt, db_card = sub[0], sub[1], sub[2]
                        if db_card not in st.session_state.wallet:
                            delete_subscription(st.session_state.username, db_service, db_card)
                            needs_sync_rerun = True
                        else:
                            valid_subs.append(sub)
                            
                if needs_sync_rerun:
                    st.rerun() 
                
                if valid_subs:
                    st.markdown("<h3 style='color: #F8FAFC;'>📊 Subscription Analytics</h3>", unsafe_allow_html=True)
                    
                    df = pd.DataFrame(valid_subs, columns=["Service", "Monthly (₹)", "Card Used"])
                    df["Action"] = "🟢 Active"
                    
                    unique_cards = df["Card Used"].unique().tolist()
                    filter_options = ["All Cards"] + unique_cards
                    selected_filter = st.selectbox("Filter Dashboard by Card:", filter_options, label_visibility="collapsed")
                    
                    if selected_filter != "All Cards":
                        filtered_df = df[df["Card Used"] == selected_filter]
                    else:
                        filtered_df = df

                    st.dataframe(filtered_df, use_container_width=True, hide_index=True)
                    
                    total_monthly = filtered_df["Monthly (₹)"].sum()
                    annual_spend = total_monthly * 12
                    
                    if selected_filter != "All Cards":
                        services_list = ", ".join(filtered_df["Service"].unique())
                        with st.spinner(f"AI calculating exact yield for {services_list}..."):
                            actual_rate = get_utility_cashback_rate(selected_filter, services_list)
                        est_annual_yield = annual_spend * (actual_rate / 100)
                        yield_label = f"({actual_rate}% Actual Value-Back)"
                    else:
                        est_annual_yield = annual_spend * 0.02 
                        yield_label = "(~2.0% Estimated Mixed Yield)"
                    
                    st.markdown(f"""
                    <div style="display: flex; gap: 15px; margin-top: 10px; margin-bottom: 20px;">
                        <div style="flex: 1; background: #08100C; border: 1px solid rgba(52, 211, 153, 0.2); border-radius: 10px; padding: 15px; text-align: center;">
                            <p style="color: #94A3B8; margin: 0; font-size: 14px; text-transform: uppercase; letter-spacing: 1px;">Annual Auto-Debits</p>
                            <h3 style="color: #E2E8F0; margin: 5px 0 0 0; font-size: 1.8rem;">₹{annual_spend:,.0f}</h3>
                        </div>
                        <div style="flex: 1; background: #08100C; border: 1px solid rgba(239, 68, 68, 0.4); border-radius: 10px; padding: 15px; text-align: center;">
                            <p style="color: #ef4444; margin: 0; font-size: 14px; text-transform: uppercase; letter-spacing: 1px;">UPI / Debit Yield</p>
                            <h3 style="color: #ef4444; margin: 5px 0 0 0; font-size: 1.8rem;">₹0</h3>
                        </div>
                        <div style="flex: 1; background: #34D399; border: none; border-radius: 10px; padding: 15px; text-align: center; box-shadow: 0 4px 15px rgba(52, 211, 153, 0.2);">
                            <p style="color: #040D08; margin: 0; font-size: 14px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px;">Credit Card Yield</p>
                            <h3 style="color: #040D08; margin: 5px 0 0 0; font-size: 1.8rem; font-weight: 800;">₹{est_annual_yield:,.0f}</h3>
                            <p style="color: #040D08; margin: 5px 0 0 0; font-size: 12px; font-weight: 600;">{yield_label}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    with st.expander("🗑️ Delete a tracked bill"):
                        df["Unique_ID"] = df["Service"] + " (paid via " + df["Card Used"] + ")"
                        del_col1, del_col2 = st.columns([3, 1])
                        target_unique = del_col1.selectbox("Select bill to delete:", df["Unique_ID"].unique(), label_visibility="collapsed")
                        
                        del_col2.markdown("<div style='margin-top: 0px;'></div>", unsafe_allow_html=True)
                        if del_col2.button("Delete Bill", type="secondary", use_container_width=True):
                            selected_row = df[df["Unique_ID"] == target_unique].iloc[0]
                            delete_subscription(st.session_state.username, selected_row["Service"], selected_row["Card Used"])
                            st.toast(f"Removed {selected_row['Service']} from tracking.")
                            st.rerun()
                else:
                    st.write("No active subscriptions tracked yet. Add your first bill above!")

        # --- TAB 5: FOREX ENGINE ---
        with tab_forex:
            st.markdown("<h3 style='color: #F8FAFC;'>Cross-Border Forex Optimizer</h3>", unsafe_allow_html=True)
            
            if not st.session_state.wallet:
                st.warning("⚠️ Please add a card to your Digital Wallet above to analyze Forex markups.")
            else:
                col_fx1, col_fx2 = st.columns(2)
                with col_fx1:
                    currency = st.selectbox("Destination Currency", ["USD ($)", "EUR (€)", "GBP (£)", "AED (د.إ)"])
                    budget = st.number_input("Estimated Trip Budget (In Foreign Currency)", min_value=0, value=2500, step=500)
                
                with col_fx2:
                    travel_card = st.selectbox("Card to use abroad:", st.session_state.wallet, key="forex_card")
                    
                    st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
                    if st.button("✈️ Analyze Forex Fees", key="btn_fx", type="primary", use_container_width=True):
                        with st.spinner("AI analyzing actual markup rates..."):
                            st.session_state[f"forex_{travel_card}"] = get_forex_markup(travel_card)
                    
                ai_markup_rate = st.session_state.get(f"forex_{travel_card}", 3.5)
                current_markup = st.slider(f"Confirmed Forex Markup for {travel_card} (%)", 0.0, 5.0, ai_markup_rate, step=0.1)
                    
                conversion_rate = 83 if "USD" in currency else 90 if "EUR" in currency else 105 if "GBP" in currency else 22
                inr_budget = budget * conversion_rate
                markup_fee = inr_budget * (current_markup / 100)
                tax_tcs = markup_fee * 0.18
                total_loss = markup_fee + tax_tcs
                
                st.markdown("---")
                c_loss, c_save = st.columns(2)
                c_loss.metric(f"Penalty using {travel_card}", f"₹{total_loss:,.0f}", delta=f"-{current_markup}% Markup", delta_color="inverse")
                
                with c_save:
                    if total_loss > 0:
                        st.success(f"**Action:** Apply for a Zero-Forex card like IDFC First Wealth or Scapia to save **₹{total_loss:,.0f}** on this trip.")
                    else:
                        st.success(f"**Action:** Great choice! {travel_card} has 0% markup. Swipe away!")
                
                st.markdown("""
                    <div style="margin-top: 15px; padding: 12px; border-left: 3px solid #F59E0B; background-color: rgba(245, 158, 11, 0.1); border-radius: 5px;">
                        <p style="color: #FCD34D; margin: 0; font-size: 13px; line-height: 1.4;">
                            <b>⚠️ Hidden Tax Disclaimer:</b> Indian banks levy an additional <b>18% GST</b> on the calculated forex markup fee amount. A <b>1% Dynamic Currency Conversion (DCC) fee</b> (+ GST) may also apply if you choose to be billed in INR at an international payment terminal.
                        </p>
                    </div>
                """, unsafe_allow_html=True)

        # --- TAB 6: REWARD POINT MATRIX ---
        with tab_points:
            st.markdown("<h3 style='color: #F8FAFC;'>💎 Reward Point Conversion Matrix</h3>", unsafe_allow_html=True)
            st.write("Stop redeeming points blindly. See the exact INR value of your balance across redemption channels.")
            
            if not st.session_state.wallet:
                st.warning("⚠️ Please add a card to your Digital Wallet above.")
            else:
                col_pt1, col_pt2, col_pt3 = st.columns([2, 1.5, 1.5])
                pt_card = col_pt1.selectbox("Select Card to Evaluate:", st.session_state.wallet, key="pt_card")
                pt_balance = col_pt2.number_input("Current Point Balance", min_value=0, value=10000, step=1000)
                
                col_pt3.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
                if col_pt3.button("Evaluate Points", key="btn_pts", type="primary", use_container_width=True):
                    with st.spinner(f"AI scraping live valuation multipliers for {pt_card}..."):
                        st.session_state[f"pts_{pt_card}"] = get_reward_point_values(pt_card)
                
                pt_data = st.session_state.get(f"pts_{pt_card}")
                
                if pt_data:
                    cash_val = pt_balance * pt_data.get("cash_rate", 0)
                    voucher_val = pt_balance * pt_data.get("voucher_rate", 0)
                    travel_val = pt_balance * pt_data.get("travel_rate", 0)
                    
                    max_val = max(cash_val, voucher_val, travel_val)
                    min_val = min(cash_val, voucher_val, travel_val)
                    arbitrage = max_val - min_val

                    st.markdown("---")
                    st.markdown(f"""
                    <div style="display: flex; gap: 15px; margin-bottom: 20px;">
                        <div style="flex: 1; background: #08100C; border: 1px solid rgba(52, 211, 153, 0.2); border-radius: 8px; padding: 15px; text-align: center;">
                            <p style="color: #94A3B8; margin: 0; font-size: 13px; text-transform: uppercase;">Statement Credit</p>
                            <h3 style="color: #E2E8F0; margin: 5px 0 0 0; font-size: 1.5rem;">₹{cash_val:,.0f}</h3>
                            <p style="color: #64748B; margin: 0; font-size: 12px;">₹{pt_data.get('cash_rate', 0):.2f} / pt</p>
                        </div>
                        <div style="flex: 1; background: #08100C; border: 1px solid rgba(52, 211, 153, 0.2); border-radius: 8px; padding: 15px; text-align: center;">
                            <p style="color: #94A3B8; margin: 0; font-size: 13px; text-transform: uppercase;">Brand Vouchers</p>
                            <h3 style="color: #E2E8F0; margin: 5px 0 0 0; font-size: 1.5rem;">₹{voucher_val:,.0f}</h3>
                            <p style="color: #64748B; margin: 0; font-size: 12px;">₹{pt_data.get('voucher_rate', 0):.2f} / pt</p>
                        </div>
                        <div style="flex: 1; background: #34D399; border: none; border-radius: 8px; padding: 15px; text-align: center; box-shadow: 0 4px 15px rgba(52, 211, 153, 0.2);">
                            <p style="color: #040D08; margin: 0; font-size: 13px; font-weight: 700; text-transform: uppercase;">Travel Transfer</p>
                            <h3 style="color: #040D08; margin: 5px 0 0 0; font-weight: 800; font-size: 1.5rem;">₹{travel_val:,.0f}</h3>
                            <p style="color: #040D08; margin: 0; font-weight: 600; font-size: 12px;">₹{pt_data.get('travel_rate', 0):.2f} / pt</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    if max_val == cash_val and travel_val == 0 and voucher_val == 0:
                        st.info("💡 **Cash is King:** This card is a pure cashback card. It provides direct statement credit optimally. Point transfers are not applicable.")
                    elif arbitrage > 0 and travel_val == max_val:
                        st.success(f"💡 **Arbitrage Opportunity:** You are leaving **₹{arbitrage:,.0f}** on the table if you redeem for cash instead of transferring to **{pt_data.get('best_partner', 'Travel Partners')}**.")
                    elif arbitrage > 0 and voucher_val == max_val:
                        st.success(f"💡 **Voucher Optimization:** You are leaving **₹{arbitrage:,.0f}** on the table if you redeem for cash instead of claiming Brand Vouchers.")

        # --- TAB 7: PENALTY AUDIT ---
        with tab_audit:
            st.markdown("<h3 style='color: #F8FAFC;'>⚖️ Comprehensive Fee & Penalty Audit</h3>", unsafe_allow_html=True)
            st.write("A strict breakdown of the hidden terms, conditions, and penalties attached to your card.")
            
            if not st.session_state.wallet:
                st.warning("⚠️ Please add a card to your Digital Wallet above.")
            else:
                c_sel, c_btn = st.columns([3, 1])
                audit_card = c_sel.selectbox("Select Card to Audit:", st.session_state.wallet, key="audit_card")
                
                c_btn.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
                if c_btn.button("Run Audit", key="btn_audit", type="primary", use_container_width=True):
                    with st.spinner(f"AI conducting forensic audit of {audit_card} terms and conditions..."):
                        st.session_state[f"audit_{audit_card}"] = get_fee_and_penalty_audit(audit_card)
                
                audit_data = st.session_state.get(f"audit_{audit_card}")
                
                if audit_data:
                    st.markdown("---")
                    
                    a1, a2 = st.columns(2)
                    a1.markdown(f"**Annual / Joining Fee:**<br><span style='color:#34D399'>{audit_data.get('annual_fee', 'N/A')}</span>", unsafe_allow_html=True)
                    a2.markdown(f"**Interest Rate (APR):**<br><span style='color:#ef4444'>{audit_data.get('apr', 'N/A')}</span>", unsafe_allow_html=True)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    a3, a4 = st.columns(2)
                    a3.markdown(f"**Late Payment Fee Slabs:**<br><span style='color:#F59E0B'>{audit_data.get('late_fee', 'N/A')}</span>", unsafe_allow_html=True)
                    a4.markdown(f"**Over-limit Penalty:**<br><span style='color:#F59E0B'>{audit_data.get('overlimit', 'N/A')}</span>", unsafe_allow_html=True)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown(f"**ATM Cash Advance Charge (High Risk):**<br><span style='color:#ef4444'>{audit_data.get('cash_advance', 'N/A')}</span>", unsafe_allow_html=True)

                    st.markdown(f"""
                        <div style="margin-top: 25px; padding: 15px; border-left: 4px solid #ef4444; background-color: rgba(239, 68, 68, 0.1); border-radius: 5px;">
                            <p style="color: #FCA5A5; margin: 0; font-size: 14px; line-height: 1.5;">
                                <b>🚨 AI RED FLAG ADVISORY:</b> {audit_data.get('critical_warning', 'Review all terms carefully.')}
                            </p>
                        </div>
                    """, unsafe_allow_html=True)

    # ==========================================
    # IF NOT LOGGED IN: Show Login/Signup form
    # ==========================================
    else:
        st.markdown("""
            <style>
            [data-testid="stTextInput"] button,
            [data-testid="stTextInput"] [role="button"] {
                display: none !important;
                visibility: hidden !important;
                opacity: 0 !important;
                width: 0px !important;
                height: 0px !important;
                font-size: 0px !important;
                pointer-events: none !important;
            }
            [data-testid="stTextInput"] div[data-baseweb="input"] > div:nth-child(2) {
                display: none !important;
            }
            </style>
        """, unsafe_allow_html=True)

        st.markdown("""
            <div style="text-align: center; margin-bottom: 30px; margin-top: 10px;">
                <h1 class='vault-title'>
                    <span> Obsidian </span><span style="color: #34D399;">Vault</span>
                </h1>
                <p class='vault-subtitle'>Active Yield & Subscription Command</p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        _, center_col, _ = st.columns([1, 1.5, 1])
        
        with center_col:
            with st.container(border=True):
                title_placeholder = st.empty()
                auth_mode = st.radio("Access Gateway", ["🟢 Secure Login", "✨ Create Account"], horizontal=True, label_visibility="collapsed")
                
                clean_title = auth_mode.replace('🟢', '').replace('✨', '').strip()
                title_placeholder.markdown(f"<h3 style='text-align: center; color: #E2E8F0; margin-bottom: 25px;'>{clean_title}</h3>", unsafe_allow_html=True)
                
                username = st.text_input("👤 Commander ID (Username)", placeholder="e.g., abc_24", key="login_username")
                
                st.markdown("🔑 **Security Clearance (Password)**")
                
                show_pwd = st.session_state.get("show_pwd_checkbox", False)
                
                password = st.text_input(
                    "Password", 
                    type="default" if show_pwd else "password", 
                    placeholder="Enter your secret passcode", 
                    label_visibility="collapsed",
                    key="login_password_box"
                )
                
                st.checkbox("Show password", key="show_pwd_checkbox")
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                if auth_mode == "✨ Create Account":
                    if st.button("🚀 Initialize Commander Profile", type="primary", use_container_width=True):
                        if username and password:
                            if create_user(username, password):
                                st.success("✅ Profile initialized! Please switch to Secure Login.")
                            else:
                                st.error("⚠️ Commander ID already exists. Please choose another.")
                        else:
                            st.warning("⚠️ Please provide both your Commander ID and Security Clearance.")
                
                elif auth_mode == "🟢 Secure Login":
                    if st.button("⚡ Breach The Vault", type="primary", use_container_width=True):
                        if username and password:
                            if verify_user(username, password):
                                st.session_state.logged_in = True
                                st.session_state.username = username
                                st.rerun()
                            else:
                                st.error("❌ Access Denied: Invalid ID or Clearance.")
                        else:
                            st.warning("⚠️ Authentication requires credentials.")