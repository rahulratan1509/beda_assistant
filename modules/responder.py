# modules/responder.py

import requests
from modules.web_search import perform_web_search

LLM_ENDPOINT = "http://127.0.0.1:1234/v1/chat/completions"

def generate_response(user_input, history, search_enabled=False):
    # ✅ Only trigger search if user explicitly types "search:"
    if user_input.lower().startswith("search:"):
        query = user_input[len("search:"):].strip()
        print(f"[🔎 Manual Web Search Triggered] Query: {query}")  # Developer log only
        return perform_web_search(query)  # ✅ No debug info shown to user

    # 🔧 Placeholder for auto-trigger search in future
    # if search_enabled and should_trigger_search(user_input): ...

    # 🧠 System prompt
    system_prompt = {
        "role": "system",
        "content": (
            "You are Beda, a calm, caring, and helpful assistant. "
            "You answer clearly and concisely. Avoid guessing. "
            "Do not invent web results. Only trigger web search if the user prompt starts with 'search:'."
        )
    }

    messages = [system_prompt] + [{"role": role, "content": msg} for role, msg in history]
    messages.append({"role": "user", "content": user_input})

    payload = {
        "model": "llama-3.2-1b-instruct",
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 4000,
    }

    try:
        res = requests.post(LLM_ENDPOINT, json=payload)
        res.raise_for_status()
        return res.json()['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"[❌ LLM Error] {e}")  # Dev-side
        return "❌ Sorry, something went wrong while generating a response."
