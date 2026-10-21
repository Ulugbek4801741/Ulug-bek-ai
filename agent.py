import os
import json
import sqlite3
import requests
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory, session
from dotenv import load_dotenv
from backup import create_backup

load_dotenv()

app = Flask(__name__, static_folder=".", static_url_path="")
app.secret_key = os.getenv("SECRET_KEY", "ulug-bek-ai-secret")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_KEY_2 = os.getenv("GEMINI_API_KEY_2")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "A4801741_a")

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
OPENAI_URL = "https://api.openai.com/v1/chat/completions"
DB_PATH = "ulugbek_ai.db"


def db():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = db()
    connection.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        google_id TEXT UNIQUE,
        name TEXT,
        email TEXT,
        picture TEXT,
        created_at TEXT
    );

    CREATE TABLE IF NOT EXISTS chats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_email TEXT,
        question TEXT,
        answer TEXT,
        rating TEXT,
        provider TEXT,
        created_at TEXT
    );

    CREATE TABLE IF NOT EXISTS knowledge (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        content TEXT,
        active INTEGER DEFAULT 1,
        created_at TEXT
    );
    """)
    connection.commit()
    connection.close()


init_db()


@app.route("/")
def home():
    return send_from_directory(".", "index.html")


@app.route("/a7x9q")
def admin_page():
    return send_from_directory(".", "admin.html")


@app.route("/health")
def health():
    try:
        connection = db()
        connection.execute("SELECT 1")
        connection.close()
        database = "ok"
    except Exception:
        database = "error"

    return jsonify({
        "status": "ok" if database == "ok" else "degraded",
        "database": database,
        "gemini_primary": bool(GEMINI_API_KEY),
        "gemini_backup": bool(GEMINI_API_KEY_2),
        "openai_backup": bool(OPENAI_API_KEY)
    })


@app.route("/api/config")
def config():
    return jsonify({"googleClientId": GOOGLE_CLIENT_ID or ""})


def get_knowledge():
    connection = db()
    rows = connection.execute(
        "SELECT title, content FROM knowledge WHERE active = 1 ORDER BY id DESC LIMIT 40"
    ).fetchall()
    connection.close()

    return "\n\n".join(
        f"BILIM: {row['title']}\n{row['content']}" for row in rows
    )


def get_feedback():
    connection = db()
    rows = connection.execute(
        """
        SELECT question, answer, rating FROM chats
        WHERE rating IS NOT NULL
        ORDER BY id DESC LIMIT 25
        """
    ).fetchall()
    connection.close()

    return "\n\n".join(
        f"SAVOL: {row['question']}\nJAVOB: {row['answer']}\nBAHO: {row['rating']}"
        for row in rows
    )


def build_system_prompt(base_prompt):
    prompt = base_prompt
    knowledge = get_knowledge()
    feedback = get_feedback()

    if knowledge:
        prompt += "\n\nADMIN BILIMLARI:\n" + knowledge

    if feedback:
        prompt += "\n\nOLDINGI BAHOLAR ASOSIDA YAXSHIROQ JAVOB BER:\n" + feedback

    return prompt


def ask_gemini(prompt, system_prompt, api_key):
    payload = {
        "system_instruction": {"parts": [{"text": system_prompt}]},
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "tools": [{"google_search": {}}]
    }

    response = requests.post(
        f"{GEMINI_URL}?key={api_key}",
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload),
        timeout=60
    )

    if response.status_code != 200:
        return None

    try:
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        return None


def ask_openai(prompt, system_prompt):
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(
        OPENAI_URL,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}"
        },
        data=json.dumps(payload),
        timeout=60
    )

    if response.status_code != 200:
        return None

    try:
        return response.json()["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        return None


def ask_ai(prompt, base_system):
    system_prompt = build_system_prompt(base_system)

    if GEMINI_API_KEY:
        answer = ask_gemini(prompt, system_prompt, GEMINI_API_KEY)
        if answer:
            return answer, "gemini_primary"

    if GEMINI_API_KEY_2:
        answer = ask_gemini(prompt, system_prompt, GEMINI_API_KEY_2)
        if answer:
            return answer, "gemini_backup"

    if OPENAI_API_KEY:
        answer = ask_openai(prompt, system_prompt)
        if answer:
            return answer, "openai_backup"

    return None, "AI provayderlarining hech biri javob bermadi."


@app.route("/api/login", methods=["POST"])
def login():
    body = request.get_json(silent=True) or {}
    token = body.get("credential")

    if not token:
        return jsonify({"error": "Google tokeni yo‘q."}), 400

    try:
        import base64
        payload_part = token.split(".")[1]
        payload_part += "=" * (-len(payload_part) % 4)
        payload = json.loads(base64.urlsafe_b64decode(payload_part))
    except Exception:
        return jsonify({"error": "Google tokeni noto‘g‘ri."}), 400

    connection = db()
    connection.execute(
        """
        INSERT OR IGNORE INTO users (google_id, name, email, picture, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            payload.get("sub"),
            payload.get("name"),
            payload.get("email"),
            payload.get("picture"),
            datetime.utcnow().isoformat()
        )
    )
    connection.commit()
    connection.close()

    session["user"] = {
        "google_id": payload.get("sub"),
        "name": payload.get("name"),
        "email": payload.get("email"),
        "picture": payload.get("picture")
    }

    return jsonify({"user": session["user"]})


@app.route("/api/logout", methods=["POST"])
def logout():
    session.pop("user", None)
    return jsonify({"ok": True})


@app.route("/api/chat", methods=["POST"])
def chat():
    body = request.get_json(silent=True) or {}
    prompt = (body.get("prompt") or "").strip()
    user = session.get("user") or {}

    if not prompt:
        return jsonify({"error": "Savol bo‘sh bo‘lishi mumkin emas."}), 400

    system = (
        "Sen Ulug'bek AI — professional, kuchli va xavfsiz AI agentsan. "
        "O‘zbek tilida aniq, tahliliy va professional javob ber. "
        "Kerak bo‘lsa Google Search orqali internetdan so‘nggi ma’lumot top. "
        "Maxfiy kalit, parol yoki xavfli kod so‘ralsa, rad et."
    )

    answer, provider = ask_ai(prompt, system)

    if not answer:
        return jsonify({"error": provider}), 503

    connection = db()
    cursor = connection.execute(
        "INSERT INTO chats (user_email, question, answer, provider, created_at) VALUES (?, ?, ?, ?, ?)",
        (user.get("email"), prompt, answer, provider, datetime.utcnow().isoformat())
    )
    chat_id = cursor.lastrowid
    connection.commit()
    connection.close()

    return jsonify({"reply": answer, "chat_id": chat_id, "provider": provider})


@app.route("/api/rate", methods=["POST"])
def rate():
    body = request.get_json(silent=True) or {}
    chat_id = body.get("chat_id")
    rating = body.get("rating")

    if rating not in ("good", "bad"):
        return jsonify({"error": "Baho noto‘g‘ri."}), 400

    connection = db()
    connection.execute("UPDATE chats SET rating = ? WHERE id = ?", (rating, chat_id))
    connection.commit()
    connection.close()

    return jsonify({"ok": True})


@app.route("/api/generate-app", methods=["POST"])
def generate_app():
    body = request.get_json(silent=True) or {}
    prompt = (body.get("prompt") or "").strip()

    if not prompt:
        return jsonify({"error": "Ilova g‘oyasi bo‘sh bo‘lishi mumkin emas."}), 400

    system = (
        "Sen senior frontend dasturchisan. "
        "Foydalanuvchi g‘oyasi asosida bitta to‘liq ishlaydigan, professional, "
        "mobil uchun moslashgan HTML fayl yoz. "
        "Faqat HTML kodini qaytar. Dizayn 100/100 darajasida zamonaviy, "
        "gradient, glassmorphism, animatsiya va toza tipografiyaga ega bo‘lsin."
    )

    code, provider = ask_ai(prompt, system)

    if not code:
        return jsonify({"error": provider}), 503

    code = code.strip()

    if code.startswith("```"):
        code = code.split("\n", 1)[1] if "\n" in code else code
        if code.endswith("```"):
            code = code[:-3]

    return jsonify({"code": code.strip(), "provider": provider})


def admin_required():
    return session.get("admin") is True


@app.route("/api/admin/login", methods=["POST"])
def admin_login():
    body = request.get_json(silent=True) or {}

    if body.get("password") != ADMIN_PASSWORD:
        return jsonify({"error": "Parol noto‘g‘ri."}), 401

    session["admin"] = True
    return jsonify({"ok": True})


@app.route("/api/admin/logout", methods=["POST"])
def admin_logout():
    session.pop("admin", None)
    return jsonify({"ok": True})


@app.route("/api/admin/knowledge", methods=["GET"])
def admin_knowledge():
    if not admin_required():
        return jsonify({"error": "Ruxsat yo‘q."}), 401

    connection = db()
    rows = connection.execute("SELECT * FROM knowledge ORDER BY id DESC").fetchall()
    connection.close()

    return jsonify([dict(row) for row in rows])


@app.route("/api/admin/knowledge", methods=["POST"])
def add_knowledge():
    if not admin_required():
        return jsonify({"error": "Ruxsat yo‘q."}), 401

    body = request.get_json(silent=True) or {}
    title = (body.get("title") or "").strip()
    content = (body.get("content") or "").strip()

    if not title or not content:
        return jsonify({"error": "Sarlavha va matn kerak."}), 400

    connection = db()
    connection.execute(
        "INSERT INTO knowledge (title, content, created_at) VALUES (?, ?, ?)",
        (title, content, datetime.utcnow().isoformat())
    )
    connection.commit()
    connection.close()

    return jsonify({"ok": True})


@app.route("/api/admin/knowledge/<int:item_id>", methods=["DELETE"])
def delete_knowledge(item_id):
    if not admin_required():
        return jsonify({"error": "Ruxsat yo‘q."}), 401

    connection = db()
    connection.execute("DELETE FROM knowledge WHERE id = ?", (item_id,))
    connection.commit()
    connection.close()

    return jsonify({"ok": True})


@app.route("/api/admin/chats", methods=["GET"])
def admin_chats():
    if not admin_required():
        return jsonify({"error": "Ruxsat yo‘q."}), 401

    connection = db()
    rows = connection.execute(
        "SELECT * FROM chats ORDER BY id DESC LIMIT 100"
    ).fetchall()
    connection.close()

    return jsonify([dict(row) for row in rows])


@app.route("/api/admin/backup", methods=["POST"])
def admin_backup():
    if not admin_required():
        return jsonify({"error": "Ruxsat yo‘q."}), 401

    path = create_backup()
    return jsonify({"ok": True, "backup": path})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
