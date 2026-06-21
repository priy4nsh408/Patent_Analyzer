import time
from datetime import datetime
from collections import defaultdict
import re
from app.config import EMBEDDING_MODEL_NAME

# 🔥 In-memory metrics tracking
_metrics_data = {
    "total_analyses": 0,
    "total_time": 0,
    "predictions": [],
    "processing_times": [],
    "model_confidence": [],
    "total_patents_retrieved": 0,
    "patents_per_query": [],
    "test_queries": 0,
    "technology_domains": defaultdict(int),
    "patent_lengths": [],
    "query_history": [],
}

# 📊 Model benchmark data for the currently configured embedding model
MODEL_BENCHMARKS = {
    "model_name": EMBEDDING_MODEL_NAME,
    "accuracy": 0.0,
    "precision": 0.0,
    "recall": 0.0,
    "f1_score": 0.0,
    "avg_processing_time_ms": 0,
    "model_size_mb": 0.0,
    "parameters_million": 0.0,
}

# Default descriptive stats for a known model can be updated here.
MODEL_DESCRIPTORS = {
    "all-MiniLM-L6-v2": {
        "accuracy": 47.9,
        "precision": 48.15,
        "recall": 57.53,
        "f1_score": 53.06,
        "avg_processing_time_ms": 45,
        "model_size_mb": 33.8,
        "parameters_million": 22.7,
    },
    "all-MiniLM-L12-v2": {
        "accuracy": 47.89,
        "precision": 48.15,
        "recall": 57.53,
        "f1_score": 53.06,
        "avg_processing_time_ms": 50,
        "model_size_mb": 55.0,
        "parameters_million": 33.0,
    },
    "GiacomoSignorile/PatentBert-FineTuned": {
        "accuracy": 38.0,
        "precision": 39.58,
        "recall": 86.36,
        "f1_score": 54.29,
        "avg_processing_time_ms": 0,
        "model_size_mb": 438.0,
        "parameters_million": 0.0,
    },
    "all-mpnet-base-v2": {
        "accuracy": 52.0,
        "precision": 50.0,
        "recall": 55.0,
        "f1_score": 52.0,
        "avg_processing_time_ms": 80,
        "model_size_mb": 420.0,
        "parameters_million": 110.0,
    },
}

# 📈 Performance statistics
PERFORMANCE_STATS = {
    "batch_size": 1,
    "avg_confidence": 0.0,
    "std_confidence": 0.0,
    "min_confidence": 0.0,
    "max_confidence": 100.0,
}


def start_timer():
    """Start processing timer"""
    return time.time()


def end_timer(start_time):
    """Calculate elapsed time in milliseconds"""
    elapsed = (time.time() - start_time) * 1000
    _metrics_data["processing_times"].append(elapsed)
    return round(elapsed, 2)


def record_prediction(score, risk_level, prediction_confidence=None):
    """Record a prediction with its score and risk level"""
    if prediction_confidence is None:
        # Calculate confidence based on how extreme the score is
        prediction_confidence = min(abs(score - 50) / 50 * 100, 95)
    
    _metrics_data["predictions"].append({
        "score": score,
        "risk": risk_level,
        "confidence": prediction_confidence,
        "timestamp": datetime.now().isoformat()
    })
    _metrics_data["model_confidence"].append(prediction_confidence)
    _metrics_data["total_analyses"] += 1


def get_session_metrics():
    """Get current session metrics"""
    if not _metrics_data["processing_times"]:
        avg_time = 0
        max_time = 0
        min_time = 0
    else:
        avg_time = sum(_metrics_data["processing_times"]) / len(_metrics_data["processing_times"])
        max_time = max(_metrics_data["processing_times"])
        min_time = min(_metrics_data["processing_times"])

    if not _metrics_data["model_confidence"]:
        avg_confidence = 0
    else:
        avg_confidence = sum(_metrics_data["model_confidence"]) / len(_metrics_data["model_confidence"])

    return {
        "total_analyses": _metrics_data["total_analyses"],
        "avg_processing_time_ms": round(avg_time, 2),
        "max_processing_time_ms": round(max_time, 2),
        "min_processing_time_ms": round(min_time, 2),
        "avg_model_confidence": round(avg_confidence, 2),
        "total_predictions": len(_metrics_data["predictions"]),
    }


def get_model_metrics():
    """Get model benchmark metrics"""
    descriptor = MODEL_DESCRIPTORS.get(EMBEDDING_MODEL_NAME)
    if descriptor:
        return {
            "model_name": EMBEDDING_MODEL_NAME,
            "accuracy": descriptor["accuracy"],
            "precision": descriptor["precision"],
            "recall": descriptor["recall"],
            "f1_score": descriptor["f1_score"],
            "avg_processing_time_ms": descriptor["avg_processing_time_ms"],
            "model_size_mb": descriptor["model_size_mb"],
            "parameters_million": descriptor["parameters_million"],
        }

    return MODEL_BENCHMARKS


def get_risk_distribution():
    """Get distribution of risk levels across predictions"""
    distribution = defaultdict(int)
    for pred in _metrics_data["predictions"]:
        distribution[pred["risk"]] += 1
    
    return dict(distribution)


def get_confidence_stats():
    """Get confidence statistics"""
    if not _metrics_data["model_confidence"]:
        return {
            "avg": 0,
            "min": 0,
            "max": 0,
            "median": 0
        }
    
    confidences = sorted(_metrics_data["model_confidence"])
    avg = sum(confidences) / len(confidences)
    median = confidences[len(confidences) // 2]
    
    return {
        "avg": round(avg, 2),
        "min": round(min(confidences), 2),
        "max": round(max(confidences), 2),
        "median": round(median, 2),
        "total_predictions": len(confidences),
    }


def get_performance_comparison():
    """Compare current session performance vs model benchmarks"""
    session_metrics = get_session_metrics()
    benchmarks = MODEL_BENCHMARKS
    
    comparison = {
        "accuracy_benchmark": benchmarks["accuracy"],
        "precision_benchmark": benchmarks["precision"],
        "recall_benchmark": benchmarks["recall"],
        "f1_score_benchmark": benchmarks["f1_score"],
        "avg_processing_time_benchmark_ms": benchmarks["avg_processing_time_ms"],
        "current_avg_time_ms": session_metrics["avg_processing_time_ms"],
        "time_efficiency_percent": round(
            (1 - session_metrics["avg_processing_time_ms"] / benchmarks["avg_processing_time_ms"]) * 100, 2
        ) if session_metrics["avg_processing_time_ms"] > 0 else 0,
    }
    
    return comparison


def reset_session():
    """Reset session metrics"""
    global _metrics_data
    _metrics_data = {
        "total_analyses": 0,
        "total_time": 0,
        "predictions": [],
        "processing_times": [],
        "model_confidence": [],
    }
