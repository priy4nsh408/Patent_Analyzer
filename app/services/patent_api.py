import requests
import json
import os
from bs4 import BeautifulSoup
from app.config import LENS_API_URL, LENS_API_KEY, SERPAPI_KEY, TOP_K


# 🔹 CLEAN TEXT
def clean_text(text):
    if not text:
        return "No abstract available"
    return text.replace("...", "").strip()


# 🔹 EXTRACT CLAIMS FROM API
def extract_claims(p):
    claims_text = ""

    claims_data = p.get("claims")

    if isinstance(claims_data, list):
        for claim in claims_data:
            claims_text += claim.get("text", "") + "\n\n"

    elif isinstance(claims_data, dict):
        claims_text = claims_data.get("text", "")

    return claims_text.strip()


# 🔥 🔹 SCRAPE CLAIMS FROM LENS WEBSITE (IMPORTANT)
def scrape_claims_from_lens(link, max_claims=4):
    try:
        print("🌐 Scraping claims from Lens fulltext page...")

        response = requests.get(link, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        claims = []

        # 🔥 Method 1: claim-text tags (BEST CASE)
        claim_tags = soup.find_all("claim-text")
        if claim_tags:
            for c in claim_tags[:max_claims]:
                claims.append(c.get_text(strip=True))

        # 🔥 Method 2: fallback parsing numbered claims
        if not claims:
            text = soup.get_text(separator="\n")
            lines = text.split("\n")

            for line in lines:
                line = line.strip()
                if line.startswith(("1.", "2.", "3.", "4.")):
                    claims.append(line)

        if claims:
            return "\n\n".join(claims[:max_claims])

        return "No claims extracted"

    except Exception as e:
        print("❌ Scraping error:", e)
        return "No claims available"


# 🔹 PRIMARY: LENS API
def fetch_from_lens(query):
    headers = {
        "Authorization": f"Bearer {LENS_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "query": {
            "query_string": {
                "query": query
            }
        },
        "size": TOP_K,
        "include": [
            "biblio",
            "claims",
            "lens_id"
        ]
    }

    try:
        print("🔍 Trying Lens API...")
        response = requests.post(LENS_API_URL, json=body, headers=headers)

        print("Lens Status:", response.status_code)

        patents = []

        if response.status_code == 200:
            data = response.json()
            print("Lens Data Count:", len(data.get("data", [])))

            for p in data.get("data", []):

                title = ""
                abstract = ""

                # 🔹 Extract title & abstract safely
                if p.get("biblio"):
                    if p["biblio"].get("invention_title"):
                        title = p["biblio"]["invention_title"][0].get("text", "")

                    if p["biblio"].get("abstract"):
                        abstract = p["biblio"]["abstract"][0].get("text", "")

                # 🔹 Extract claims from API
                claims = extract_claims(p)

                # 🔥 Fallback to scraping if claims missing
                if not claims or len(claims) < 50:
                    lens_id = p.get("lens_id")
                    link = f"https://www.lens.org/lens/patent/{lens_id}/fulltext"
                    claims = scrape_claims_from_lens(link, max_claims=4)

                if not claims:
                    claims = "No claims available"

                # 🔥 Combine everything (BEST FOR LLM)
                full_text = f"{title}\n\n{abstract}\n\n--- CLAIMS ---\n\n{claims}"

                patents.append({
                    "title": title,
                    "abstract": full_text,
                    "claims": claims,
                    "link": f"https://www.lens.org/lens/patent/{p.get('lens_id')}"
                })

        return patents

    except Exception as e:
        print("❌ Lens API Error:", e)
        return []


# 🔹 FALLBACK: SERPAPI
def fetch_from_serpapi(query):
    try:
        print("🔍 Using SerpAPI...")

        url = "https://serpapi.com/search"

        params = {
            "engine": "google_patents",
            "q": query,
            "api_key": SERPAPI_KEY
        }

        response = requests.get(url, params=params)

        print("SerpAPI Status:", response.status_code)

        patents = []

        if response.status_code == 200:
            data = response.json()

            for result in data.get("organic_results", [])[:TOP_K]:
                title = result.get("title", "")
                abstract = clean_text(result.get("snippet", ""))

                full_text = f"{title}\n\n{abstract}"

                patents.append({
                    "title": title,
                    "abstract": full_text,
                    "claims": "Not available (SerpAPI limitation)",
                    "link": result.get("link", "")
                })

        return patents

    except Exception as e:
        print("❌ SerpAPI Error:", e)
        return []


# 🔥 MAIN FUNCTION
def fetch_patents(query):

    if LENS_API_KEY:
        patents = fetch_from_lens(query)
        if patents:
            print("✅ Using Lens data")
            return patents
        else:
            print("⚠️ Lens returned no useful data")

    patents = fetch_from_serpapi(query)
    if patents:
        print("✅ Using SerpAPI data")
        return patents

    print("⚠️ No API returned useful data")
    return []