import os
import requests
from dotenv import load_dotenv

load_dotenv()

SERP_API_KEY = os.getenv("SERP_API_KEY")
print("Loaded SERP_API_KEY:", SERP_API_KEY)  # ✅ For debugging

SEARCH_URL = "https://serpapi.com/search"


def perform_web_search(query):
    params = {
        "q": query,
        "api_key": SERP_API_KEY,
        "engine": "google",  # you can use "bing", "duckduckgo", etc.
    }

    try:
        response = requests.get(SEARCH_URL, params=params)
        response.raise_for_status()
        data = response.json()

        results = data.get("organic_results", [])
        if not results:
            return "No results found."

        top_results = ""
        for result in results[:3]:
            title = result.get("title", "")
            link = result.get("link", "")
            snippet = result.get("snippet", "")
            top_results += f"🔗 [{title}]({link})\n{snippet}\n\n"

        return top_results.strip()

    except Exception as e:
        return f"❌ Web search error: {e}"
