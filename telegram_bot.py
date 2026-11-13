import hmac
import os
import sqlite3
from datetime import datetime, timezone

import requests
from flask import Blueprint, jsonify, request

telegram_bp = Blueprint("telegram_bot", __name__)
DB_PATH = os.getenv("DB_PATH", "ulugbek_ai.db")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
WEBHOOK_SECRET = os.getenv("TELEGRAM_WEBHOOK_SECRET", "")
ADMIN_CHAT_ID = os.getenv("TELEGRAM_ADMIN_CHAT_ID", "")
API_BASE = "https://api.telegram.org/bot"


def _db():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_telegram_db():
    connection = _db()
    connection.executescript("""
        CREATE TABLE IF NOT EXISTS telegram_sessions (
            chat_id INTEGER PRIMARY KEY,
            mode TEXT NOT NULL DEFAULT 'menu',
            updated_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS telegram_orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_user_id INTEGER NOT NULL,
            chat_id INTEGER NOT NULL,
            username TEXT,
            service TEXT NOT NULL,
            details TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'new',
            created_at TEXT NOT NULL
        );
    """)
    connection.commit()
    connection.close()


def _telegram(method, payload):
    if not BOT_TOKEN:
        return None
    try:
        response = requests.post(
            f"{API_BASE}{BOT_TOKEN}/{method}",
            json=payload,
            timeout=15,
        )
        response.raise_for_status()
        data = response.json()
        return data if data.get("ok") else None
    except (requests.RequestException, ValueError):
        return None


def _send(chat_id, text, keyboard=None):
    payload = {
        "chat_id": chat_id,
        "text": text[:4000],
        "disable_web_page_preview": True,
    }
    if keyboard:
        payload["reply_markup"] = {"inline_keyboard": keyboard}
    return _telegram("sendMessage", payload)


def _menu(chat_id):
    keyboard = [
        [{"text": "🤖 AI konsultant", "callback_data": "mode:chat"},
         {"text": "🛒 Buyurtma berish", "callback_data": "mode:order"}],
        [{"text": "📦 Xizmatlar katalogi", "callback_data": "catalog"},
         {"text": "💼 Tayyor mahsulotlar", "callback_data": "products"}],
        [{"text": "👨‍💼 Administrator", "callback_data": "support"}],
    ]
    _send(
        chat_id,
        "Assalomu alaykum! ULUGBEK AI platformasiga xush kelibsiz.\n"
        "Sayt, mobil ilova, Telegram bot, internet-do‘kon, AI agent yoki "
        "boshqa raqamli mahsulot uchun buyurtma berishingiz mumkin.",
        keyboard,
    )


def _set_mode(chat_id, mode):
    connection = _db()
    connection.execute(
        """INSERT INTO telegram_sessions(chat_id, mode, updated_at)
           VALUES (?, ?, ?)
           ON CONFLICT(chat_id) DO UPDATE SET
             mode=excluded.mode, updated_at=excluded.updated_at""",
        (chat_id, mode, datetime.now(timezone.utc).isoformat()),
    )
    connection.commit()
    connection.close()


def _get_mode(chat_id):
    connection = _db()
    row = connection.execute(
        "SELECT mode FROM telegram_sessions WHERE chat_id=?", (chat_id,)
    ).fetchone()
    connection.close()
    return row["mode"] if row else "menu"


def _save_order(message, details, ai_handler):
    user = message.get("from", {})
    chat_id = message["chat"]["id"]
    service = "Raqamli mahsulot bo‘yicha buyurtma"
    connection = _db()
    cursor = connection.execute(
        """INSERT INTO telegram_orders
           (telegram_user_id, chat_id, username, service, details, created_at)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (
            user.get("id", 0),
            chat_id,
            user.get("username", ""),
            service,
            details[:8000],
            datetime.now(timezone.utc).isoformat(),
        ),
    )
    order_id = cursor.lastrowid
    connection.commit()
    connection.close()

    _set_mode(chat_id, "menu")
    _send(
        chat_id,
        f"✅ Buyurtmangiz qabul qilindi. Raqami: #{order_id}.\n"
        "Administrator talablaringizni ko‘rib chiqib, narx va muddatni "
        "tasdiqlaydi. Tasdiqlanmagan narx yoki muddat va’da qilinmaydi.",
    )

    if ADMIN_CHAT_ID:
        _send(
            ADMIN_CHAT_ID,
            f"🆕 Yangi buyurtma #{order_id}\n"
            f"Mijoz: @{user.get('username') or 'username yo‘q'} "
            f"(ID: {user.get('id', 'noma’lum')})\n"
            f"Talab: {details[:3000]}",
        )


@telegram_bp.post("/telegram/webhook")
def telegram_webhook():
    if not BOT_TOKEN:
        return jsonify({"error": "Telegram bot sozlanmagan."}), 503

    supplied_secret = request.headers.get(
        "X-Telegram-Bot-Api-Secret-Token", ""
    )
    if WEBHOOK_SECRET and not hmac.compare_digest(
        supplied_secret, WEBHOOK_SECRET
    ):
        return jsonify({"error": "Unauthorized"}), 401

    update = request.get_json(silent=True) or {}
    callback = update.get("callback_query")

    if callback:
        data = callback.get("data", "")
        message = callback.get("message") or {}
        chat_id = (message.get("chat") or {}).get("id")
        callback_id = callback.get("id")
        if callback_id:
            _telegram("answerCallbackQuery", {"callback_query_id": callback_id})
        if not chat_id:
            return jsonify({"ok": True})

        if data == "mode:chat":
            _set_mode(chat_id, "chat")
            _send(chat_id, "Savolingizni yozing. AI konsultant javob beradi. Menyuga qaytish: /start")
        elif data == "mode:order":
            _set_mode(chat_id, "order")
            _send(chat_id, "Qanday mahsulot kerakligini batafsil yozing: sayt, Android/iOS ilova, bot, do‘kon, AI agent yoki boshqa loyiha. Byudjet va kerakli muddatni ham yozishingiz mumkin.")
        elif data == "catalog":
            _send(chat_id, "Xizmatlarimiz: veb-saytlar, internet-do‘konlar, mobil ilovalar, Telegram botlar, AI agentlar, avtomatlashtirish, dizayn va biznes tizimlari.")
        elif data == "products":
            _send(chat_id, "Tayyor mahsulotlar katalogi hozir shakllantirilmoqda. Mavjud mahsulotlar va narxlar administrator tasdiqlagach shu yerda ko‘rsatiladi.")
        elif data == "support":
            _send(chat_id, "Administratorga murojaat qilish uchun buyurtma tavsifini yuboring yoki /start orqali buyurtma bo‘limini tanlang.")
        return jsonify({"ok": True})

    message = update.get("message") or update.get("edited_message")
    if not message or not message.get("chat"):
        return jsonify({"ok": True})

    chat_id = message["chat"]["id"]
    text = (message.get("text") or "").strip()
    if not text:
        _send(chat_id, "Hozircha matnli xabar yuboring. /start")
        return jsonify({"ok": True})

    if text in ("/start", "/menu"):
        _set_mode(chat_id, "menu")
        _menu(chat_id)
    elif text == "/help":
        _send(chat_id, "Buyurtma berish, AI konsultant va xizmatlar katalogi uchun /start buyrug‘ini yuboring.")
    elif _get_mode(chat_id) == "order":
        _save_order(message, text, None)
    elif _get_mode(chat_id) == "chat":
        ai_handler = telegram_webhook.ai_handler
        answer, provider = ai_handler(
            text,
            "Sen ULUGBEK AI savdo konsultantisan. O‘zbek tilida javob ber. "
            "Mijoz ehtiyojini aniqlashtir, xizmatlarni tushuntir. "
            "Tasdiqlanmagan narx, chegirma, muddat yoki to‘lov qabul qilinganini "
            "uydirma. Buyurtma berish uchun /start ni taklif qil."
        )
        _send(chat_id, answer or "AI hozir javob bera olmadi. Keyinroq urinib ko‘ring.")
    else:
        _menu(chat_id)

    return jsonify({"ok": True})


def create_telegram_blueprint(ai_handler):
    telegram_webhook.ai_handler = ai_handler
    init_telegram_db()
    return telegram_bp
