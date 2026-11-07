"""Shared application settings."""
import os

APP_NAME = "JobImpact AI"
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
SKILL_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
TASK_LIMIT = 15
MIN_TASKS = 10
