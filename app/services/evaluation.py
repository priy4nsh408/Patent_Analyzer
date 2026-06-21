import json
import math
import os
import random
from collections import Counter
from typing import Any, Dict, List, Tuple

import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import (
    accuracy_score,
    auc,
    confusion_matrix,
    precision_recall_fscore_support,
    roc_curve,
)
from sklearn.preprocessing import label_binarize

from app.services.llm import generate_explanation
from app.services.risk import classify_risk
from app.services.similarity import compute_similarity
from app.services.similarity_type import similarity_type
from app.config import HIGH_THRESHOLD, MEDIUM_THRESHOLD


def load_evaluation_dataset(dataset_path: str) -> List[Dict[str, Any]]:
    with open(dataset_path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_patent_text(entry: Dict[str, Any]) -> str:
    return " ".join([
        entry.get("patent_title", ""),
        entry.get("patent_abstract", ""),
        entry.get("patent_claims", ""),
    ]).strip()


def evaluate_similarity_pairs(entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    results = []

    for item in entries:
        idea = item["idea"]
        patent = {
            "title": item.get("patent_title", ""),
            "abstract": item.get("patent_abstract", ""),
            "claims": item.get("patent_claims", ""),
        }
        patent_text = build_patent_text(item)
        score = compute_similarity(idea, patent)
        predicted_risk = classify_risk(score)
        sim_type = similarity_type(idea, patent)

        results.append({
            "idea": idea,
            "patent": patent,
            "patent_text": patent_text,
            "true_risk": item["true_risk"],
            "score": score,
            "predicted_risk": predicted_risk,
            "sim_type": sim_type,
        })

    return results


def baseline_tfidf_similarity(entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    texts = []
    for item in entries:
        texts.append(item["idea"])
        texts.append(build_patent_text(item))

    vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
    vectorizer.fit(texts)

    baseline_results = []
    for item in entries:
        idea_vec = vectorizer.transform([item["idea"]])
        patent_vec = vectorizer.transform([build_patent_text(item)])
        dot_result = idea_vec @ patent_vec.T
        score = float(dot_result.toarray()[0][0]) * 100
        predicted_risk = classify_risk(score)
        baseline_results.append({
            "idea": item["idea"],
            "patent_text": build_patent_text(item),
            "true_risk": item["true_risk"],
            "score": round(score, 2),
            "predicted_risk": predicted_risk,
        })

    return baseline_results


def risk_classification_metrics(true_labels: List[str], predicted_labels: List[str]) -> Dict[str, Any]:
    labels = ["High", "Medium", "Low"]
    acc = accuracy_score(true_labels, predicted_labels)
    precision, recall, f1, support = precision_recall_fscore_support(
        true_labels,
        predicted_labels,
        labels=labels,
        zero_division=0,
    )
    cm = confusion_matrix(true_labels, predicted_labels, labels=labels)

    return {
        "accuracy": round(acc * 100, 2),
        "precision": [round(x * 100, 2) for x in precision],
        "recall": [round(x * 100, 2) for x in recall],
        "f1": [round(x * 100, 2) for x in f1],
        "support": support.tolist() if hasattr(support, "tolist") else list(support),
        "labels": labels,
        "confusion_matrix": cm.tolist(),
    }


def threshold_grid_search(
    entries: List[Dict[str, Any]],
    high_range: Tuple[int, int] = (70, 91),
    medium_range: Tuple[int, int] = (40, 71),
    step: int = 5,
) -> Dict[str, Any]:
    best = {
        "high_threshold": HIGH_THRESHOLD,
        "medium_threshold": MEDIUM_THRESHOLD,
        "f1": 0,
        "accuracy": 0,
        "metrics": None,
    }

    scores = [item["score"] for item in entries]
    labels = [item["true_risk"] for item in entries]

    for high in range(high_range[0], high_range[1], step):
        for medium in range(medium_range[0], min(high, medium_range[1]), step):
            predictions = [
                "High" if s >= high else "Medium" if s >= medium else "Low"
                for s in scores
            ]
            metrics = risk_classification_metrics(labels, predictions)
            macro_f1 = sum(metrics["f1"]) / len(metrics["f1"])

            if macro_f1 > best["f1"] or (
                macro_f1 == best["f1"] and metrics["accuracy"] > best["accuracy"]
            ):
                best.update({
                    "high_threshold": high,
                    "medium_threshold": medium,
                    "f1": macro_f1,
                    "accuracy": metrics["accuracy"],
                    "metrics": metrics,
                })

    return best


def plot_roc_curves(results: List[Dict[str, Any]], output_dir: str = "reports") -> str:
    os.makedirs(output_dir, exist_ok=True)
    labels = ["High", "Medium", "Low"]
    y_true = [item["true_risk"] for item in results]
    y_score = [item["score"] for item in results]
    y_bin = label_binarize(y_true, classes=labels)

    plt.figure(figsize=(8, 6))
    for i, label in enumerate(labels):
        fpr, tpr, _ = roc_curve(y_bin[:, i], y_score)
        roc_auc = auc(fpr, tpr)
        plt.plot(fpr, tpr, label=f"{label} (AUC = {roc_auc:.2f})")

    plt.plot([0, 1], [0, 1], "--", color="#888")
    plt.title("ROC Curve for Risk Classification")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.legend(loc="lower right")
    plt.grid(True, alpha=0.2)

    file_path = os.path.join(output_dir, "roc_curve.png")
    plt.savefig(file_path, bbox_inches="tight")
    plt.close()
    return file_path


def plot_threshold_analysis(results: List[Dict[str, Any]], output_dir: str = "reports") -> str:
    os.makedirs(output_dir, exist_ok=True)
    thresholds = list(range(40, 96, 5))
    accuracies = []
    macro_f1s = []
    true_labels = [item["true_risk"] for item in results]
    scores = [item["score"] for item in results]

    for high in thresholds:
        predictions = [
            "High" if s >= high else "Medium" if s >= MEDIUM_THRESHOLD else "Low"
            for s in scores
        ]
        metrics = risk_classification_metrics(true_labels, predictions)
        accuracies.append(metrics["accuracy"])
        macro_f1s.append(sum(metrics["f1"]) / len(metrics["f1"]))

    plt.figure(figsize=(8, 6))
    plt.plot(thresholds, accuracies, marker="o", label="Accuracy")
    plt.plot(thresholds, macro_f1s, marker="s", label="Macro F1")
    plt.title("Threshold Tuning: High Threshold vs Performance")
    plt.xlabel("High Threshold")
    plt.ylabel("Score (%)")
    plt.xticks(thresholds)
    plt.legend()
    plt.grid(True, alpha=0.2)

    file_path = os.path.join(output_dir, "threshold_analysis.png")
    plt.savefig(file_path, bbox_inches="tight")
    plt.close()
    return file_path


def evaluate_explainability(
    results: List[Dict[str, Any]],
    sample_count: int = 5,
    output_dir: str = "reports",
) -> Dict[str, Any]:
    os.makedirs(output_dir, exist_ok=True)

    criteria = {
        "risk_mentioned": ["risk", "high", "medium", "low"],
        "score_mentioned": ["score", "%"],
        "difference_mentioned": ["difference", "overlap", "variation", "distinct", "different"],
        "suggestion_mentioned": ["suggest", "recommend", "should", "consider", "improve"],
        "similarity_mentioned": ["similarity", "overlap", "match", "related"],
    }

    sample_results = random.sample(results, min(sample_count, len(results)))
    evaluations = []

    for item in sample_results:
        explanation = generate_explanation(
            item["idea"],
            item["patent"],
            item["score"],
            item["predicted_risk"],
            item["sim_type"],
        )
        lower_text = explanation.lower()
        matched = {
            name: any(token in lower_text for token in tokens)
            for name, tokens in criteria.items()
        }
        quality_score = round(sum(matched.values()) / len(criteria) * 100, 2)

        evaluations.append({
            "idea": item["idea"],
            "true_risk": item["true_risk"],
            "predicted_risk": item["predicted_risk"],
            "score": item["score"],
            "quality_score": quality_score,
            "matched_criteria": matched,
            "explanation": explanation,
        })

    output_path = os.path.join(output_dir, "explainability_samples.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(evaluations, f, indent=2, ensure_ascii=False)

    avg_quality = round(sum(item["quality_score"] for item in evaluations) / len(evaluations), 2)
    criteria_hits = {
        name: sum(1 for item in evaluations if item["matched_criteria"][name])
        for name in criteria
    }

    return {
        "average_quality_score": avg_quality,
        "criteria_hits": criteria_hits,
        "sample_evaluations": evaluations,
        "output_path": output_path,
    }


def bootstrap_confidence_interval(
    true_labels: List[str],
    predicted_labels: List[str],
    metric: str = "accuracy",
    samples: int = 1000,
    alpha: float = 0.05,
) -> Tuple[float, float]:
    n = len(true_labels)
    values = []

    for _ in range(samples):
        indices = [random.randrange(n) for _ in range(n)]
        sample_true = [true_labels[i] for i in indices]
        sample_pred = [predicted_labels[i] for i in indices]

        if metric == "accuracy":
            values.append(accuracy_score(sample_true, sample_pred))
        else:
            values.append(precision_recall_fscore_support(
                sample_true,
                sample_pred,
                average="macro",
                zero_division=0,
            )[2])

    values.sort()
    lower = values[int((alpha / 2) * len(values))]
    upper = values[int((1 - alpha / 2) * len(values))]
    return round(lower * 100, 2), round(upper * 100, 2)


def mcnemar_test(predictions_a: List[str], predictions_b: List[str], true_labels: List[str], target: str = "High") -> Dict[str, Any]:
    b = 0
    c = 0

    for a, b_pred, true in zip(predictions_a, predictions_b, true_labels):
        if a == target and b_pred != target:
            b += 1
        elif a != target and b_pred == target:
            c += 1

    statistic = 0.0
    p_value = 1.0
    if b + c > 0:
        statistic = ((abs(b - c) - 1) ** 2) / (b + c)
        p_value = math.erfc(math.sqrt(statistic / 2))

    return {
        "target_label": target,
        "b": b,
        "c": c,
        "chi2_statistic": round(statistic, 4),
        "p_value": round(p_value, 6),
    }


def summarize_distribution(entries: List[Dict[str, Any]]) -> Dict[str, int]:
    return dict(Counter(item["true_risk"] for item in entries))
