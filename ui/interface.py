import gradio as gr
import os
from modules.responder import generate_response
from modules.session_manager import load_session, save_session, list_sessions, new_session_id

sessions = {}
current_session = new_session_id()


import markdown
from pygments.formatters import HtmlFormatter

import markdown
from pygments.formatters import HtmlFormatter
from markdown.extensions import Extension
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.codehilite import CodeHiliteExtension

def render_chat(history):
    formatter = HtmlFormatter(style="monokai", noclasses=True)
    css = formatter.get_style_defs('.highlight')
    
    rendered = f"<style>{css}</style>"

    for role, msg in history:
        html_msg = markdown.markdown(
            msg,
            extensions=[
                FencedCodeExtension(),
                CodeHiliteExtension(noclasses=True, pygments_style="monokai"),
            ]
        )

        # Inject copy button above each <pre> block
        html_msg = html_msg.replace(
            "<div class=\"codehilite\"><pre>",
            """
            <div class="codehilite" style="position:relative;">
                <button onclick="copyToClipboard(this)" style="position:absolute; top:6px; right:6px; background:#444; color:white; font-size:12px; border:none; border-radius:3px; padding:2px 6px; cursor:pointer;">📋</button>
                <pre>
            """
        )

        align = "right" if role == "user" else "left"
        bubble_color = "#1f1f1f" if role == "user" else "#2c2c2c"

        rendered += f"""
        <div style='text-align:{align}; margin:10px;'>
            <div style='display:inline-block; background-color:{bubble_color}; padding:10px 15px; border-radius:12px; color:white; max-width:85%; overflow-x:auto;'>
                {html_msg}
            </div>
        </div>
        """

    rendered += """
    <script>
    function copyToClipboard(button) {
        const codeBlock = button.parentElement.querySelector("pre");
        navigator.clipboard.writeText(codeBlock.innerText).then(() => {
            button.innerText = "✅";
            setTimeout(() => { button.innerText = "📋"; }, 1000);
        });
    }
    </script>
    """
    return rendered




def chat(user_input, chatbox_html, session_id):
    # Load session history if not already in memory
    if session_id not in sessions:
        sessions[session_id] = load_session(session_id)

    history = sessions[session_id]
    history.append(("user", user_input))

    # Generate response using full history
    response = generate_response(user_input, history)
    history.append(("assistant", response))

    # Save in-memory and to disk
    sessions[session_id] = history
    save_session(session_id, history)

    return "", render_chat(history)


def load_chat(session_id):
    global current_session
    current_session = session_id

    if session_id not in sessions:
        sessions[session_id] = load_session(session_id)

    history = sessions[session_id]
    return gr.update(value=session_id), render_chat(history)


def delete_session(session_id):
    path = os.path.join("data", f"{session_id}.json")
    if os.path.exists(path):
        os.remove(path)
    sessions.pop(session_id, None)
    return gr.update(choices=list_sessions()), "", new_session_id()


def launch_ui():
    with gr.Blocks(css="""
        body { background-color: #000; color: white; font-family: Arial; }
        .gradio-container { color: white; }
        #chat-scroll { overflow-y: auto; height: 500px; border: 1px solid #333; padding: 10px; border-radius: 8px; background-color: #121212; }
        #input-area textarea { background-color: #1f1f1f; color: white; border: 1px solid #555; border-radius: 6px; resize: none; }
        #send-button button { background-color: #333; color: white; border-radius: 6px; padding: 6px 12px; font-size: 18px; }
        #send-button button:hover { background-color: #444; }
    """) as demo:
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### 💬 Sessions", elem_id="sidebar")
                session_list = gr.Radio(choices=list_sessions(), label="Select Session", value=current_session)
                refresh_btn = gr.Button("🔄 Refresh")
                new_btn = gr.Button("➕ New Session")
                delete_btn = gr.Button("🗑️ Delete Session")

            with gr.Column(scale=4):
                session_id_box = gr.Textbox(value=current_session, visible=False)
                chatbox = gr.HTML(render_chat([]), elem_id="chat-scroll")
                with gr.Row(elem_id="input-area"):
                    user_input = gr.Textbox(placeholder="Type your message...", lines=2, scale=9)
                    send_btn = gr.Button("➤", elem_id="send-button", scale=1)

        # Events
        send_btn.click(fn=chat, inputs=[user_input, chatbox, session_id_box], outputs=[user_input, chatbox])
        user_input.submit(fn=chat, inputs=[user_input, chatbox, session_id_box], outputs=[user_input, chatbox])
        session_list.change(fn=load_chat, inputs=session_list, outputs=[session_id_box, chatbox])
        refresh_btn.click(fn=lambda: gr.update(choices=list_sessions()), outputs=session_list)
        new_btn.click(fn=lambda: [new_session_id(), ""], outputs=[session_id_box, chatbox])
        delete_btn.click(fn=delete_session, inputs=session_id_box, outputs=[session_list, chatbox, session_id_box])

    demo.launch()
