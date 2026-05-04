import requests
from app.config import OLLAMA_URL, OLLAMA_MODEL


# 🔥 LIMIT TEXT SIZE (CRITICAL FIX)
def truncate_text(text, max_chars=2000):
    if not text:
        return ""
    if len(text) > max_chars:
        return text[:max_chars] + "\n\n...[truncated]"
    return text


def generate_explanation(user_input, patent, score, risk, sim_type):

    # 🔥 LIMIT INPUT SIZE TO AVOID TIMEOUT
    patent_text = truncate_text(patent.get("abstract", ""), 2000)

    prompt = f"""
You are an expert patent analysis assistant.

Compare the USER IDEA with the PATENT CONTENT and provide a structured explanation.

-----------------------------
USER IDEA:
{user_input}

PATENT CONTENT:
{patent_text}

SIMILARITY SCORE: {score}%
RISK LEVEL: {risk}
SIMILARITY TYPE: {sim_type}
-----------------------------

STRICT RULES:
- Do NOT change risk level
- Use similarity score to justify reasoning
- Be specific (no generic answers)

TASKS:

1. Identify EXACT overlapping features
2. Identify CLEAR differences
3. Justify risk level ({risk}) using score ({score}%)
4. Explain similarity type
5. Suggest SPECIFIC improvements
6. Perform GAP ANALYSIS

FORMAT:

🔍 Analysis:
🔄 Key Differences:
⚖️ Risk Interpretation:
🧩 Similarity Insight:
💡 Suggestions:
⚠️ Disclaimer:
"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=120   # 🔥 Increased timeout
        )

        print("LLM STATUS:", response.status_code)

        if response.status_code == 200:
            data = response.json()
            print("LLM RAW:", data)

            llm_response = data.get("response", "").strip()

            if llm_response and len(llm_response) > 20:
                return llm_response

        print("⚠️ Weak LLM response")

    except Exception as e:
        print("❌ LLM ERROR:", e)

    return dynamic_fallback(user_input, patent, score, risk, sim_type)


# 🔥 IMPROVED FALLBACK (ALIGNED WITH YOUR THRESHOLDS)
def dynamic_fallback(user_input, patent, score, risk, sim_type):

    if score <= 40:
        return f"""
🔍 Analysis:
Minimal overlap between idea and patent.

🔄 Key Differences:
The patent focuses on {patent['title']}, while the idea differs in application.

⚖️ Risk Interpretation:
LOW risk because score ({score}%) ≤ 40%.

🧩 Similarity Insight:
Mostly {sim_type.lower()} similarity.

💡 Suggestions:
- Focus on unique features
- Avoid general overlap

⚠️ Disclaimer:
AI-based analysis.
"""

    elif score <= 75:
        return f"""
🔍 Analysis:
Moderate overlap exists in concepts.

🔄 Key Differences:
Implementation differs despite sharend ideas.

⚖️ Risk Interpretation:
MEDIUM risk because 40% < {score}% ≤ 75%.

🧩 Similarity Insight:
Partial {sim_type.lower()} similarity.

💡 Suggestions:
- Modify architecture
- Add unique modules

⚠️ Disclaimer:
AI-based analysis.
"""

    else:
        return f"""
🔍 Analysis:
Strong overlap in functionality.

🔄 Key Differences:
Only minor variations exist.

⚖️ Risk Interpretation:
HIGH risk because score ({score}%) > 75%.

🧩 Similarity Insight:
Strong {sim_type.lower()} similarity.

💡 Suggestions:
- Redesign core idea
- Introduce novel features

⚠️ Disclaimer:n
AI-based analysis.
""" 