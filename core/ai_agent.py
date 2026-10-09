# core/ai_agent.py
import os
import json
import re
import streamlit as st
import google.generativeai as genai
from tavily import TavilyClient
from config.settings import APP_SETTINGS

# Initialize Tavily
tavily = TavilyClient(api_key=APP_SETTINGS["TAVILY_API_KEY"])

# Initialize Gemini Key Pool
KEY_POOL = APP_SETTINGS["GEMINI_API_KEYS"]
current_key_index = 0

def get_gemini_model():
    """Configures and returns the Gemini model using the current active key."""
    global current_key_index
    active_key = KEY_POOL[current_key_index]
    
    os.environ["GEMINI_API_KEY"] = active_key
    genai.configure(api_key=active_key)
    
    return genai.GenerativeModel('gemini-3.8-flash')

def rotate_key():
    """Switches to the next available API key in the pool."""
    global current_key_index
    if len(KEY_POOL) > 1:
        current_key_index = (current_key_index + 1) % len(KEY_POOL)
        print(f"🔄 Switched to Gemini API Key #{current_key_index + 1}")
        return True
    return False

# 1-HOUR CACHE (3600 seconds)
@st.cache_data(ttl=3600, show_spinner=False)
def generate_card_roadmap(user_data):
    """Searches web context and generates recommendations with network resilience."""
    attempts = 0
    # Add a couple of extra buffer attempts purely for network drops
    max_attempts = len(KEY_POOL) + 2 

    while attempts < max_attempts:
        try:
            query = f"Best credit cards in India 2026 for {user_data.get('occ', 'professional')} with {user_data.get('income', 50000)} monthly income."
            
            # The network drop happens here. The try-except will now catch it.
            web_data = tavily.search(query=query, search_depth="advanced")
            
            prompt = f"""
            Act as an Expert Financial Advisor.
            User Profile: {user_data}
            Recent Web Data: {web_data}

            Please provide a comprehensive financial roadmap structured into these specific sections:

            1. Top 5 Podium Recommendations: First, create a clean Markdown table (using | and -) to visually summarize the recommended cards. Below the table, provide a detailed numbered list explaining the rewards and why each card fits this user.
            2. Step-by-Step Action Plan: At the very bottom, provide a clear, actionable list of key steps the user must follow to achieve their credit and financial goals.

            Format your entire response clearly using standard markdown.
            """
            model = get_gemini_model()
            response = model.generate_content(prompt)
            return response.text

        except Exception as e:
            error_message = str(e)
            
            # 1. Detect if it's a Gemini Quota Error
            is_quota_error = any(err in error_message for err in ["429", "Quota", "API_KEY_INVALID"])
            # 2. Detect if it's a Tavily/Network Drop Error
            is_network_error = any(err in error_message for err in ["Connection", "RemoteDisconnected", "ProtocolError", "Max retries"])
            
            if is_quota_error or is_network_error:
                attempts += 1
                if attempts < max_attempts:
                    import time
                    time.sleep(2) # Give the network 2 seconds to recover
                    
                    if is_quota_error:
                        rotate_key() # Only burn a key rotation if it was actually a Gemini quota issue
                        
                    continue # Retry the API calls
            
            # If it's a completely unknown error, or we ran out of retries
            raise RuntimeError(f"Roadmap Error: {error_message}")

    raise RuntimeError("Generation failed. Network may be down or all API keys are exhausted.")

# 1-HOUR CACHE (3600 seconds)
@st.cache_data(ttl=3600, show_spinner=False)
def generate_battle_analysis(entered_card, original_recommendation, user_data):
    """Compares an entered card against the top recommendation."""
    attempts = 0
    max_attempts = len(KEY_POOL)

    while attempts < max_attempts:
        try:
            battle_prompt = f"""
            Expert Advisor Mode. 
            Profile: {user_data}. 
            Original podium: {original_recommendation}. 
            
            Compare the card '{entered_card}' against the #1 recommended card from the podium.
            Explain clearly and concisely which card is better for this specific user.
            """
            model = get_gemini_model()
            response = model.generate_content(battle_prompt)
            return response.text
            
        except Exception as e:
            error_message = str(e)
            if "429" in error_message or "Quota" in error_message or "API_KEY_INVALID" in error_message:
                attempts += 1
                if rotate_key() and attempts < max_attempts:
                    import time
                    time.sleep(1)
                    continue
            raise RuntimeError(f"Battle Analysis Error: {error_message}")

    raise RuntimeError("All API keys exhausted for battle analysis.")

# 1-HOUR CACHE (3600 seconds)
@st.cache_data(ttl=3600, show_spinner=False)
def get_fee_waiver_target(card_name):
    """Fetches annual fee waiver spend target with fallback."""
    attempts = 0
    max_attempts = len(KEY_POOL)

    while attempts < max_attempts:
        try:
            query = f"What is the annual fee waiver spend target for {card_name} credit card in India 2026?"
            web_data = tavily.search(query=query)
            
            prompt = f"""
            Based on this web data: {web_data}.
            What is the exact annual spend required in INR to waive the annual fee for the '{card_name}'? 
            Return ONLY the integer number (e.g., 100000, 200000). 
            If it is lifetime free or has no waiver, return 0. Do not include text or commas.
            """
            model = get_gemini_model()
            response = model.generate_content(prompt)
            numbers = re.findall(r'\d+', response.text.replace(',', ''))
            return int(numbers[0]) if numbers else 200000 
            
        except Exception as e:
            error_message = str(e)
            if "429" in error_message or "Quota" in error_message or "API_KEY_INVALID" in error_message:
                attempts += 1
                if rotate_key() and attempts < max_attempts:
                    import time
                    time.sleep(1)
                    continue
            raise RuntimeError(f"Waiver Target Error: {error_message}")

    raise RuntimeError("All API keys exhausted.")

# 1-HOUR CACHE (3600 seconds)
@st.cache_data(ttl=3600, show_spinner=False)
def get_forex_markup(card_name):
    """Fetches the actual forex markup fee percentage with key rotation."""
    attempts = 0
    max_attempts = len(KEY_POOL)

    while attempts < max_attempts:
        try:
            query = f"What is the exact forex markup fee percentage for {card_name} in India?"
            web_data = tavily.search(query=query, search_depth="basic")
            
            prompt = f"""
            Based on this web data: {web_data}.
            What is the base forex markup fee percentage (in %) charged by the '{card_name}' for international transactions?
            (For example, if it's a standard card, it might be 3.5. If it's a Zero-Forex card like IDFC First Wealth, IDFC WOW, or Scapia, return 0.0).
            Return ONLY the float number (e.g., 3.5, 1.5, 0.0). Do not include the % sign, taxes, or any text.
            """
            model = get_gemini_model()
            response = model.generate_content(prompt)
            
            numbers = re.findall(r"[-+]?\d*\.\d+|\d+", response.text)
            if numbers:
                rate = float(numbers[0])
                return min(rate, 5.0)
            return 3.5 
            
        except Exception as e:
            error_message = str(e)
            if "429" in error_message or "Quota" in error_message or "API_KEY_INVALID" in error_message:
                attempts += 1
                if rotate_key() and attempts < max_attempts:
                    import time
                    time.sleep(1)
                    continue
            raise RuntimeError(f"Forex fetch error: {error_message}")

    raise RuntimeError("All API keys exhausted.")

# 15-MINUTE CACHE (900 seconds) - KEEPS DEALS LIVE
@st.cache_data(ttl=900, show_spinner=False)
def get_copilot_verdict(query, wallet_context):
    """Evaluates an impromptu expense against the user's wallet."""
    attempts = 0
    max_attempts = len(KEY_POOL)

    while attempts < max_attempts:
        try:
            prompt = f"""
            You are a strict, elite financial advisor. The user is asking about an upcoming expense.
            
            User's Expense Query: "{query}"
            
            User's Digital Wallet & Credit Limits:
            {wallet_context}
            
            RULES FOR YOUR VERDICT:
            1. 30% UTILIZATION RULE (CRITICAL): If the user's expense exceeds 30% of the specific card's limit, you MUST issue a "🔴 HOLD" verdict and warn them about CIBIL score damage. Advise them to split the transaction or use a different payment method.
            2. If the expense is safe (<30%), recommend the best card from their wallet for this specific category (e.g., travel, dining, fuel) and issue a "🟢 SWIPE" verdict.
            3. Keep the response under 4 sentences. Be punchy, formatting the first word as either 🟢 SWIPE or 🔴 HOLD.
            """
            model = get_gemini_model()
            response = model.generate_content(prompt)
            return response.text
        
        except Exception as e:
            error_message = str(e)
            if "429" in error_message or "Quota" in error_message or "API_KEY_INVALID" in error_message:
                attempts += 1
                if rotate_key() and attempts < max_attempts:
                    import time
                    time.sleep(1)
                    continue
            raise RuntimeError(f"Copilot Error: {error_message}")

    raise RuntimeError("All API keys are currently rate-limited.")

@st.cache_data(ttl=899, show_spinner=False) # Changed from 900 to 899
def fetch_live_card_offers(card_name):
    """Searches the web for live discounts and renders them as UI Coupon Cards."""
    attempts = 0
    max_attempts = len(KEY_POOL)

    while attempts < max_attempts:
        try:
            query = f"Latest active offers, sales, and discounts for {card_name} credit card in India on Amazon, Flipkart, Swiggy, Zomato, MakeMyTrip, IRCTC Train Booking, Indigo/AirIndia Flights, and HPCL/BPCL/IOCL Fuel 2026"
            web_data = tavily.search(query=query, search_depth="basic")
            
            prompt = f"""
            Based on the following live web data: {web_data}
            
            List the current active offers, sales, or standard benefits available for the '{card_name}' credit card.
            You must find data for these 5 exact categories:
            1. E-Commerce (Amazon/Flipkart)
            2. Food & Dining (Swiggy/Zomato)
            3. Travel (Flights/Hotels)
            4. Train Bookings (IRCTC)
            5. Fuel & Transit (BPCL/HPCL/IOCL)
            
            OUTPUT INSTRUCTION:
            Do NOT output standard markdown text. You must output exactly 5 HTML blocks (one for each category).
            Wrap each category in this exact HTML structure:
            
            <div style="background: linear-gradient(145deg, #1A2235, #111827); border: 1px solid #2D3748; border-left: 4px solid #06B6D4; border-radius: 12px; padding: 20px; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
                <h4 style="color: #E2E8F0; margin-top: 0; margin-bottom: 10px; font-weight: 700; letter-spacing: 0.5px;">[EMOJI] [CATEGORY NAME]</h4>
                <p style="color: #94A3B8; font-size: 14px; margin-bottom: 0; line-height: 1.5;">[ONE PUNCHY SENTENCE EXPLAINING THE BEST OFFER OR BENEFIT FOUND]</p>
            </div>
            
            Replace the bracketed information with the actual data. Do not include any other text outside the HTML blocks.
            """
            model = get_gemini_model()
            response = model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            error_message = str(e)
            if "429" in error_message or "Quota" in error_message or "API_KEY_INVALID" in error_message:
                attempts += 1
                if rotate_key() and attempts < max_attempts:
                    import time
                    time.sleep(1)
                    continue
            raise RuntimeError(f"Error fetching offers: {error_message}")

    raise RuntimeError("All API keys exhausted. Please try again later.")

# 1-HOUR CACHE (3600 seconds)
@st.cache_data(ttl=3600, show_spinner=False)
def get_hidden_milestones(card_name):
    """Fetches milestone rewards and renders them as Gold Achievement Cards."""
    attempts = 0
    max_attempts = len(KEY_POOL)

    while attempts < max_attempts:
        try:
            query = f"What are the milestone rewards or bonus offers based on annual spend for {card_name} credit card in India 2026? Be specific about spend amounts and the reward."
            web_data = tavily.search(query=query, search_depth="basic")
            
            prompt = f"""
            Based on this web data: {web_data}.
            List the annual milestone rewards for the '{card_name}' credit card. 
            
            OUTPUT INSTRUCTION:
            Do NOT output standard markdown text. You must output HTML blocks for each milestone found.
            Wrap each milestone in this exact HTML structure:
            
            <div style="background: linear-gradient(145deg, #1A2235, #111827); border: 1px solid #2D3748; border-left: 4px solid #F59E0B; border-radius: 12px; padding: 20px; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
                <h4 style="color: #FCD34D; margin-top: 0; margin-bottom: 10px; font-weight: 700; letter-spacing: 0.5px;">🏆 Spend ₹[AMOUNT]</h4>
                <p style="color: #94A3B8; font-size: 14px; margin-bottom: 0; line-height: 1.5;">[ONE PUNCHY SENTENCE EXPLAINING THE REWARD]</p>
            </div>
            
            Replace the bracketed information with the actual data. 
            If there are no milestone rewards found, output a single HTML block stating "No Milestone Rewards Found" and explain that this card focuses on direct cashback/rewards rather than spend-based milestones.
            Do not include any other text outside the HTML blocks.
            """
            model = get_gemini_model()
            response = model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            error_message = str(e)
            if "429" in error_message or "Quota" in error_message or "API_KEY_INVALID" in error_message:
                attempts += 1
                if rotate_key() and attempts < max_attempts:
                    import time
                    time.sleep(1)
                    continue
            raise RuntimeError(f"Error fetching milestones: {error_message}")

    raise RuntimeError("Milestone data temporarily unavailable.")

# 1-HOUR CACHE (3600 seconds)
@st.cache_data(ttl=3600, show_spinner=False)
def get_utility_cashback_rate(card_name, services):
    """Fetches the actual cashback percentage for specific services with key rotation."""
    attempts = 0
    max_attempts = len(KEY_POOL)

    while attempts < max_attempts:
        try:
            query = f"Cashback percentage for {services} using {card_name} credit card India"
            web_data = tavily.search(query=query, search_depth="basic")
            
            prompt = f"""
            Based on this web data: {web_data}.
            The user is paying for these specific services: {services}.
            What is the actual exact cashback or value-back percentage (in %) the '{card_name}' gives for these specific services?
            (If it's Netflix/Amazon Prime on a card that only gives 1% for general online spends, return 1.0).
            Return ONLY the float number (e.g., 5.0, 1.0, 2.0). Do not include the % sign or text.
            If there are multiple different services, return the average percentage as a float.
            """
            model = get_gemini_model()
            response = model.generate_content(prompt)
            
            numbers = re.findall(r"[-+]?\d*\.\d+|\d+", response.text)
            if numbers:
                rate = float(numbers[0])
                return min(rate, 25.0)
            return 1.0 
            
        except Exception as e:
            error_message = str(e)
            if "429" in error_message or "Quota" in error_message or "API_KEY_INVALID" in error_message:
                attempts += 1
                if rotate_key() and attempts < max_attempts:
                    import time
                    time.sleep(1)
                    continue
            raise RuntimeError(f"Utility Rate Error: {error_message}")

    raise RuntimeError("Failed to calculate utility yield.")

# 1-HOUR CACHE (3600 seconds)
@st.cache_data(ttl=3600, show_spinner=False)
def get_reward_point_values(card_name):
    """Fetches exact INR conversion values for reward points across 3 redemption categories."""
    attempts = 0
    max_attempts = len(KEY_POOL)

    while attempts < max_attempts:
        try:
            query = f"Value of 1 reward point in INR for {card_name} statement credit, vouchers, and travel miles transfer"
            web_data = tavily.search(query=query, search_depth="basic")
            
            prompt = f"""
            Based on this web data: {web_data}.
            What is the monetary value of 1 Reward Point (in INR) for the '{card_name}' in these three specific categories?
            Return ONLY a valid JSON object with exact float values (e.g., 0.25, 1.0) and no markdown formatting, no backticks.
            Format exactly like this:
            {{
                "cash_rate": float (statement credit value),
                "voucher_rate": float (Amazon/Flipkart voucher value),
                "travel_rate": float (Airmiles/Hotel transfer value),
                "best_partner": "string (name of the best airline/hotel partner to transfer to, max 3 words)"
            }}
            """
            model = get_gemini_model()
            response = model.generate_content(prompt)
            
            cleaned_text = response.text.replace("```json", "").replace("```", "").strip()
            return json.loads(cleaned_text)
            
        except Exception as e:
            error_message = str(e)
            if "429" in error_message or "Quota" in error_message or "API_KEY_INVALID" in error_message:
                attempts += 1
                if rotate_key() and attempts < max_attempts:
                    import time
                    time.sleep(1)
                    continue
            raise RuntimeError(f"Point Valuation Error: {error_message}")

    raise RuntimeError("Failed to evaluate reward point values.")

# 1-HOUR CACHE (3600 seconds)
@st.cache_data(ttl=3600, show_spinner=False)
def get_fee_and_penalty_audit(card_name):
    """Extracts hidden fees, APR, and penalties into a structured audit format."""
    attempts = 0
    max_attempts = len(KEY_POOL)

    while attempts < max_attempts:
        try:
            query = f"{card_name} hidden fees, interest rate APR, cash advance fee, late payment penalty India"
            web_data = tavily.search(query=query, search_depth="basic")
            
            prompt = f"""
            Based on this web data: {web_data}.
            Perform a strict financial audit of the '{card_name}'.
            Return ONLY a valid JSON object, no markdown formatting, no backticks.
            Format exactly like this:
            {{
                "annual_fee": "string (e.g., '₹5,000 + GST' or 'Lifetime Free')",
                "apr": "string (e.g., '3.6% per month / 43.2% Annually')",
                "late_fee": "string (e.g., 'Up to ₹1,200 depending on balance')",
                "cash_advance": "string (e.g., '2.5% or Min ₹500 + Instant Interest')",
                "overlimit": "string (e.g., '2.5% of overlimit amount')",
                "critical_warning": "string (Identify the most dangerous or hidden penalty clause in 1 short sentence)"
            }}
            """
            model = get_gemini_model()
            response = model.generate_content(prompt)
            
            cleaned_text = response.text.replace("```json", "").replace("```", "").strip()
            return json.loads(cleaned_text)
            
        except Exception as e:
            error_message = str(e)
            if "429" in error_message or "Quota" in error_message or "API_KEY_INVALID" in error_message:
                attempts += 1
                if rotate_key() and attempts < max_attempts:
                    import time
                    time.sleep(1)
                    continue
            raise RuntimeError(f"Audit Error: {error_message}")

    raise RuntimeError("Failed to conduct penalty audit.")