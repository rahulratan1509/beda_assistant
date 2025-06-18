# import json
# import logging
# import requests

# # Setup basic logging
# logging.basicConfig(level=logging.INFO)

# # Define your LLM endpoint
# LLM_ENDPOINT = "http://localhost:1234/v1/chat/completions"
# HEADERS = {"Content-Type": "application/json"}

# # 🧠 Fact schema to structure memory
# FACT_SCHEMA = {
#     "name": None,
#     "age": None,
#     "job": None,
#     "gender": None,
#     "preferences": [],
#     "interests": [],
#     "personality": {
#         "introverted": None,
#         "ambitious": None,
#         "optimistic": None
#     },
#     "goals": []
# }

# # ✅ Normalize and clean raw extracted facts
# def clean_facts(raw_json_str):
#     try:
#         data = json.loads(raw_json_str)
#         fixed = {}

#         for key, value in data.items():
#             key = key.strip().lower()
#             if key == "prefrences":
#                 key = "preferences"
#             fixed[key] = value
#         return fixed
#     except Exception as e:
#         logging.error("Failed to parse JSON from model: %s", e)
#         return {}

# # ✅ Merge new extracted facts into schema or existing fact memory
# def merge_into_memory(existing, new):
#     merged = existing.copy()
#     for key, value in new.items():
#         if isinstance(value, dict):
#             merged[key] = merge_into_memory(merged.get(key, {}), value)
#         elif value not in [None, "", [], {}]:
#             merged[key] = value
#     return merged

# # 🧠 Extract structured facts using LLM
# def extract_facts_from_text(conversation: str) -> dict:
#     prompt = """
# You are an intelligent assistant. Your task is to extract structured facts about a user from a conversation.

# Use this exact JSON format:
# {
#   "name": "string or null",
#   "age": integer or null,
#   "job": "string or null",
#   "gender": "string or null",
#   "preferences": ["string"],
#   "interests": ["string"],
#   "personality": {
#     "introverted": true/false/null,
#     "ambitious": true/false/null,
#     "optimistic": true/false/null
#   },
#   "goals": ["string"]
# }

# Only output valid JSON. Do not include comments or explanation.
# """

#     messages = [
#         {"role": "system", "content": prompt},
#         {"role": "user", "content": conversation}
#     ]

#     body = {
#         "model": "llama-3.2-1b-instruct",
#         "temperature": 0.2,
#         "messages": messages,
#         "stream": False
#     }

#     logging.info("🔍 Sending conversation to LLM:\n%s", conversation)

#     try:
#         response = requests.post(LLM_ENDPOINT, headers=HEADERS, json=body)
#         response.raise_for_status()
#         content = response.json()["choices"][0]["message"]["content"]
#         logging.info("✅ Raw model output: %s", content)
#         cleaned = clean_facts(content)
#         merged = merge_into_memory(FACT_SCHEMA, cleaned)
#         return merged
#     except Exception as e:
#         logging.error("❌ Error during fact extraction: %s", e)
#         return {}

# # 🔁 Exported function for responder.py to call
# def extract_facts_from_input(input_text: str) -> dict:
#     return extract_facts_from_text(input_text)

# # 🧪 Manual test
# if __name__ == "__main__":
#     chat = """
# Hey, I'm Rahul. I'm 24 and working as a site engineer at Coal India.
# I like music, anime, and tech. I'm quite introverted but ambitious.
# """
#     extracted = extract_facts_from_input(chat)
#     print(json.dumps(extracted, indent=2))
