# modules/responder.py

import requests
from modules.web_search import perform_web_search

LLM_ENDPOINT = "http://127.0.0.1:1234/v1/chat/completions"

def generate_response(user_input, history, search_enabled=False):
    if search_enabled and user_input.lower().startswith("search:"):
        query = user_input[len("search:"):].strip()
        debug_info = f"🔎 [Search triggered manually]\nQuery: {query}"
        result = perform_web_search(query)
        return f"{result}\n\n{debug_info}"

    system_prompt = {
        "role": "system",
        "content": (
            "You are Beda, a calm, caring, and helpful assistant. "
            "You answer clearly and concisely. Avoid guessing. "
            "Do not invent web results. Do not search the web unless explicitly asked."
        )
    }

    messages = [system_prompt] + [{"role": role, "content": msg} for role, msg in history]
    messages.append({"role": "user", "content": user_input})

    payload = {
        "model": "llama-3.2-1b-instruct",
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 512,
    }

    try:
        res = requests.post(LLM_ENDPOINT, json=payload)
        res.raise_for_status()
        return res.json()['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"❌ Error: {e}"
