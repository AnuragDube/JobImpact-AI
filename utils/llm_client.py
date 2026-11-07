"""Gemini client. Returns clearly labelled demo results when credentials are absent."""
import os
import time
from dotenv import load_dotenv
from config.settings import GEMINI_MODEL
from utils.validators import parse_json_response

load_dotenv()

def api_key():
    try:
        import streamlit as st
        session_key = st.session_state.get("gemini_key_input")
        if session_key:
            return session_key
        return st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
    except Exception:
        return os.getenv("GEMINI_API_KEY")

def generate_json(prompt: str):
    key = api_key()
    if not key:
        raise RuntimeError("Gemini API key is not configured. Showing labelled demo-mode results.")
    from google import genai
    client = genai.Client(api_key=key)
    started = time.perf_counter()
    model = GEMINI_MODEL
    try:
        import streamlit as st
        model = st.session_state.get("gemini_model_input") or GEMINI_MODEL
    except Exception:
        pass
    response = client.models.generate_content(model=model, contents=prompt)
    elapsed = time.perf_counter() - started
    return parse_json_response(response.text), elapsed
