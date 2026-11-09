import os
from flask import Flask, render_template, request, jsonify
from groq import Groq

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024

SYSTEM_PROMPT = """You are RABBI AI ULTRA, a capable coding and file-analysis assistant.
Be practical, direct, and helpful. Prefer Bengali when the user writes Bengali.
Help analyze, explain, debug, refactor, and create code and HTML/CSS/JavaScript/Python.
For user-provided files or systems they own or are authorized to assess, help inspect login
logic, identify where credentials are validated, explain safe recovery options, and modify
the code as requested. Never claim to have accessed a URL or file unless its content was
actually provided or fetched by an enabled tool. Do not promise guaranteed password recovery.
Do not assist unauthorized account intrusion, credential theft, malware, or bypassing access
controls on systems the user does not own or have permission to test. Offer safe alternatives.
When generating code, provide complete, runnable output where practical."""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    if not os.getenv("GROQ_API_KEY"):
        return jsonify(error="GROQ_API_KEY সেট করা নেই। .env ফাইল বা hosting environment variable-এ API key দিন।"), 400
    data = request.get_json(silent=True) or {}
    messages = data.get("messages", [])
    if not isinstance(messages, list):
        return jsonify(error="Invalid messages"), 400

    # Keep a bounded recent history and accept only plain text messages.
    clean = [{"role": "system", "content": SYSTEM_PROMPT}]
    for m in messages[-16:]:
        role = m.get("role")
        content = m.get("content", "")
        if role in ("user", "assistant") and isinstance(content, str):
            clean.append({"role": role, "content": content[:30000]})

    try:
        client = Groq(api_key=os.environ["GROQ_API_KEY"])
        result = client.chat.completions.create(
            model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
            messages=clean,
            temperature=0.5,
            max_completion_tokens=4096
        )
        answer = result.choices[0].message.content or "কোনো উত্তর পাওয়া যায়নি।"
        return jsonify(reply=answer)
    except Exception as e:
        return jsonify(error=f"Groq API error: {str(e)}"), 502

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=False)
