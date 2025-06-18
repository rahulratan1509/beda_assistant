# modules/llm_studio.py

import requests

class LMStudioClient:
    def __init__(self, base_url="http://127.0.0.1:1234/v1"):
        self.base_url = base_url

    def get_response(self, system_prompt, user_prompt, model="llama-3.2-1b-instruct"):
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.7,
            "stream": False,
            "max_tokens": 1024
        }

        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"].strip()
        except Exception as e:
            return f"[LLM Error] {str(e)}"

lm_client = LMStudioClient()
