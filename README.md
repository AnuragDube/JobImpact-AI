---
title: JobImpact AI
emoji: 🧭
colorFrom: blue
colorTo: indigo
sdk: streamlit
sdk_version: 1.40.0
python_version: 3.11
app_file: app.py
pinned: false
---

# JobImpact AI

**P59 · Job Task Exposure Analyzer · Track E: Responsible AI**
Anurag Chotulal Dube · Roll 59 · MIT ADT University · B.Tech Computer Science Engineering

JobImpact AI decomposes a job into responsibilities and examines which tasks may be automatable, AI-augmented, or human-led. It also connects tasks to professional skills, supports a self-rated skill-gap review, and produces a staged reskilling roadmap. Results are exploratory and require human review.

## Run locally

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
streamlit run app.py
```

Add `GEMINI_API_KEY` to `.env` (or `.streamlit/secrets.toml`) to enable Gemini generation and reasoning. Set `GEMINI_MODEL` to a model available to your Google AI account. Without a key, decomposition, classification and roadmap features use illustrative demo behavior and are labelled in the UI. Demo classifications are not AI model results.

Sentence-BERT loads `sentence-transformers/all-MiniLM-L6-v2` on CPU. The first load downloads model weights and needs network access; if unavailable, a labelled TF-IDF fallback is used. No model weights are fine-tuned.

## Application modules

- **U1:** Job decomposition and zero-shot/few-shot prompt comparison.
- **U2:** Per-task exposure labels and explanations, plus prompt-based inference versus fine-tuning discussion.
- **U3:** Sentence-BERT task-to-skill semantic matching and proficiency self-assessment.
- **U4:** Staged roadmap and dynamically generated PNG infographic.
- **U5:** Controlled demographic wording probes, consistency guardrails, limitations, privacy and workforce context.
- **Evaluation:** Manually labelled reference dataset, accuracy, confusion matrix, latency and failure cases.

`evaluation/test_dataset.csv` is an illustrative manually labelled class exercise. Its labels are not an external ground truth or occupational research dataset. Run `python -m evaluation.evaluate --demo` to measure the rule-based fallback, or omit `--demo` with a Gemini key to evaluate live model predictions. Record the mode and date when reporting results. The demo rules were developed alongside this small teaching dataset, so scores are descriptive only and are not an unbiased estimate of generalization.

## Deployment: Streamlit Community Cloud

**Live app:** https://jobimpact-ai-anurag.streamlit.app/

The app is deployed from the public [`AnuragDube/JobImpact-AI`](https://github.com/AnuragDube/JobImpact-AI) repository, branch `main`, with `app.py` as its entry point. The first deployment may take several minutes while the Python dependencies are installed.

To use Gemini, enter a key in the password field in the app sidebar. A key entered there is used for that browser session. To configure a default key for the hosted app, add `GEMINI_API_KEY` under the app's Streamlit Cloud settings → Secrets. Optionally set `GEMINI_MODEL` there as well. Never commit API keys to Git or put them in source code. Without a configured key, the app clearly labels its illustrative demo outputs.

## Documentation

- [`docs/model_card.md`](docs/model_card.md)
- [`docs/viva_guide.md`](docs/viva_guide.md)
- [`docs/demo_script.md`](docs/demo_script.md)
- [`docs/report.md`](docs/report.md) (submission report source)

## Privacy and limits

Job descriptions are held in the current Streamlit session and are not written to an application database. When Gemini is configured, submitted text is sent to Google's API. Do not submit personal or confidential job information. Exposure labels do not predict job loss, actual adoption, wages, or future employment. Similarity scores are not competence probabilities. Bias probes use a tiny controlled set and do not establish fairness across populations. A human must review all outputs.
