# 59_Anurag_Chotulal_Dube_P59

## Cover page
**JobImpact AI: Job Task Exposure Analyzer**  
P59 · Track E: Responsible AI  
Anurag Chotulal Dube · Roll 59  
MIT ADT University · B.Tech Computer Science Engineering

## Problem statement and objective
Analyze how generative AI could affect individual responsibilities within a role. Classify tasks as Automate, Augment, or Human-led, explain the assessment, connect tasks to skills, and propose a reskilling path. The system is an educational prototype; it does not estimate actual job loss.

## Tools, models and dataset
Python 3.11+, Streamlit, Gemini API, Sentence-BERT `all-MiniLM-L6-v2`, PyTorch runtime, scikit-learn, Pandas, Plotly and Matplotlib. The 19 reference examples in `evaluation/test_dataset.csv` are manually labelled classroom examples, not representative external ground truth. The executed demo-rule evaluation scored 18/19 (94.74%); confusion matrix true rows/predicted columns in Automate, Augment, Human-led order: [[6,0,0],[0,6,0],[1,0,6]]. Its failure was a security-sensitive authentication task whose wording also contains “boilerplate.” This describes the fallback on a small dataset developed alongside its rules; it is not Gemini performance or an unbiased generalization estimate.

## System architecture and block diagram
See the generated block diagram in the submission PDF. In sequence: user job text → bounded input validation → Gemini decomposition (zero/few shot) → Gemini task exposure classification → Sentence-BERT semantic skill matching → self-rated skill gap → Gemini or illustrative staged roadmap → Matplotlib infographic → Streamlit report views. Responsible-AI probes and structural checks run beside analysis. A labelled demo fallback is used without credentials.

## Implementation approach
See modular code in `modules/`, `utils/`, and `app.py`. Prompt-based inference is used; weights are not fine-tuned. PyTorch is used by Sentence Transformers when available. The TF-IDF fallback is labelled.

## Important code and GitHub link
Key files: `app.py`, `modules/job_decomposition.py`, `modules/task_classification.py`, `modules/skill_matching.py`, `modules/responsible_ai.py`, and `evaluation/evaluate.py`. GitHub URL: **not created or verified**. Add after authorized repository creation and push.

## Application screenshots
Insert genuine screenshots captured from the running application here. Do not use mockups as evidence of execution.

## Results and evaluation
Executed on 2026-11-07 using the rule-based illustrative fallback, not Gemini: 19 examples, accuracy 18/19 (94.74%), mean local loop latency 0.000076 seconds per row. Confusion matrix (true rows, predicted columns; Automate, Augment, Human-led): [[6,0,0],[0,6,0],[1,0,6]]. Failure: “Generate boilerplate for a security-sensitive authentication flow” was labelled Human-led but predicted Automate because the simple rule triggers on “boilerplate” without weighing the security context. These rules were developed alongside the small teaching set, so the score is descriptive and not a generalization estimate. The submission PDF includes these results. No screenshots are included because the complete Streamlit runtime could not be run in this environment.

## Limitations and failure cases
Task descriptions omit organizational context; generated content can be incorrect; the fixed skill vocabulary is incomplete; similarity is not competence; classifications are not calibrated; wording audit is small; API/model availability changes. Discuss failure rows from the executed evaluation and how review and labels expose the limitations.

## Ethical considerations
Protect job-description privacy; consider differential impacts and workforce displacement; do not use for individual employment decisions; keep humans accountable; explain uncertainty and avoid presenting exposure as inevitable replacement.

## Conclusion
Summarize measured results only after the application and evaluation have actually been run. Explain what task-level analysis and reskilling support can contribute, and why human oversight and further evaluation remain necessary.
