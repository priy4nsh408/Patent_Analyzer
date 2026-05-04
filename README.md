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

## APIs
- Lens API
- SerpAPI (Google Patents)

## Web Scraping
- BeautifulSoup4

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