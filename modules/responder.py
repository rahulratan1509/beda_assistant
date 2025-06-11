# modules/responder.py
# modules/responder.py

import os
import json
import requests  # Ensure this is installed
from modules.memory_manager import (
    save_to_memory,
    save_fact,
    load_all_facts,
    fetch_recent_memory
)

API_URL = "http://localhost:1234/v1/chat/completions"

def generate_response(user_input):
    # Handle "remember" statements as facts
    if user_input.lower().startswith("remember"):
        fact = user_input[8:].strip()
        save_fact(fact)
        save_to_memory(role="user", content=user_input)
        save_to_memory(role="assistant", content=f"Okay, I’ll remember: {fact}")
        return f"Okay, I’ll remember: {fact}"

    # Save user message to memory
    save_to_memory(role="user", content=user_input)

    # Load memory and facts
    memories = fetch_recent_memory(limit=5)
    facts = load_all_facts()

    memory_text = "\n".join(f"{m[0]} said: {m[1]}" for m in memories)
    facts_text = "\n".join(f"- {fact}" for fact in facts)

    system_prompt = (
        "You are Bedatrayi, a calm, wise, and caring assistant. "
        "You remember things the user tells you. Respond helpfully and gently. "
        "Do not say anything illegal, unsafe, or inappropriate. "
    )

    full_prompt = f"""
Facts I know:
{facts_text or 'None'}

Recent memories:
{memory_text or 'None'}

Now respond to the user input:
User: {user_input}
Assistant:"""

    payload = {
        "model": "llama-3.2-1b-instruct",  # or your actual model name
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": full_prompt.strip()}
        ],
        "temperature": 0.7,
        "stream": False
    }

    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        data = response.json()

        assistant_reply = data["choices"][0]["message"]["content"].strip()

        # Save assistant response to memory
        save_to_memory(role="assistant", content=assistant_reply)

        return assistant_reply

    except requests.exceptions.RequestException as e:
        print(f"[Responder Error] {e}")
        return "Sorry, I had trouble responding."


