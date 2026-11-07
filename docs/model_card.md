# Model Card: JobImpact AI

## Intended use
Educational exploration of task exposure and skills/reskilling concepts for P59. It is not an employment, hiring, workforce reduction, or public-policy decision system.

## System components
Gemini API (configured model name is environment-dependent) generates decomposition, classifications and roadmap drafts. Sentence-BERT `all-MiniLM-L6-v2` encodes task and skill text for cosine similarity. TF-IDF is an explicitly labelled fallback. Rule-based demo results support credential-free demonstrations; these are not model predictions. PyTorch provides the Sentence Transformers runtime where installed. No fine-tuning occurs.

## Data
User-supplied job text and a built-in curated list of generic professional skills. Evaluation examples are a manually labelled educational dataset in `evaluation/test_dataset.csv`, not representative occupational data.

## Limitations and risks
Outputs depend on prompt quality, job wording, role context, API model changes and incomplete skills taxonomy. Labels can obscure mixed human/AI workflows and do not measure adoption or displacement. Demographic wording probes are small and not a fairness certification. Similarity scores are not probabilities or proficiency. Generated explanations may be wrong or overconfident.

## Safeguards
Credential-free demo mode is labelled; input length is bounded; model outputs are described as estimates; structural validation checks label and explanation presence; sensitive inputs are discouraged; human oversight is emphasized. Review outputs and avoid high-stakes decisions.

## Evaluation
Use `python -m evaluation.evaluate --demo` for the actual fallback metrics, or configured Gemini for live predictions. Cite the evaluation mode and run date. No performance claims are made in this card without an executed run.
