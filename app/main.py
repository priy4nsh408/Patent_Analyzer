import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
from app.services.patent_api import fetch_patents
from app.services.similarity import compute_similarity
from app.services.risk import classify_risk
from app.services.similarity_type import similarity_type
from app.services.llm import generate_explanation
from app.services.metrics import (
    start_timer, end_timer, record_prediction,
    get_session_metrics, get_model_metrics, 
    get_risk_distribution, get_confidence_stats,
    get_performance_comparison
)

# 🔹 Page config
st.set_page_config(
    page_title="Patent Analyzer",
    page_icon="🧠",
    layout="wide"
)

# 🔥 Custom Styling (BIG UI IMPROVEMENT)
st.markdown("""
<style>
.big-title {
    font-size:28px !important;
    font-weight:600;
    margin-bottom:10px;
}
.section-title {
    font-size:22px !important;
    font-weight:500;
    margin-top:10px;
}
.explanation-box {
    font-size:18px !important;
    line-height:1.6;
    padding:10px;
    border-radius:10px;
    background-color:#f8f9fa;
}
</style>
""", unsafe_allow_html=True)

# 🔹 Title
st.title("🧠 Patent Similarity & Infringement Analyzer")
st.markdown("Analyze your idea against existing patents using AI + NLP")

# 🔹 Input
user_input = st.text_area(
    "Enter your idea:",
    placeholder="e.g., Smart helmet with alcohol detection and GPS tracking"
)

# 🔹 Analyze Button
if st.button("Analyze"):

    if not user_input.strip():
        st.warning("⚠️ Please enter a valid idea before analyzing.")
        st.stop()

    # 🔄 Start timing
    start_time = start_timer()
    
    # 🔄 Fetch
    with st.spinner("🔍 Fetching patents and analyzing..."):
        patents = fetch_patents(user_input)

    if not patents:
        st.warning("⚠️ No real patent data available.")
        st.stop()

    # 🔹 Compute
    results = []
    for patent in patents:
        score = compute_similarity(user_input, patent)
        risk = classify_risk(score)
        sim_type = similarity_type(user_input, patent)
        
        # 📊 Record metrics
        record_prediction(score, risk)

        results.append((patent, score, risk, sim_type))

    # 🔹 Sort
    results = sorted(results, key=lambda x: x[1], reverse=True)

    # 🔹 Filter
    filtered_results = [r for r in results if r[1] > 10]

    if not filtered_results:
        st.warning("⚠️ No sufficiently relevant patents found.")
        st.stop()

    # ⏱️ End timing
    processing_time = end_timer(start_time)

    # 🔥 Best Match
    best_patent, best_score, _, _ = filtered_results[0]
    st.info(f"🏆 Best Match: {best_patent.get('title','No Title')} ({best_score}%)")

    st.success(f"✅ Found {len(filtered_results)} relevant patents")
    
    # 📊 MODEL ACCURACY & PERFORMANCE METRICS
    st.markdown("### 📊 Model Accuracy & Performance Metrics")
    
    # Get metrics data
    model_metrics = get_model_metrics()
    session_metrics = get_session_metrics()
    perf_comparison = get_performance_comparison()
    confidence_stats = get_confidence_stats()
    risk_dist = get_risk_distribution()
    
    # 🎯 Main Accuracy Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📈 Accuracy", f"{model_metrics['accuracy']}%")
    col2.metric("🎯 Precision", f"{model_metrics['precision']}%")
    col3.metric("🔍 Recall", f"{model_metrics['recall']}%")
    col4.metric("📊 F1-Score", f"{model_metrics['f1_score']}")
    
    # ⏱️ Processing Performance
    col1, col2, col3 = st.columns(3)
    col1.metric("⏱️ Avg Time", f"{session_metrics['avg_processing_time_ms']}ms")
    col2.metric("🤖 Avg Confidence", f"{session_metrics['avg_model_confidence']}%")
    col3.metric("📝 Total Analyses", session_metrics['total_analyses'])
    
    # 📋 Expandable Sections
    with st.expander("📋 Detailed Benchmark Comparison"):
        st.subheader(f"Model Benchmarks ({model_metrics['model_name']})")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Model Name:** {model_metrics['model_name']}")
            st.write(f"**Model Size:** {model_metrics['model_size_mb']} MB")
            st.write(f"**Parameters:** {model_metrics['parameters_million']}M")
        with col2:
            st.write(f"**Benchmark Accuracy:** {model_metrics['accuracy']}%")
            st.write(f"**Avg Processing Time:** {model_metrics['avg_processing_time_ms']}ms")
            st.write(f"**Accuracy Tier:** High-Performance")
    
    with st.expander("📊 Confidence Analysis"):
        st.write(f"**Average Confidence:** {confidence_stats['avg']}%")
        st.write(f"**Median Confidence:** {confidence_stats['median']}%")
        st.write(f"**Range:** {confidence_stats['min']}% - {confidence_stats['max']}%")
        st.write(f"**Predictions Made:** {confidence_stats['total_predictions']}")
    
    with st.expander("⚠️ Risk Distribution"):
        if risk_dist:
            for risk_level, count in risk_dist.items():
                st.write(f"**{risk_level} Risk:** {count} patents")
        else:
            st.write("No risk data available yet")
    
    with st.expander("🚀 Performance vs Benchmarks"):
        st.write(f"**Current Avg Processing Time:** {perf_comparison['current_avg_time_ms']}ms")
        st.write(f"**Benchmark Avg Time:** {perf_comparison['avg_processing_time_benchmark_ms']}ms")
        st.write(f"**Time Efficiency:** {perf_comparison['time_efficiency_percent']}%")
    
    st.markdown("---")
    st.markdown("### 🔍 Analysis Results")

    # 🔹 Display
    for idx, (patent, score, risk, sim_type) in enumerate(filtered_results, 1):

        explanation = generate_explanation(
            user_input, patent, score, risk, sim_type
        )

        with st.container():

            # 🔥 Title
            st.markdown(
                f'<div class="big-title">🔎 Patent {idx}: {patent.get("title","No Title")}</div>',
                unsafe_allow_html=True
            )

            # 🔗 Link
            link = patent.get("link", "").strip()
            if link:
                if not link.startswith("http"):
                    link = "https://" + link

                st.markdown(
                    f'<a href="{link}" target="_blank">🔗 View Full Patent</a>',
                    unsafe_allow_html=True
                )
            else:
                st.write("🔗 No link available")

            # 📊 Metrics
            col1, col2, col3 = st.columns(3)
            col1.metric("Similarity (%)", f"{score}")
            col2.metric("Risk Level", risk)
            col3.metric("Similarity Type", sim_type)

            # 📄 Abstract
            st.markdown('<div class="section-title">📄 Patent Abstract</div>', unsafe_allow_html=True)
            abstract = patent.get("abstract", "No abstract available")
            st.write(abstract)

            # 💬 AI Analysis
            st.markdown('<div class="section-title">🧠 AI Analysis</div>', unsafe_allow_html=True)

            with st.expander("💬 Detailed Explanation"):
                if explanation and explanation.strip():
                    st.markdown(explanation)
                else:
                    st.warning("⚠️ No AI explanation generated. Check LLM connection.")
            st.markdown("---")