import os
import google.generativeai as genai

# Gemini API kalitini GitHub Secrets'dan olish
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    print("Ulug'bek AI: Gemini API muvaffaqiyatli ulagandi!")
else:
    print("Ogohlantirish: GEMINI_API_KEY topilmadi!")

def ask_agent(prompt):
    """Ulug'bek AI agentining javob berish funksiyasi"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Xatolik yuz berdi: {str(e)}"

if __name__ == "__main__":
    print("Ulug'bek AI ishga tushmoqda...")
    test_response = ask_agent("Salom! Sen kimsan?")
    print("Agent javobi:", test_response)
        
