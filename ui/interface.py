import gradio as gr
import os
import json
from modules.responder import generate_response
from modules.init_db import init_memory_db
init_memory_db()

from modules.memory_manager import save_to_memory, fetch_recent_memory

chat_history = []
SAVE_FILE = "data/chat_history.json"

def chat_with_beda(user_input):
    global chat_history
    if not user_input.strip():
        return chat_history, ""

    user_msg = {"role": "user", "content": user_input}
    chat_history.append(user_msg)
    save_to_memory("user", user_input)

    response = generate_response(user_input)
    assistant_msg = {"role": "assistant", "content": response}
    chat_history.append(assistant_msg)
    save_to_memory("assistant", response)

    # Save to file
    with open(SAVE_FILE, "w") as f:
        json.dump(chat_history, f, indent=2)

    return chat_history, ""

def load_previous_chat():
    global chat_history
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            chat_history = json.load(f)
    return chat_history

def clear_chat():
    global chat_history
    chat_history = []
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)
    return [], ""

def launch_ui():
    with gr.Blocks(css="ui/chatgpt_style.css") as demo:
        with gr.Row():
            with gr.Column(scale=2):
                gr.Markdown("### 📁 Saved Sessions")
                load_btn = gr.Button("📂 Load Previous")
                clear_btn = gr.Button("🧹 Clear Chat")
            with gr.Column(scale=8):
                gr.Markdown("## 🤖 Beda — Personal Assistant", elem_id="header")

                chatbot = gr.Chatbot(label="Chat", elem_id="chatbot", show_copy_button=True, type="messages")

                with gr.Row():
                    user_input = gr.Textbox(placeholder="Talk to Beda...", show_label=False, lines=1, scale=8)
                    send_button = gr.Button("➤", elem_id="send")

                send_button.click(chat_with_beda, inputs=user_input, outputs=[chatbot, user_input])
                user_input.submit(chat_with_beda, inputs=user_input, outputs=[chatbot, user_input])

                load_btn.click(fn=load_previous_chat, outputs=[chatbot])
                clear_btn.click(fn=clear_chat, outputs=[chatbot, user_input])

    demo.launch()
