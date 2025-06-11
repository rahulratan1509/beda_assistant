import requests
import json
from modules.memory_manager import save_fact

LM_API_URL = "http://localhost:1234/v1/chat/completions"

SYSTEM_PROMPT = {
    "role": "system",
    "content": "You are a fact extractor. Extract facts like name, age, job, location, preferences, etc. from the user's message and return them as a JSON list of strings. Format: [\"User's name is X\", \"User is Y years old\"]. Do not include code block markers or explanations."
}

def extract_facts_from_input(user_input):
    try:
        messages = [
            SYSTEM_PROMPT,
            {"role": "user", "content": user_input}
        ]

        payload = {
            "model": "llama-3.2-1b-instruct",
            "messages": messages,
            "stream": False
        }

        response = requests.post(LM_API_URL, json=payload)
        result = response.json()
        content = result['choices'][0]['message']['content']

        # ✅ Remove code block markers like ``` or ```json
        if content.startswith("```"):
            content = content.strip("`").strip()
            if "\n" in content:
                content = "\n".join(content.split("\n")[1:])  # remove 'json' or blank line at the top

        # ✅ Parse the cleaned JSON string
        facts = json.loads(content)

        for fact in facts:
            save_fact(fact=fact.strip(), context=user_input)

        return facts

    except Exception as e:
        print("[Fact Extractor Error]", e)
        return []
