from flask import Flask, render_template, request, jsonify, session
from groq import Groq
from database import Database
from dotenv import load_dotenv
import os
import uuid

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-change-in-production")

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are a helpful, friendly AI assistant.
You give clear, concise answers and maintain a warm, conversational tone.
If you don't know something, say so honestly."""

db = Database()

# ── Routes ──────────────────────────────────────────────

@app.route("/")
def index():
    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()
    session_id   = data.get("session_id") or session.get("session_id", "default")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    db.save_message(session_id, "user", user_message)

    history = db.get_messages(session_id)
    groq_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    groq_messages += [{"role": m["role"], "content": m["content"]} for m in history]

    try:
        response = client.chat.completions.create(
           model="llama-3.1-8b-instant",
            messages=groq_messages,
            max_tokens=1000,
            temperature=0.7
        )
        reply = response.choices[0].message.content
        db.save_message(session_id, "assistant", reply)
        return jsonify({"reply": reply, "session_id": session_id})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/sessions", methods=["GET"])
def get_sessions():
    sessions = db.get_all_sessions()
    return jsonify({"sessions": sessions})


@app.route("/history/<session_id>", methods=["GET"])
def get_history(session_id):
    messages = db.get_messages(session_id)
    return jsonify({"messages": messages})


@app.route("/session/<session_id>", methods=["DELETE"])
def delete_session(session_id):
    db.delete_session(session_id)
    return jsonify({"success": True})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
