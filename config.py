import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Updated to use available Gemini models from Vertex AI Model Garden
MODELS = {
    "thinking": "gemini-2.5-pro",  # For complex analysis and coordination
    "simple": "gemini-2.5-flash-lite",  # For searches and simple tasks (from Model Garden)
}

# Configuration for langchain-google-genai (direct model names)
LLM_CONFIG = {
    "thinking": {
        "model": MODELS["thinking"],  # Direct model name for langchain-google-genai
        "api_key": GOOGLE_API_KEY,
        "temperature": 0.1,
    },
    "simple": {
        "model": MODELS["simple"],  # Direct model name for langchain-google-genai
        "api_key": GOOGLE_API_KEY,
        "temperature": 0.3,
    }
}