# RABBI AI ULTRA — Hacker Edition

## Run locally
1. Install Python 3.10+.
2. Open terminal in this folder.
3. Create a virtual environment (optional but recommended).
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and set `GROQ_API_KEY`.
6. Load variables from `.env` (or set them in your hosting dashboard).
7. Run: `python app.py`
8. Open `http://127.0.0.1:5000`

For local `.env` loading, install python-dotenv (`pip install python-dotenv`) and add
`from dotenv import load_dotenv; load_dotenv()` near the top of app.py, or export
the environment variables in your shell.

## Deploy
Use a Python-capable host. Start command: `gunicorn app:app`.
Set `GROQ_API_KEY` and optionally `GROQ_MODEL` as environment variables in the host dashboard.
Never put the API key in `static/` or `templates/`.

## Current starter features
- Dark neon-green responsive chat UI
- Groq chat backend
- Recent chat context held in the browser session
- Small text-based code file attachment analysis

This is a starter build. It does not yet fetch arbitrary URLs or execute uploaded code.
Only analyze files and systems you own or are authorized to assess.
