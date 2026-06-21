# Project Changes Summary

## Overview
This file summarizes the recent changes made to the patent analysis project to improve project explanation, evaluation, dataset coverage, and report artifacts.
It is intended as a detailed change log for the current prototype.

## Detailed Changes

### Evaluation Pipeline
- Added `evaluate.py` as a command-line evaluation runner for the annotated dataset.
- Added `app/services/evaluation.py` with support for:
  - loading and evaluating annotated idea/patent pairs
  - TF-IDF baseline similarity and model comparison
  - per-class precision, recall, and macro F1
  - confusion matrix support and classification reports
  - threshold grid search for High / Medium / Low risk boundaries
  - ROC curve plotting for the multiclass risk labels
  - threshold tuning plots and saved figure exports
  - bootstrap confidence intervals for accuracy
  - McNemar statistical tests for comparing classifiers
  - sample failure case extraction and explainability summary output

### Annotated Dataset
- Expanded `data/evaluation_dataset.json` to 71 manually annotated pairs.
- The new dataset supports more stable evaluation and gives a better basis for threshold selection.

### Risk Thresholds and Explainability
- Updated `app/config.py` to expose:
  - `HIGH_THRESHOLD = 80`
  - `MEDIUM_THRESHOLD = 50`
- Added support for environment-configurable thresholds via `SIMILARITY_THRESHOLD_HIGH` and `SIMILARITY_THRESHOLD_MEDIUM`.
- Updated `app/services/risk.py` to use inclusive `>=` cutoffs for risk tier assignment.
- Improved `app/services/llm.py` fallback explanations so they reference the same configurable thresholds and produce consistent risk-language output.

### Documentation and Reports
- Extended `README.md` with:
  - evaluation workflow and instructions
  - recent improvements and project rationale
  - mention of ROC and threshold tuning artifacts
- Updated `requirements.txt` to include `sentence-transformers` and `matplotlib` for evaluation and plotting.
- Added report integration in `reports/research_paper.tex` for:
  - `reports/roc_curve.png`
  - `reports/threshold_analysis.png`
  - a short note describing the generated evaluation artifacts.

## Summary
These changes turn the prototype from a feature demo into a more evaluatable system by adding:
- quantitative evaluation tooling,
- a larger annotated dataset,
- baseline comparison,
- configurable risk thresholds,
- explainability consistency,
- and report-ready figures.

## Practical Notes
- The evaluation dataset remains a prototype and should be expanded further before publication-grade claims.
- The new code and artifacts support stronger evidence for threshold selection and deployment claims.

### Evaluation and Validation
- Added `evaluate.py` to run an end-to-end evaluation pipeline.
- Added `app/services/evaluation.py` with:
  - annotated idea/patent pair processing
  - TF-IDF baseline similarity comparison
  - confusion matrix and per-class precision/recall support
  - threshold grid search for High/Medium/Low risk boundaries
  - bootstrap confidence interval for accuracy
  - McNemar test for model comparison
  - example failure case extraction
- Added a sample annotated dataset in `data/evaluation_dataset.json`.

### Threshold and Classification
- Updated risk threshold defaults in `app/config.py`:
  - `HIGH_THRESHOLD = 80`
  - `MEDIUM_THRESHOLD = 50`
- Made thresholds configurable via environment variables.
- Changed risk classification in `app/services/risk.py` to use inclusive (`>=`) cutoffs.
- Updated LLM fallback explanation text to reference configurable thresholds.

### Model and Explainability Rationale
- Added `EMBEDDING_MODEL_NAME` config for the sentence transformer model.
- Added explanation of why `all-MiniLM-L6-v2` is used for this prototype.
- Documented the caveat that domain-specific models like PatentBERT, LegalBERT, and MPNet are stronger candidates for future research but require fine-tuning.

### Documentation
- Extended `README.md` with:
  - project overview
  - recent improvements
  - evaluation instructions
  - project summary
- Added `sentence-transformers` to `requirements.txt`.

## Practical Notes
- The current evaluation dataset is still small and intended for prototype demonstration only.
- A larger, legally-reviewed annotation dataset is needed for publication-grade claims.
- The evaluation script helps support claims about threshold selection, baseline performance, and statistical significance.

## Next Steps
- Expand the annotated dataset with more real patent/idea pairs.
- Add ROC/threshold tuning visualizations, if possible.
- Add explicit evaluation for LLM-powered explainability quality.
- Add a more detailed literature comparison section in the documentation.
- Collect legal expert annotations for ground-truth risk labels and explanation quality.
