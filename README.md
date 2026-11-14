# Ulug'bek AI

Google akkaunt bilan kiriladigan, ovozli AI agent, internet qidiruvi, No-Code mahsulot studiyasi, avtomatik AI provayder fallback va ma’lumot zaxirasi tizimiga ega platforma.

## Ishga tushirish

```bash
pip install -r requirements.txt
python agent.py
```

Brauzerda:

```text
http://127.0.0.1:5000
```

## Admin panel

```text
/a7x9q
```

Parol `.env` faylidagi `ADMIN_PASSWORD` orqali boshqariladi.

## AI fallback tizimi

AI javob berish tartibi:

1. Asosiy Gemini kaliti
2. Zaxira Gemini kaliti
3. OpenAI kaliti

Biror provayder ishlamasa, tizim keyingisiga avtomatik o‘tadi.

## Ma’lumot zaxirasi

Admin panelda **Zaxira olish** tugmasi bosilganda foydalanuvchilar, suhbatlar va bilimlar JSON faylga saqlanadi.

Terminal orqali tiklash:

```bash
python restore.py backups/backup_fayli.json
```

## Server holati

```text
/health
```

## Sozlash

```env
GEMINI_API_KEY=...
GEMINI_API_KEY_2=...
OPENAI_API_KEY=...
GOOGLE_CLIENT_ID=...
ADMIN_PASSWORD=A4801741_a
SECRET_KEY=...
```

## Imkoniyatlar

- Google bilan kirish
- Professional animatsion avatar
- Ovozli savol va ovozli javob
- Ovozli buyruqlar
- Internet ma’lumotlari bilan javob berish
- Foydalanuvchi baholari asosida javob sifatini yaxshilash
- Admin orqali bilim va qoidalar qo‘shish
- AI provayder fallback
- Ma’lumot zaxirasi va tiklash
- No-Code HTML ilova generatori


## Telegram savdo boti

Telegram moduli mavjud Flask/AI platformasiga qo‘shilgan. U alohida webhook orqali ishlaydi:

- `POST /telegram/webhook` — Telegram yangilanishlarini qabul qiladi.
- `/start` — asosiy menyu.
- AI konsultant — mavjud `ask_ai` provayder zanjiridan foydalanadi.
- Buyurtma — SQLite bazasiga yoziladi va sozlangan administrator chatiga xabar yuboradi.
- Katalog — xizmatlar va tayyor mahsulotlar bo‘limlari.

### Render sozlamalari

Render Environment Variables bo‘limiga quyidagilarni kiriting:

- `TELEGRAM_BOT_TOKEN` — BotFather bergan yangi token.
- `TELEGRAM_WEBHOOK_SECRET` — tasodifiy, uzun va maxfiy webhook kaliti.
- `TELEGRAM_ADMIN_CHAT_ID` — buyurtmalar yuboriladigan administrator Telegram chat ID.

Tokenni GitHub'ga, kodga yoki chatga joylamang. Oldin oshkor qilingan tokenni BotFather orqali bekor qiling.

### Webhookni ulash

Render deploy muvaffaqiyatli bo‘lgach, xavfsiz terminalda quyidagini bajaring (qiymatlarni o‘zingizning maxfiy muhit o‘zgaruvchilaringizdan oling):

```bash
curl -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/setWebhook" \
  -d "url=https://YOUR-RENDER-SERVICE.onrender.com/telegram/webhook" \
  -d "secret_token=${TELEGRAM_WEBHOOK_SECRET}"
```

Webhook so‘rovlari `X-Telegram-Bot-Api-Secret-Token` sarlavhasi bilan tekshiriladi.

### Hozirgi bosqich chegarasi

Bu birinchi integratsiya bosqichi: buyurtma yig‘ish, AI konsultant va administratorga xabar berish. Haqiqiy to‘lov provayderi, avtomatik narxlash, mahsulotlarni GitHub'da yaratish va mijozga APK/ZIP yetkazish alohida modullar va testlardan keyin ulanadi. Bot to‘lovni qabul qildim yoki loyiha tayyor deb yolg‘on tasdiqlamaydi.
