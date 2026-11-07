"""Personalized learning roadmap generation."""
from utils.llm_client import generate_json

def make_roadmap(gaps):
    priority=[x["skill"] for x in gaps if x["proficiency"]<60][:8]
    if not priority: priority=["AI literacy","Data analysis","Communication"]
    prompt=f'''Create a realistic 3-stage reskilling plan for these priority skills: {priority}. Return JSON only: {{"stages":[{{"stage":"Foundation","duration":"2 weeks","goals":["..."],"practice":"..."}}]}}. Keep advice general; do not claim certifications or employment outcomes.'''
    try:
        data,lat=generate_json(prompt)
        return data.get("stages",data),lat,"Gemini API",priority
    except Exception as exc:
        stages=[{"stage":"Foundation","duration":"Weeks 1–2","goals":[f"Learn core concepts in {s}" for s in priority[:3]],"practice":"Choose one beginner course or trusted open resource per skill; keep notes."},{"stage":"Applied practice","duration":"Weeks 3–5","goals":[f"Practice {s} in a small project" for s in priority[:3]],"practice":"Create one work-like deliverable and ask a peer for feedback."},{"stage":"Evidence and iteration","duration":"Week 6 onward","goals":["Review progress and update priorities"],"practice":"Document a portfolio example and reassess proficiency."}]
        return stages,None,f"Illustrative demo plan: {exc}",priority
