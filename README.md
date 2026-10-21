# Ulug'bek AI

Google akkaunt bilan kiriladigan, animatsion avatar, ovozli suhbat va No-Code ilova generatoriga ega AI platforma.

## Ishga tushirish

```bash
pip install -r requirements.txt
python agent.py
```

Brauzerda oching:

```text
http://127.0.0.1:5000
```

## Sozlash

`.env.example` faylini `.env` nomiga nusxalang va kalitlarni kiriting:

```env
GEMINI_API_KEY=...
GOOGLE_CLIENT_ID=...
```

Google Cloud Console’da OAuth Client yaratib, quyidagi redirect URI’ni qo‘shing:

```text
http://127.0.0.1:5000
```

## Imkoniyatlar

- Google bilan kirish
- Animatsion AI avatar
- Ovozli savol berish
- Ovozli javob
- Ovozli buyruqlar
- Internet ma’lumotlari bilan javob berish
- Prompt orqali HTML ilova yaratish va yuklab olish
