"""Input validation and safe JSON parsing helpers."""
import json

def validate_job_input(value: str) -> str:
    text = (value or "").strip()
    if len(text) < 3:
        raise ValueError("Enter a job title or description with at least 3 characters.")
    if len(text) > 12000:
        raise ValueError("Please keep the job description under 12,000 characters.")
    return text

def parse_json_response(text: str):
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[-1].rsplit("```", 1)[0]
    start, end = cleaned.find("{"), cleaned.rfind("}")
    if start < 0 or end < start:
        start, end = cleaned.find("["), cleaned.rfind("]")
    if start < 0 or end < start:
        raise ValueError("The model response did not contain valid JSON.")
    return json.loads(cleaned[start:end + 1])
