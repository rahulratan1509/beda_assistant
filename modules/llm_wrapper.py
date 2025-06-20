import requests

LLM_ENDPOINT = "http://127.0.0.1:1234/v1/chat/completions"

def call_llm(prompt, max_tokens=300):
    payload = {
        "model": "llama-3.2-1b-instruct",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that summarizes information professionally using markdown and numbered citations."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": max_tokens,
    }

    try:
        response = requests.post(LLM_ENDPOINT, json=payload)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"❌ LLM summarization failed: {e}"
