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
    response = client.models.generate_content(model=GEMINI_MODEL, contents=prompt)
    elapsed = time.perf_counter() - started
    return parse_json_response(response.text), elapsed
