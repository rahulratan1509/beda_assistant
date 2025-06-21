# 🤖 Beda Assistant

**Beda Assistant** is a ChatGPT-style local AI assistant powered by open-source LLMs (like LLaMA-3.2), featuring smart web search with citation-style answers, full-page scraping fallback, and token-by-token response streaming. Built with a custom Gradio UI and session-aware memory.

---

## ✨ Features

- ✅ Local LLM support (LLaMA 3, OpenChat, etc.)
- 🔍 Web search via Google (SerpAPI) + DuckDuckGo fallback
- 📚 LLM-powered answer summarization with citations like [1], [2]
- 📰 Auto full-page scraping with `newspaper3k` for short snippets
- 🧠 Smart LLM-based decision to trigger search
- 🧵 Token-by-token streaming responses (like ChatGPT)
- 🗃️ Memory & session support
- 🎛️ Toggle between auto/manual search mode
- 🧰 Modular and extensible Python architecture

---

## 📁 Folder Structure

beda_assistant/
├── .env # API keys and flags
├── .gitignore
├── README.md
├── main.py # Entry point
├── run_beda.bat # Windows launcher
├── push_changes.bat # Git helper
├── generate_file_structure.py
├── project_structure.txt # Generated structure summary
├── data/ # Logs, sessions, memory files
├── modules/
│ ├── responder.py # LLM + search + summarizer
│ ├── web_search.py # Google/DDG + scraping
│ ├── session_manager.py # Chat history & memory
│ └── llm_wrapper.py # Local model wrapper
├── ui/
│ └── interface.py # Gradio-based custom UI


---

## ⚙️ Setup Instructions

### 1. Clone the repo

git clone https://github.com/your-username/beda_assistant.git
cd beda_assistant



### 2. Install dependencies

pip install -r requirements.txt



> ✅ Python 3.10+ recommended

### 3. Add `.env` file

Create a `.env` file with:

SERPAPI_KEY=your_actual_key_here
ENABLE_WEB_SEARCH=true


### 4. Start the assistant

python main.py


Or on Windows:

run_beda.bat



---

## 🔍 Web Search Modes

| Mode     | Description                                  |
|----------|----------------------------------------------|
| Auto     | LLM decides when to perform web search       |
| Manual   | Use `search:` prefix to force search         |
| Fallback | DuckDuckGo used if Google fails              |
| Scraping | Uses `newspaper3k` if snippet is too short   |

---

## 🧠 Compatible LLMs

Runs with any OpenAI-compatible local model server:

http://127.0.0.1:1234/v1/chat/completions



Examples:
- llama-3.2-1b-instruct
- openchat-3.5
- Mistral / Zephyr etc. via OAI-compatible API

---

## 📝 Example Prompts

Tell me the latest news in space exploration.

or force search:
search: top universities for AI research 2025


Sample output:

> MIT and Stanford continue leading in AI research, with ETH Zurich and CMU climbing global ranks [1][2].

---

## 📁 Git Ignore Tips

To track the `data/` directory, update your `.gitignore` like this:

Track data folder
!data/

makefile


Then:

git add -f data/
git commit -m "Track data folder"


---

## 🛠️ Dev Notes

- Google search via SerpAPI (optional API key)
- DuckDuckGo fallback if SerpAPI fails or limit hits
- Scraping enabled when snippet is short (< 50 chars)
- Token streaming powered by Gradio with `stream=True`

---

## 🧾 License

MIT License — free for personal or commercial use.

---

## 🙏 Acknowledgements

- Meta AI (LLaMA)
- SerpAPI
- Gradio
- Newspaper3k

> Built with ❤️ to be your personal, offline ChatGPT.
