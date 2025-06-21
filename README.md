# 🤖 Beda Assistant

**Beda Assistant** is a ChatGPT-style local AI assistant powered by open-source LLMs (like LLaMA-3.2), with smart web search, citation-style answers, and token-by-token response streaming. Built with a custom Gradio UI and full memory/session support.

---

## ✨ Features

- ✅ Runs on local LLMs (LLaMA 3, OpenChat, etc.)
- 🔍 Smart web search (Google via SerpAPI or DuckDuckGo fallback)
- 📚 LLM-based summarization of search results with inline citations like `[1]`
- 📰 Full-page scraping via `newspaper3k` when search snippets are weak
- 🧠 LLM self-assessment to decide when to search
- 🧵 Real-time token streaming (like ChatGPT)
- 🗃️ Session-aware chat with memory storage
- 🎛️ Toggle for auto/manual search triggering
- 🧰 Modular & clean architecture (easy to extend)

---

## 📁 Folder Structure

beda_assistant/
├── .env # SerpAPI key and environment settings
├── .gitignore
├── README.md
├── main.py # Launcher script
├── run_beda.bat # Windows launcher
├── push_changes.bat # Git helper
├── generate_file_structure.py
├── project_structure.txt # Auto-generated file map
├── data/ # Memory, logs, session storage (tracked)
├── modules/ # Core modules
│ ├── responder.py # Main LLM + web search logic
│ ├── web_search.py # Google + DuckDuckGo + scraping
│ ├── session_manager.py # In-memory session handling
│ └── llm_wrapper.py # Model calling wrapper
├── ui/
│ └── interface.py # Custom Gradio Blocks UI

yaml
Copy
Edit

---

## ⚙️ Setup Instructions

### ✅ 1. Clone this repo

```bash
git clone https://github.com/your-username/beda_assistant.git
cd beda_assistant
✅ 2. Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
Python 3.10+ is recommended.

✅ 3. Add your .env
Create a .env file in the root directory with this content:

env
Copy
Edit
SERPAPI_KEY=your_actual_key_here
ENABLE_WEB_SEARCH=true
✅ 4. Start the assistant
Run via:

bash
Copy
Edit
python main.py
Or on Windows:

bash
Copy
Edit
run_beda.bat
🔍 Web Search Modes
Mode	Description
Auto	Toggle on in UI. LLM decides when to search
Manual	Prefix with search: for forced search
Fallback	DuckDuckGo used if Google fails
Scraping	Auto-enabled for short or weak results

🧠 Backend Model Info
Make sure your local LLM is running and accessible at:

bash
Copy
Edit
http://127.0.0.1:1234/v1/chat/completions
Supports models like:

llama-3.2-1b-instruct

openchat-3.5

Any OpenAI-compatible local server

📥 Git & .gitignore Notes
To include data/ in Git, ensure this is at the bottom of your .gitignore:

gitignore
Copy
Edit
# Ignore everything in data except tracked files
!data/
Then commit with:

bash
Copy
Edit
git add -f data/
git commit -m "Add data directory"
📝 Example Query
sql
Copy
Edit
Tell me the latest news about AI in healthcare.

-- OR --

search: top LLMs released in 2025
LLM will generate a summarized answer like:

OpenAI’s GPT-4.5 and Meta’s LLaMA-3.2 are dominating the open-source space, with new benchmarks emerging weekly [1][2].

🛠️ Dev Notes
Web search uses Google via SerpAPI

Scraping done via newspaper3k when snippet is < 50 chars

Streaming UI powered by Gradio Blocks with stream=True

🧾 License
MIT License — open source, free to modify and distribute.

🙏 Acknowledgements
Meta AI

SerpAPI

Gradio

Newspaper3k

Built with ❤️ to be your local ChatGPT alternative.

yaml
Copy
Edit

---

Let me know if you want:
- A `requirements.txt` generated
- A project badge setup (e.g., Python version, license)
- GitHub Actions or Hugging Face Spaces integration

Would you like me to generate the file automatically and add it to your repo?
