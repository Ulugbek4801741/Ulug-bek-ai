import os
import json
import requests
from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder=".", static_url_path="")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"


@app.route("/")
def home():
    return send_from_directory(".", "index.html")


@app.route("/api/config")
def config():
    return jsonify({"googleClientId": GOOGLE_CLIENT_ID or ""})


def ask_gemini(prompt, system_instruction):
    if not GEMINI_API_KEY:
        return None, "GEMINI_API_KEY sozlanmagan. Replit Secrets yoki .env fayliga qo‘shing."

    payload = {
        "system_instruction": {
            "parts": [{"text": system_instruction}]
        },
        "contents": [
            {"role": "user", "parts": [{"text": prompt}]}
        ],
        "tools": [{"google_search": {}}]
    }

    response = requests.post(
        f"{GEMINI_URL}?key={GEMINI_API_KEY}",
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload),
        timeout=60
    )

    if response.status_code != 200:
        return None, f"Gemini xatosi: {response.status_code} - {response.text[:300]}"

    data = response.json()

    try:
        text = data["candidates"][0]["content"]["parts"][0]["text"]
        return text, None
    except (KeyError, IndexError):
        return None, "Gemini javob formati noto‘g‘ri keldi."


@app.route("/api/chat", methods=["POST"])
def chat():
    body = request.get_json(silent=True) or {}
    prompt = (body.get("prompt") or "").strip()

    if not prompt:
        return jsonify({"error": "Savol bo‘sh bo‘lishi mumkin emas."}), 400

    system = (
        "Sen Ulug'bek AI nomli yordamchisan. "
        "Foydalanuvchiga o‘zbek tilida, aniq, foydali va qisqa javob ber. "
        "Zamonaviy yoki aniq ma’lumot kerak bo‘lsa, Google Search vositasidan foydalanib, "
        "internetdan tekshirilgan ma’lumot asosida javob ber."
    )

    answer, error = ask_gemini(prompt, system)

    if error:
        return jsonify({"error": error}), 500

    return jsonify({"reply": answer})


@app.route("/api/generate-app", methods=["POST"])
def generate_app():
    body = request.get_json(silent=True) or {}
    prompt = (body.get("prompt") or "").strip()

    if not prompt:
        return jsonify({"error": "Ilova g‘oyasi bo‘sh bo‘lishi mumkin emas."}), 400

    system = (
        "Sen tajribali frontend dasturchisan. "
        "Foydalanuvchi bergan g‘oya asosida bitta to‘liq ishlaydigan HTML fayl yoz. "
        "Faqat HTML kodini qaytar. Izoh, markdown yoki tushuntirish yozma. "
        "HTML fayl mobil telefonda ham chiroyli ko‘rinsin, o‘zbek tilida bo‘lsin "
        "va tashqi kutubxonalarni CDN orqali ishlatsin."
    )

    code, error = ask_gemini(prompt, system)

    if error:
        return jsonify({"error": error}), 500

    code = code.strip()

    if code.startswith("```"):
        code = code.split("\n", 1)[1] if "\n" in code else code
        if code.endswith("```"):
            code = code[:-3]

    return jsonify({"code": code.strip()})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
