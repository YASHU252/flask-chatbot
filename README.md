# 🤖 AI Chatbot — Flask + OpenAI + SQLite

A full-stack conversational AI chatbot with persistent chat history, built using Flask, the OpenAI GPT API, and SQLite. Features a dark-themed chat UI with a session history sidebar and one-click Railway deployment.

---

## 🚀 Features

- **Persistent chat history** — all conversations saved to SQLite, survive server restarts
- **Session sidebar** — browse, load, and delete past conversations
- **Multi-turn memory** — full context passed to GPT on every message
- **OOPs database layer** — clean `Database` class with encapsulated SQLite logic
- **REST API backend** — Flask endpoints for chat, history, sessions
- **Production-ready** — Gunicorn + Railway deployment config included

---

## 🗂 Project Structure

```
flask_chatbot/
├── app.py              # Flask routes + OpenAI integration
├── database.py         # Database class — all SQLite logic (OOPs)
├── requirements.txt    # Dependencies
├── Procfile            # Gunicorn start command for deployment
├── railway.json        # Railway platform config
├── .env.example        # Environment variable template
├── .gitignore
└── templates/
    └── index.html      # Chat UI with sidebar, history, suggestions
```

---

## ⚙️ Local Setup

```bash
# 1. Clone
git clone https://github.com/yourusername/flask-chatbot.git
cd flask-chatbot

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your OpenAI API key
cp .env.example .env
# Edit .env → paste your key from platform.openai.com

# 5. Run
python app.py
# Visit http://localhost:5000
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Serve the chat UI |
| `POST` | `/chat` | Send a message, get AI reply |
| `GET` | `/sessions` | List all saved sessions |
| `GET` | `/history/<session_id>` | Load messages for a session |
| `DELETE` | `/session/<session_id>` | Delete a session |

### POST `/chat` — Example

**Request:**
```json
{ "message": "Explain Python OOPs", "session_id": "sess_abc123" }
```

**Response:**
```json
{ "reply": "OOPs stands for Object-Oriented Programming...", "session_id": "sess_abc123" }
```

---

## 🗄 Database Schema

```sql
CREATE TABLE sessions (
    id         TEXT PRIMARY KEY,
    created_at TEXT NOT NULL,
    title      TEXT               -- auto-set to first user message
);

CREATE TABLE messages (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    role       TEXT NOT NULL,     -- 'user' or 'assistant'
    content    TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
);
```

---

## ☁️ Deploy to Railway (Free)

1. Push your code to GitHub
2. Go to [railway.app](https://railway.app) → **New Project** → **Deploy from GitHub**
3. Select your repo
4. Go to **Variables** tab → add:
   ```
   OPENAI_API_KEY = sk-your-key-here
   SECRET_KEY     = any-random-string
   ```
5. Railway auto-detects `Procfile` and deploys. Your live URL appears in ~2 minutes.

> **Note:** Railway's free tier resets the filesystem, so SQLite data clears on redeploy. For persistent storage on Railway, swap SQLite for their free PostgreSQL add-on.

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.11, Flask 3.0 |
| AI | OpenAI GPT-3.5-turbo |
| Database | SQLite (via Python sqlite3) |
| Frontend | HTML, CSS, Vanilla JS |
| Server | Gunicorn |
| Deployment | Railway |

---

## 💡 Concepts Demonstrated

- **OOPs** — `Database` class with encapsulation, private methods (`_init_db`, `_get_connection`)
- **REST API** — 5 endpoints with proper HTTP methods and JSON responses
- **SQL** — `CREATE TABLE`, `INSERT`, `SELECT`, `DELETE`, `FOREIGN KEY`, cascade delete
- **Flask** — routing, sessions, `jsonify`, `request.get_json()`
- **Git** — `.gitignore` protects `.env` and `chatbot.db`
- **Deployment** — Procfile, environment variables, production server

---

## 📄 License
MIT — free to use and modify.
