import os
import json
import requests

from modules.memory_manager import (
    save_to_memory,
    save_fact,
    load_all_facts,
    fetch_recent_memory
)
# from modules.fact_extractor import extract_facts_from_input

API_URL = "http://localhost:1234/v1/chat/completions"

def generate_response(user_input):
    # Handle explicit remember command
    if user_input.lower().startswith("remember"):
        fact = user_input[8:].strip()
        save_fact(fact)
        save_to_memory("user", user_input)
        save_to_memory("assistant", f"Okay, I’ll remember: {fact}")
        return f"Okay, I’ll remember: {fact}"

    # Save user input to memory
    save_to_memory("user", user_input)

    # Extract facts and store them
    extracted_facts = extract_facts_from_input(user_input)
    if extracted_facts:
        for fact in extracted_facts:
            save_fact(fact)  # ✅ Removed unsupported arguments
            print(f"[Auto-Fact Saved] {fact}")

    # Load recent memory & facts
    memory_items = fetch_recent_memory(limit=5)
    fact_items = load_all_facts()

    memory_text = "\n".join(f"{m[0]} said: {m[1]}" for m in memory_items)
    facts_text = "\n".join(f"- {fact}" for fact in fact_items)

    system_prompt = (
        "You are Bedatrayi, a calm, wise, and caring assistant. "
        "You remember things the user tells you. Respond helpfully and gently. "
        "Do not say anything illegal, unsafe, or inappropriate."
    )

    full_prompt = f"""
Facts I know:
{facts_text or 'None'}

Recent memories:
{memory_text or 'None'}

Now respond to the user input:
User: {user_input}
Assistant:
""".strip()

    payload = {
        "model": "llama-3.2-1b-instruct",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": full_prompt}
        ],
        "temperature": 0.7,
        "stream": False
    }

    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        assistant_reply = result["choices"][0]["message"]["content"].strip()

        save_to_memory("assistant", assistant_reply)
        return assistant_reply

    except requests.exceptions.RequestException as e:
        print(f"[Responder Error] {e}")
        return "Sorry, I had trouble responding."
