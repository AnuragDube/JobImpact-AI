# JobImpact AI Viva Guide

## Project objective
The application analyzes a job at the responsibility level. It labels tasks as Automate, Augment, or Human-led, matches them to skills, and outlines a reskilling plan. These are exploratory judgments, not forecasts of job loss.

## Generative AI lifecycle
Define a task and constraints, provide context and a prompt, run model inference, validate the returned structure and content, have a person review it, and refine the prompt or workflow using observed failures.

## Zero-shot and few-shot prompting
Zero-shot prompting gives instructions without examples. Few-shot prompting includes examples to demonstrate the desired output format or reasoning pattern. Neither changes model weights. Output differences should be inspected, not assumed to be improvements.

## Transformer and attention
A transformer processes token representations using attention. For each token, learned projections produce queries, keys, and values. Similarity between queries and keys gives weights over values, allowing context to influence the token representation. Multiple heads can learn different relationships. This application does not expose Gemini's internal attention maps.

## GPT and BERT
GPT-style models use a decoder and predict subsequent tokens autoregressively, making them useful for generating text. BERT-style encoders use bidirectional context to build token representations, commonly for classification or understanding. Sentence-BERT is adapted to produce sentence embeddings useful for semantic similarity.

## Sentence-BERT and similarity
The app encodes a task and candidate skill descriptions into vectors, then uses cosine similarity. A higher score means the text representations are closer under the model. It is not a probability that the skill is required, nor evidence that a person has the skill.

## PyTorch usage
Sentence Transformers typically runs on PyTorch. This project loads a pretrained CPU model; it does not train or fine-tune model weights. If unavailable, the interface reports a TF-IDF fallback.

## LLM API integration
The Gemini client reads a key from environment variables or Streamlit secrets, requests JSON output, parses it, and handles API errors by showing clearly labelled illustrative behavior. The fallback is not represented as model output.

## Evaluation and bias
The reference CSV has manually labelled examples across three roles. Accuracy and confusion matrix compare predictions to those labels. Since the dataset is small and authored for a class exercise, the score does not generalize. Matched demographic wording probes check sensitivity for a few prompts; they do not certify fairness.

## Hallucinations and safeguards
An LLM can confidently produce unsupported details. The app requests constrained JSON, validates label values and explanation presence, bounds input length, labels demo outputs, presents uncertainty, and asks the user to review. Structural validity does not prove factual accuracy.

## Reskilling roadmap
Required skills are matched from a structured vocabulary. Users self-rate proficiency; lower ratings among the matched skills become priorities. A model or illustrative fallback drafts staged learning goals and the infographic renders current results.

## Limitations and responsible use
Descriptions omit local workflows, model outputs change, the skill vocabulary is incomplete, and an exposure category is not an adoption or displacement prediction. Avoid confidential input and high-stakes employment use. Humans remain accountable.

## Deployment architecture
Hugging Face Spaces can run the Streamlit entry point on CPU. Store Gemini keys in Space secrets, never in the repository. The first Sentence-BERT use may download model weights; the TF-IDF fallback supports restricted environments.
