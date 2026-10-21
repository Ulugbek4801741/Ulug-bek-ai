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
