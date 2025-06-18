import requests
from modules.web_search import perform_web_search

# Adjust this to your local LLM server
LLM_ENDPOINT = "http://127.0.0.1:1234/v1/chat/completions"


def generate_response(user_input, history):
    # 🔎 Check for web search trigger
    if user_input.strip().lower().startswith("search:"):
        query = user_input.strip()[7:].strip()
        if not query:
            return "❌ Please provide a query after 'search:'."
        return perform_web_search(query)

    # 🧠 Format message history for LLM
    messages = []
    for role, message in history:
        messages.append({"role": role, "content": message})
    messages.append({"role": "user", "content": user_input})

    # 📤 Payload for the local model
    payload = {
        "model": "llama-3.2-1b-instruct",  # your model id
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 512,
    }

    try:
        response = requests.post(LLM_ENDPOINT, json=payload)
        response.raise_for_status()
        data = response.json()
        return data['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"❌ Error generating response: {str(e)}"
