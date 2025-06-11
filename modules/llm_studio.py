# modules/llm_studio.py
import requests
import json

class LMStudioClient:
    def __init__(self, base_url="http://127.0.0.1:1234/v1"):
        self.base_url = base_url

    def stream_response(self, prompt, max_tokens=1000):  # increased token limit
        payload = {
            "model": "llama-3.2-1b-instruct",
            "messages": [
                {"role": "system", "content": "You are Beda, a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": max_tokens,
            "stream": True
        }

        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                json=payload,
                headers=headers,
                stream=True,
                timeout=60
            )
            response.raise_for_status()

            for line in response.iter_lines(decode_unicode=True):
                if line and line.startswith("data: "):
                    if line.strip() == "data: [DONE]":
                        break
                    try:
                        json_data = json.loads(line[len("data: "):])
                        delta = json_data["choices"][0]["delta"]
                        content = delta.get("content", "")
                        if content:
                            yield content
                    except Exception:
                        continue
        except Exception as e:
            yield f"\n[Error] {str(e)}"

# Singleton
lm_client = LMStudioClient()

def generate_response_stream(prompt):
    return lm_client.stream_response(prompt)
