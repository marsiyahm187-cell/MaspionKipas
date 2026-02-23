import os
import telebot
from groq import Groq

# Ambil variabel dari Railway
BOT_TOKEN = os.environ.get('TELEGRAM_TOKEN')
GROQ_KEY = os.environ.get('GROQ_API_KEY')

# Inisialisasi Bot dan Groq
bot = telebot.TeleBot(BOT_TOKEN)
client = Groq(api_key=GROQ_KEY)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Halo! Saya bot AI yang didukung oleh Groq. Respon saya sangat cepat, silakan coba tanya apa saja!")

@bot.message_handler(func=lambda message: True)
def chat_with_groq(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        
        # Permintaan ke Groq (Menggunakan model Llama 3)
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": message.text}
            ],
        )
        
        answer = completion.choices[0].message.content
        bot.reply_to(message, answer)
        
    except Exception as e:
        bot.reply_to(message, f"Wah, ada kendala teknis: {str(e)}")

if __name__ == "__main__":
    print("Bot Groq menyala...")
    bot.infinity_polling(skip_pending=True)
