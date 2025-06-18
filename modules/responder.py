import requests

# Adjust this if you're using a different local model
LLM_ENDPOINT = "http://127.0.0.1:1234/v1/chat/completions"

def generate_response(user_input, history):
    # Format history into proper prompt format
    messages = []

    for role, message in history:
        if role == "user":
            messages.append({"role": "user", "content": message})
        elif role == "assistant":
            messages.append({"role": "assistant", "content": message})

    # Add current user message
    messages.append({"role": "user", "content": user_input})

    # Send request to the local model
    payload = {
        "model": "llama-3.2-1b-instruct",  # or whatever your model ID is
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
