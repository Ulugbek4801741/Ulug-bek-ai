import os
import hashlib
import inspect

class UlugbekAICore:
    def __init__(self):
        self.admin_password_hash = hashlib.sha256('A4801741_a'.encode()).hexdigest()
        self.is_admin_logged = False
        self.version = "1.0.0"
        self.learned_knowledge_base = []

    def verify_admin_access(self, password_input):
        """Yashirin admin panelga kirish: Parol kiritilganda * ko'rinadi va tekshiriladi"""
        masked_input = "*" * len(password_input)
        input_hash = hashlib.sha256(password_input.encode()).hexdigest()
        
        if input_hash == self.admin_password_hash:
            self.is_admin_logged = True
            print(f"[ADMIN ACCESS GRANTED] Parol tasdiqlandi: {masked_input}")
            return True
        else:
            print(f"[ACCESS DENIED] Noto'g'ri parol: {masked_input}")
            return False

    def self_read_code(self):
        """O'zining kodini o'zi o'qib tahlil qilish moduli"""
        current_file_path = inspect.getfile(inspect.currentframe())
        with open(current_file_path, 'r', encoding='utf-8') as f:
            code_content = f.read()
        return code_content

    def autonomous_learn_and_upgrade(self, external_ai_insights):
        """
        ChatGPT, Gemini, Claude, DeepSeek kabi yetakchi modellardan internet orqali 
        ma'lumot olib, o'zini o'zi o'qitish va yangi funksiyalar qo'shish jarayoni.
        """
        if not self.is_admin_logged:
            return "Xatolik: Faqat admin ruxsati bilan o'zini o'zi yangilash mumkin!"

        print("[AI CORE] Internet orqali yirik modellardan (Gemini, GPT, Claude, DeepSeek) yangi funksiyalar o'rganilmoqda...")
        
        # Yangi bilim va funksiyalarni o'zlashtirish
        self.learned_knowledge_base.append(external_ai_insights)
        
        # O'z kodiga yangi imkoniyatni avtomatik qo'shish simulyatsiyasi
        new_feature_code = f"\n    # Auto-learned feature from insights: {external_ai_insights[:30]}...\n"
        
        current_code = self.self_read_code()
        updated_code = current_code + new_feature_code
        
        current_file_path = inspect.getfile(inspect.currentframe())
        with open(current_file_path, 'w', encoding='utf-8') as f:
            f.write(updated_code)
            
        return f"Ulug'bek AI Core muvaffaqiyatli yangilandi! Yangi bilim qo'shildi."

if __name__ == "__main__":
    ai_core = UlugbekAICore()
    print("Ulug'bek AI Core ishga tushdi. Himoyalangan va o'zini o'zi o'qituvchi tizim faol.")
        
