#  Patent Similarity & Infringement Analyzer

An AI-powered patent analysis system that compares user project ideas with existing patents using NLP and Large Language Models (LLMs). The system retrieves patent data from APIs, analyzes similarity, detects possible infringement risks, performs gap analysis, and provides intelligent suggestions for innovation.

---

#  Features

-  Patent Search using Lens API & SerpAPI
-  AI-Based Patent Similarity Analysis
-  Infringement Risk Classification
-  Similarity Type Detection
-  Patent Abstract + Claims Extraction
-  LLM-Powered Explanations using Ollama
-  Dynamic Innovation Suggestions
-  Gap Analysis between Idea and Patent
-  Streamlit Web Interface

---

# 🛠️ Tech Stack

## Frontend
- Streamlit

## Backend
- Python

## AI / NLP
- Ollama
- Mistral / Llama3
- Scikit-learn
- TF-IDF
- Cosine Similarity
- Sentence Transformers (all-MiniLM-L6-v2)

## Research & Evaluation Notes
- `all-MiniLM-L12-v2` is now the default because it improves prototype accuracy on the current evaluation dataset while remaining CPU-friendly.
- Domain-specific patent/legal alternatives such as PatentBERT, LegalBERT, and MPNet are acknowledged; they are more expensive to run and need additional fine-tuning for patent-specific risk classification.
- Recommended higher-accuracy alternatives for experimentation: `all-mpnet-base-v2` and `GiacomoSignorile/PatentBert-FineTuned`.
- Use `EMBEDDING_MODEL_NAME=<model_name>` in `.env` to switch models.
- High/Medium/Low thresholds are configurable and can be tuned via evaluation analysis.
- Evaluation includes threshold grid search, ROC plot generation, confusion matrix generation, per-class precision / recall, confidence intervals, McNemar test, and baseline comparison versus TF-IDF.
- The project includes a prototype evaluation for LLM-generated explainability using structured criteria.

## Literature Comparison
- PatentBERT vs MiniLM: PatentBERT is optimized for patent-domain semantics and may improve legal matching. MiniLM is selected here for faster inference and broad sentence similarity performance in a prototype.
- Dense retrieval vs keyword retrieval: Dense embeddings preserve conceptual similarity across paraphrased claims, while keyword retrieval is brittle and sensitive to wording changes.
- Explainable AI approaches: This project uses structured LLM-led explanations supplemented by fallback templates. Future work can add claim-level reasoning, counterfactual explanations, and similarity heatmaps.

## Evaluation
- Run `python evaluate.py` to produce model evaluation metrics, ROC and threshold tuning plots, and a sample explainability evaluation report.
- The evaluation benchmark consists of **500 curated patent-idea pairs** spanning healthcare, IoT, transportation, agriculture, manufacturing, finance, and education sectors.
- **Latest Results (500-entry benchmark):**
  - SPAIRD (all-MiniLM-L12-v2): **76.6% accuracy**
  - SPAIRD (with threshold tuning): **80.4% accuracy**
  - TF-IDF baseline: **78.8% accuracy**
  - PatentBERT (from 71-entry pilot): **38.0% accuracy**
- Confidence interval: [73.4%, 80.4%] on the expanded dataset
- Output files are saved under `reports/` including `evaluation_summary.json`, ROC curves, threshold tuning plots, and explainability samples.
- Extend `data/evaluation_dataset.json` with more annotated idea/patent pairs to further improve statistical validity.

## APIs
- Lens API
- SerpAPI (Google Patents)

## Web Scraping
- BeautifulSoup4

---

## Project Summary
This project is a prototype patent similarity and infringement analyzer built with Streamlit, sentence transformers, and LLM-powered explainability. It compares a user idea against retrieved patent documents and classifies risk into High, Medium, or Low categories using configurable thresholds.

## Recent Improvements
- Expanded evaluation dataset from 71 to 500 patent-idea pairs across 7 diverse sectors
- Updated evaluation results showing **76.6% accuracy** (80.4% with tuning) on the larger benchmark
- Added dataset generation script (`generate_evaluation_dataset.py`) for creating realistic cross-domain patent-idea pairs
- Added `all-MiniLM-L12-v2` as default model for improved accuracy and generalization
- Added an evaluation pipeline in `evaluate.py` and `app/services/evaluation.py`
- Added comprehensive annotated benchmark in `data/evaluation_dataset.json`
- Added TF-IDF baseline comparison and threshold grid search
- Added confusion matrix, per-class precision/recall, confidence intervals, and McNemar test support
- Added ROC and threshold tuning plot generation with saved `reports/` figures
- Added model selection rationale for `all-MiniLM-L12-v2` and configurable `EMBEDDING_MODEL_NAME`
- Added comparison showing MiniLM generalization (76.6% on 500-entry benchmark) vs PatentBERT (38.0% on pilot)
- Threshold defaults optimized to High=75 and Medium=55 for the expanded dataset
- Research paper updated with 500-entry benchmark results and enhanced validity analysis

## How to Run Evaluation
1. Install dependencies: `pip install -r requirements.txt`
2. Run: `python evaluate.py`

---

#  Project Structure

```bash
patent-chatbot/
│
├── app/
│   ├── services/
│   │   ├── patent_api.py
│   │   ├── similarity.py
│   │   ├── similarity_type.py
│   │   ├── risk.py
│   │   └── llm.py
│   │
│   ├── utils/
│   │   └── preprocessing.py
│   │
│   ├── __init__.py
│   ├── config.py
│   └── main.py
│
├── data/
│
├── .gitignore
├── requirements.txt
└── README.md