"""Task exposure classification using Gemini, with transparent illustrative fallback."""
from utils.llm_client import generate_json

LABELS = ["Automate", "Augment", "Human-led"]
CLASSIFY_PROMPT = '''Classify each job responsibility into Automate, Augment, or Human-led. Automate means routine and rules-based work AI could perform with limited involvement. Augment means AI can assist but human review or decisions remain important. Human-led means high-stakes judgment, empathy, negotiation, accountability, or physical context remain central. Return JSON only as {"classifications":[{"task":"exact task","label":"Augment","explanation":"...","confidence":0.0,"skills":["..."]}]}. Treat confidence as a reasoned estimate, not calibrated probability. Tasks: {tasks}'''

def demo_classify(tasks):
    out=[]
    for row in tasks:
        task=row["task"] if isinstance(row,dict) else str(row)
        low=task.lower()
        if any(w in low for w in ["routine", "standard", "format", "boilerplate", "scheduled query", "remove duplicate", "resize", "schedule approved", "rules"]): label="Automate"
        elif any(w in low for w in ["security-sensitive", "discuss trade-offs", "explain", "choose an appropriate", "negotiate", "final", "crisis", "leadership"]): label="Human-led"
        else: label="Augment"
        out.append({"task":task,"label":label,"explanation":"Illustrative rule-based demo classification; review against the actual role context.","confidence":None,"skills":[]})
    return out

def classify(tasks):
    try:
        result, latency=generate_json(CLASSIFY_PROMPT.replace("{tasks}", str(tasks)))
        rows=result.get("classifications",result) if isinstance(result,dict) else result
        if not isinstance(rows,list) or not rows:
            raise ValueError("The model did not return a classification list.")
        for row in rows:
            if row.get("label") not in LABELS or not str(row.get("explanation","")).strip():
                raise ValueError("A classification had a missing explanation or unsupported label.")
            confidence=row.get("confidence")
            if not isinstance(confidence,(float,int)) or not 0 <= confidence <= 1:
                row["confidence"]=None
        return rows,latency,"Gemini API"
    except Exception as exc:
        return demo_classify(tasks),None,f"Demo mode: {exc}"
