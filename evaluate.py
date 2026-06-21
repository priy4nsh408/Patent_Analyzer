import json
import os
from app.services.evaluation import (
    baseline_tfidf_similarity,
    bootstrap_confidence_interval,
    evaluate_explainability,
    evaluate_similarity_pairs,
    load_evaluation_dataset,
    mcnemar_test,
    plot_roc_curves,
    plot_threshold_analysis,
    risk_classification_metrics,
    summarize_distribution,
    threshold_grid_search,
)


def main():
    dataset_path = "data/evaluation_dataset.json"
    entries = load_evaluation_dataset(dataset_path)

    print("Loaded evaluation dataset with", len(entries), "entries")
    print("Class distribution:", summarize_distribution(entries))

    results = evaluate_similarity_pairs(entries)
    true_labels = [item["true_risk"] for item in results]
    predicted_labels = [item["predicted_risk"] for item in results]

    print("\n=== SPAIRD-style similarity evaluation ===")
    spa_metrics = risk_classification_metrics(true_labels, predicted_labels)
    print(json.dumps(spa_metrics, indent=2))

    baseline_results = baseline_tfidf_similarity(entries)
    baseline_labels = [item["predicted_risk"] for item in baseline_results]
    print("\n=== TF-IDF baseline evaluation ===")
    baseline_metrics = risk_classification_metrics(true_labels, baseline_labels)
    print(json.dumps(baseline_metrics, indent=2))

    print("\n=== Threshold grid search ===")
    grid_search = threshold_grid_search(results)
    print(json.dumps(grid_search, indent=2))

    roc_path = plot_roc_curves(results)
    print(f"\nSaved ROC curve plot to: {roc_path}")

    threshold_plot_path = plot_threshold_analysis(results)
    print(f"Saved threshold tuning plot to: {threshold_plot_path}")

    explainability_report = evaluate_explainability(results)
    print("\n=== Explainability evaluation summary ===")
    print(json.dumps({
        "average_quality_score": explainability_report["average_quality_score"],
        "criteria_hits": explainability_report["criteria_hits"],
        "output_path": explainability_report["output_path"],
    }, indent=2))

    print("\n=== Confidence interval for accuracy ===")
    ci_low, ci_high = bootstrap_confidence_interval(true_labels, predicted_labels)
    print(f"Accuracy CI: [{ci_low}%, {ci_high}%]")

    print("\n=== McNemar test for High-risk label ===")
    mcnemar = mcnemar_test(predicted_labels, baseline_labels, true_labels, target="High")
    print(json.dumps(mcnemar, indent=2))

    summary = {
        "dataset_path": dataset_path,
        "entries": len(entries),
        "class_distribution": summarize_distribution(entries),
        "spa_metrics": spa_metrics,
        "baseline_metrics": baseline_metrics,
        "threshold_grid_search": grid_search,
        "roc_path": roc_path,
        "threshold_plot_path": threshold_plot_path,
        "accuracy_confidence_interval": {
            "low": ci_low,
            "high": ci_high,
        },
        "mcnemar": mcnemar,
    }
    summary_path = os.path.join("reports", "evaluation_summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(f"\nSaved evaluation summary to: {summary_path}")

    print("\n=== Example failure cases ===")
    for item, pred in zip(results, predicted_labels):
        if item["true_risk"] != pred:
            print(f"- Idea: {item['idea']}")
            print(f"  Patent: {item['patent_text'][:100]}...")
            print(f"  True: {item['true_risk']}, Predicted: {pred}, Score: {item['score']}%")


if __name__ == "__main__":
    main()
