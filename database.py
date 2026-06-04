import sqlite3
import os
from datetime import datetime


class Database:
    """
    Handles all SQLite operations for the chatbot.
    Demonstrates OOPs: encapsulation, single responsibility.
    """

    def __init__(self, db_path: str = "chatbot.db"):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        """Create and return a new DB connection."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enables dict-style access
        return conn

    def _init_db(self):
        """Create tables if they don't already exist."""
        with self._get_connection() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS sessions (
                    id          TEXT PRIMARY KEY,
                    created_at  TEXT NOT NULL,
                    title       TEXT
                );

                CREATE TABLE IF NOT EXISTS messages (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id  TEXT NOT NULL,
                    role        TEXT NOT NULL CHECK(role IN ('user', 'assistant')),
                    content     TEXT NOT NULL,
                    created_at  TEXT NOT NULL,
                    FOREIGN KEY (session_id) REFERENCES sessions(id) ON DELETE CASCADE
                );
            """)

    # ── Sessions ────────────────────────────────────────

    def create_session(self, session_id: str, title: str = "New chat") -> None:
        """Insert a new session row."""
        with self._get_connection() as conn:
            conn.execute(
                "INSERT OR IGNORE INTO sessions (id, created_at, title) VALUES (?, ?, ?)",
                (session_id, datetime.utcnow().isoformat(), title)
            )

    def update_session_title(self, session_id: str, title: str) -> None:
        """Set the session title to the first user message (truncated)."""
        with self._get_connection() as conn:
            conn.execute(
                "UPDATE sessions SET title = ? WHERE id = ?",
                (title[:60], session_id)
            )

    def get_all_sessions(self) -> list:
        """Return all sessions ordered by most recent first."""
        with self._get_connection() as conn:
            rows = conn.execute(
                "SELECT id, title, created_at FROM sessions ORDER BY created_at DESC"
            ).fetchall()
        return [dict(r) for r in rows]

    def delete_session(self, session_id: str) -> None:
        """Delete session and cascade-delete all its messages."""
        with self._get_connection() as conn:
            conn.execute("DELETE FROM sessions WHERE id = ?", (session_id,))

    # ── Messages ────────────────────────────────────────

    def save_message(self, session_id: str, role: str, content: str) -> None:
        """Save a message and auto-create the session if new."""
        # Create session if it doesn't exist yet
        self.create_session(session_id)

        with self._get_connection() as conn:
            conn.execute(
                "INSERT INTO messages (session_id, role, content, created_at) VALUES (?, ?, ?, ?)",
                (session_id, role, content, datetime.utcnow().isoformat())
            )

        # Use first user message as session title
        if role == "user":
            count = self._message_count(session_id)
            if count == 1:
                self.update_session_title(session_id, content)

    def get_messages(self, session_id: str) -> list:
        """Return all messages for a session in order."""
        with self._get_connection() as conn:
            rows = conn.execute(
                "SELECT role, content, created_at FROM messages WHERE session_id = ? ORDER BY id ASC",
                (session_id,)
            ).fetchall()
        return [dict(r) for r in rows]

    def _message_count(self, session_id: str) -> int:
        """Count messages in a session."""
        with self._get_connection() as conn:
            result = conn.execute(
                "SELECT COUNT(*) FROM messages WHERE session_id = ?",
                (session_id,)
            ).fetchone()
        return result[0]
