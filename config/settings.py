import os
from dotenv import load_dotenv, find_dotenv

def load_environment():
    """Loads environment variables and collects all Gemini API keys."""
    load_dotenv(find_dotenv("api.env"))
    
    tavily_key = os.getenv("TAVILY_API_KEY")
    
    # Collect all available Gemini keys from the environment
    gemini_keys = [
        os.getenv("GEMINI_API_KEY_1"),
        os.getenv("GEMINI_API_KEY_2"),
        os.getenv("GEMINI_API_KEY_3"),
        os.getenv("GEMINI_API_KEY_4"),
        os.getenv("GEMINI_API_KEY_5"),
        os.getenv("GEMINI_API_KEY")  # Backwards compatibility if single key is used
    ]
    # Filter out None or empty strings
    valid_gemini_keys = [k for k in gemini_keys if k]
    
    if not tavily_key or not valid_gemini_keys:
        print("⚠️ Warning: Missing critical API keys in api.env")
        
    return {
        "TAVILY_API_KEY": tavily_key,
        "GEMINI_API_KEYS": valid_gemini_keys
    }

APP_SETTINGS = load_environment()