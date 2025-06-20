# modules/web_search.py

import os
import requests

SEARCHAPI_IO_KEY = os.getenv("SEARCHAPI_IO_KEY")
SEARCHAPI_URL = "https://www.searchapi.io/api/v1/search"

def perform_web_search(query):
    try:
        params = {
            "engine": "duckduckgo",
            "q": query,
            "api_key": SEARCHAPI_IO_KEY
        }
        resp = requests.get(SEARCHAPI_URL, params=params)
        resp.raise_for_status()
        data = resp.json()

        results = data.get("organic_results", [])
        if not results:
            return "⚠️ No results found."

        citations = []
        summary_lines = []

        for i, r in enumerate(results[:3], 1):
            title = r.get("title", "")
            snippet = r.get("snippet", "")
            link = r.get("link", "")
            summary_lines.append(f"{snippet} [{i}]")
            citations.append(f"[{i}] [{title}]({link})")

        summary = "\n".join(summary_lines)
        refs = "\n\nSources:\n" + "\n".join(citations)
        return summary + refs

    except Exception as e:
        return f"❌ Web search failed: {e}"
