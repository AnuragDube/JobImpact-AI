"""Zero-shot/few-shot task decomposition."""
import json
from utils.llm_client import generate_json

def decomposition_prompt(job: str, few_shot: bool = False) -> str:
    examples = '\nExample: "Registered nurse" -> [{"task":"Monitor patient vital signs","context":"Record observations and flag changes"}]\n' if few_shot else ""
    return f'''Break the following job into 10 to 15 distinct, realistic responsibilities. Avoid invented company-specific facts. Return JSON only: {{"tasks":[{{"task":"...","context":"..."}}]}}. {examples}\nJob input: {job}'''

def demo_tasks(job: str):
    title = job.splitlines()[0][:90]
    tasks = ["Gather and validate relevant information", "Prepare routine reports and documentation", "Use domain tools to complete standard workflows", "Review work for accuracy and completeness", "Coordinate with colleagues and stakeholders", "Respond to routine questions and requests", "Identify exceptions and escalate complex cases", "Prioritize work against deadlines and service needs", "Apply professional standards and policies", "Communicate findings and recommendations"]
    return [{"task": t, "context": f"Illustrative responsibility for {title}"} for t in tasks]

def decompose(job: str, few_shot=False):
    try:
        result, latency = generate_json(decomposition_prompt(job, few_shot))
        tasks = result.get("tasks", result) if isinstance(result, dict) else result
        if not isinstance(tasks, list) or len(tasks) < 10:
            raise ValueError("Expected 10 to 15 responsibilities; using the labelled illustrative fallback.")
        return tasks[:15], latency, "Gemini API"
    except Exception as exc:
        return demo_tasks(job), None, f"Demo mode: {exc}"
