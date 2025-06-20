# modules/web_search.py

import os
import requests
from dotenv import load_dotenv
from newspaper import Article

load_dotenv()
SERP_API_KEY = os.getenv("SERP_API_KEY")
SEARCH_URL = "https://serpapi.com/search"

def perform_web_search(query):
    if not SERP_API_KEY:
        return "❌ Web search unavailable: API key missing."

    try:
        params = {
            "q": query,
            "api_key": SERP_API_KEY,
            "engine": "google",
            "num": "5",
            "hl": "en",
            "gl": "us"
        }

        response = requests.get(SEARCH_URL, params=params)
        if response.status_code == 401:
            return "❌ Web search failed: Invalid API key."

        data = response.json()
        results = data.get("organic_results", [])

        # If snippets are weak or missing, use newspaper3k on top link
        scrape_needed = any(len(r.get("snippet", "")) < 50 for r in results[:3])
        links = [r.get("link") for r in results[:3]]

        references = []
        snippets = []
        for i, result in enumerate(results[:3]):
            title = result.get("title", "No title")
            link = result.get("link", "#")
            snippet = result.get("snippet", "")

            if len(snippet) < 50 and scrape_needed:
                try:
                    article = Article(link)
                    article.download()
                    article.parse()
                    snippet = article.text[:4000].replace("\n", " ")
                except:
                    pass

            references.append(f"[{i+1}] {title} — {link}")
            snippets.append((snippet, i + 1))

        # Create a summary using LLM from snippets
        context = "\n\n".join([f"[{i}] {text}" for text, i in snippets])
        prompt = f"""Summarize the following info naturally in a short paragraph with numbered citations [1], [2], etc. Keep it concise, clear, and objective.

{context}
"""

        from modules.llm_wrapper import call_llm  # We'll define this next
        summary = call_llm(prompt, max_tokens=300)

        return f"{summary}\n\n" + "\n".join(references)

    except Exception as e:
        return f"❌ Web search error: {str(e)}"
