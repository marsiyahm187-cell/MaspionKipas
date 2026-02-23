import os
import telebot
from openai import OpenAI

# Mengambil variabel dari Railway
BOT_TOKEN = os.environ.get('TELEGRAM_TOKEN')
OPENAI_KEY = os.environ.get('OPENAI_API_KEY')

# Inisialisasi Bot dan OpenAI
bot = telebot.TeleBot(BOT_TOKEN)
client = OpenAI(api_key=OPENAI_KEY)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Halo! Sekarang saya menggunakan otak ChatGPT. Silakan tanya apa saja!")

@bot.message_handler(func=lambda message: True)
def chat_with_gpt(message):
    try:
        # Menampilkan status 'typing'
        bot.send_chat_action(message.chat.id, 'typing')
        
        # Permintaan ke ChatGPT (Model gpt-3.5-turbo atau gpt-4o-mini)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message.text}]
        )
        
        # Mengambil teks jawaban
        answer = response.choices[0].message.content
        bot.reply_to(message, answer)
        
    except Exception as e:
        bot.reply_to(message, f"Ada kendala: {str(e)}")

if __name__ == "__main__":
    print("Bot ChatGPT menyala...")
    bot.infinity_polling(skip_pending=True)
