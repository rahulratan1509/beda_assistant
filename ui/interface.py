# ui/interface.py

import gradio as gr
from modules.responder import generate_response
from modules.memory_manager import save_to_memory, fetch_recent_memory, clear_memory, fetch_facts
from modules.fact_extractor import extract_facts_from_input

chat_history = []
from modules.fact_extractor import extract_facts_from_input

def chat_with_beda(user_input, chat_mode):
    global chat_history
    if not user_input.strip():
        return chat_history, ""

    user_message = {"role": "user", "content": user_input}
    chat_history.append(user_message)
    save_to_memory("user", user_input)

    # Extract facts in the background
    extract_facts_from_input(user_input)

    if chat_mode == "Voice":
        response_text = "🎤 Voice mode coming soon..."
    else:
        response_gen = generate_response(user_input)

        if hasattr(response_gen, "__iter__") and not isinstance(response_gen, str):
            response_text = "".join(response_gen)
        else:
            response_text = str(response_gen)

    assistant_message = {"role": "assistant", "content": response_text}
    chat_history.append(assistant_message)
    save_to_memory("assistant", response_text)

    return chat_history, ""

def show_memory():
    memory = fetch_recent_memory(limit=10)
    return "\n".join(
        f"[{row[5][:19]}] {row[0].capitalize()}: {row[1]}" +
        (f" ({row[2]})" if row[2] else "") for row in memory
    )

def show_facts():
    facts = fetch_facts(limit=10)
    return "\n".join(f"[{row[2][:19]}] 📌 {row[0]} (from: {row[1][:30]}...)" for row in facts)

def launch_ui():
    with gr.Blocks(css="static/style.css") as demo:
        gr.Markdown("## 🤖 Beda — Your Personal AI Companion")

        chat_mode = gr.Radio(["Text", "Voice"], value="Text", label="Mode", interactive=True)
        chatbot = gr.Chatbot(label="Beda Chat", elem_id="chatbot", show_copy_button=True, type="messages")

        with gr.Row():
            user_input = gr.Textbox(placeholder="Say something...", lines=1, show_label=False, scale=9)
            send_button = gr.Button("➤", scale=1)

        with gr.Row():
            clear_chat_button = gr.Button("🗑️ Clear Chat")
            show_memory_button = gr.Button("🧠 Show Memory")
            show_facts_button = gr.Button("📌 Show Facts")
            clear_memory_button = gr.Button("🔁 Clear Memory")

        memory_box = gr.Textbox(label="🧠 Beda's Recent Memory", interactive=False, visible=False)
        fact_box = gr.Textbox(label="📌 Facts Beda Learned", interactive=False, visible=False)

        # Main message send
        send_button.click(chat_with_beda, inputs=[user_input, chat_mode], outputs=[chatbot, user_input])
        user_input.submit(chat_with_beda, inputs=[user_input, chat_mode], outputs=[chatbot, user_input])

        # UI controls
        clear_chat_button.click(lambda: ([], ""), outputs=[chatbot, user_input])

        show_memory_button.click(fn=show_memory, outputs=[memory_box])
        show_memory_button.click(lambda: gr.update(visible=True), outputs=memory_box)

        show_facts_button.click(fn=show_facts, outputs=[fact_box])
        show_facts_button.click(lambda: gr.update(visible=True), outputs=fact_box)

        clear_memory_button.click(fn=clear_memory, outputs=[])
        clear_memory_button.click(lambda: "", outputs=[memory_box, fact_box])

    demo.launch()
