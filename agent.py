import os
import json

class UlugbekAIAgent:
    def __init__(self, agent_name="Ulugbek AI Assistant"):
        self.agent_name = agent_name
        self.mode = "chat" # 'chat' yoki 'voice'

    def process_text_input(self, text_message):
        """Chat agent: Matnli buyruqlarni tahlil qiladi va javob qaytaradi"""
        print(f"[{self.agent_name} - Chat] Kiruvchi matn: {text_message}")
        
        # Bu yerda AI model (DeepSeek/Ollama) buyruqni qayta ishlaydi
        response = {
            "status": "success",
            "type": "text",
            "response": f"Buyruq qabul qilindi: {text_message}. APK va kod sozlamalari tayyorlanmoqda."
        }
        return response

    def process_voice_input(self, voice_audio_data):
        """Ovozli agent: Ovozni matnga o'giradi (STT) va javobni ovozda beradi (TTS)"""
        print(f"[{self.agent_name} - Ovoz] Ovozli xabar qabul qilindi...")
        
        # 1. Speech-to-Text (Ovozni matnga o'girish)
        converted_text = "Ovozli buyruq matnga o'girildi" 
        
        # 2. Text-to-Speech (Javobni ovozga o'girish)
        return {
            "status": "success",
            "type": "voice",
            "text_response": converted_text,
            "audio_output": "audio_response.mp3"
        }

if __name__ == "__main__":
    agent = UlugbekAIAgent()
    print("Ulug'bek AI Chat va Ovozli agent ishga tushdi!")
  
