# modules/web_search.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()

SERP_API_KEY = os.getenv("SERP_API_KEY")
SEARCH_URL = "https://serpapi.com/search"

def perform_web_search(query):
    if not SERP_API_KEY:
        print("❌ SERP_API_KEY not set in .env")  # Log for dev
        return "❌ Web search is unavailable (API key missing)."

    try:
        params = {
            "q": query,
            "api_key": SERP_API_KEY,
            "engine": "google",
            "num": "3",
            "hl": "en",
            "gl": "us"
        }

        response = requests.get(SEARCH_URL, params=params)

        if response.status_code == 401:
            print("❌ [Web Search Error] 401 Unauthorized — check your API key in .env.")
            return "❌ Web search failed: Invalid API key."

        response.raise_for_status()
        data = response.json()
        results = data.get("organic_results", [])

        if not results:
            return "⚠️ No results found."

        output = ""
        for i, r in enumerate(results[:3], 1):
            title = r.get("title", "No title")
            link = r.get("link", "#")
            snippet = r.get("snippet", "No snippet available.")
            output += f"{i}. [{title}]({link})\n{snippet}\n\n"

        return output.strip()

    except requests.RequestException:
        print("❌ [Web Search] Network/API failure.")
        return "❌ Web search is temporarily unavailable."

    except Exception as e:
        print(f"❌ [Unexpected Web Search Error] {e}")
        return "❌ An unexpected error occurred during web search."
