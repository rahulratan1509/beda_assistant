import requests
from modules.web_search import perform_web_search

LLM_ENDPOINT = "http://127.0.0.1:1234/v1/chat/completions"

def ask_if_search_needed(user_input):
    check_messages = [
        {"role": "system", "content": "If this user query needs real-time information from the internet, respond ONLY with the word 'SEARCH_NEEDED'. Otherwise, reply with 'NO_SEARCH'."},
        {"role": "user", "content": user_input}
    ]
    payload = {
        "model": "llama-3.2-1b-instruct",
        "messages": check_messages,
        "temperature": 0.0,
        "max_tokens": 5,
    }
    try:
        res = requests.post(LLM_ENDPOINT, json=payload)
        res.raise_for_status()
        decision = res.json()['choices'][0]['message']['content'].strip().upper()
        return decision
    except Exception as e:
        return "NO_SEARCH"  # fallback to normal reply

def generate_response(user_input, history):
    if ask_if_search_needed(user_input) == "SEARCH_NEEDED":
        return perform_web_search(user_input)

    # build chat history for standard LLM response
    messages = [{"role": role, "content": msg} for role, msg in history]
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
        data = res.json()
        return data['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"❌ Error generating response: {str(e)}"
