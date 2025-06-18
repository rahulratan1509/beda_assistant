import os
import requests
from dotenv import load_dotenv

load_dotenv()

SERP_API_KEY = os.getenv("SERP_API_KEY")
SEARCH_URL = "https://serpapi.com/search"

def perform_web_search(query):
    try:
        # First try using SerpAPI
        params = {
            "q": query,
            "api_key": SERP_API_KEY,
            "engine": "google",
        }
        response = requests.get(SEARCH_URL, params=params)
        response.raise_for_status()
        data = response.json()
        results = data.get("organic_results", [])

        if results:
            return format_results(results[:3])
    except Exception as e:
        print("⚠️ SerpAPI failed, falling back to DuckDuckGo:", e)

    # DuckDuckGo Fallback
    try:
        duck_url = "https://api.duckduckgo.com/"
        duck_params = {
            "q": query,
            "format": "json",
            "no_html": 1,
            "skip_disambig": 1,
        }
        response = requests.get(duck_url, params=duck_params)
        response.raise_for_status()
        data = response.json()
        abstract = data.get("AbstractText")
        related = data.get("RelatedTopics", [])
        
        if abstract:
            return f"📄 {abstract}"

        top_related = []
        for topic in related[:3]:
            if isinstance(topic, dict) and "Text" in topic and "FirstURL" in topic:
                top_related.append(f"🔗 [{topic['Text']}]({topic['FirstURL']})")
        
        return "\n\n".join(top_related) or "No results found."

    except Exception as e:
        return f"❌ Web search failed: {e}"

def format_results(results):
    formatted = ""
    for result in results:
        title = result.get("title", "No Title")
        link = result.get("link", "")
        snippet = result.get("snippet", "")
        formatted += f"🔗 [{title}]({link})\n{snippet}\n\n"
    return formatted.strip()
