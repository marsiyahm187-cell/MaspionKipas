import os
import telebot
import google.generativeai as genai

# Mengambil variabel dari Railway
BOT_TOKEN = os.environ.get('TELEGRAM_TOKEN')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

bot = telebot.TeleBot(BOT_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)

# PERBAIKAN: Gunakan 'gemini-1.5-flash' (Jauh lebih cepat & responsif)
model = genai.GenerativeModel('gemini-1.5-flash')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Halo! Saya sudah diperbaiki dan sekarang lebih cepat. Ada yang bisa dibantu?")

@bot.message_handler(func=lambda message: True)
def chat_with_ai(message):
    try:
        # Menampilkan status 'sedang mengetik'
        bot.send_chat_action(message.chat.id, 'typing')
        
        # Mengirim pesan ke AI
        response = model.generate_content(message.text)
        
        # Mengirim jawaban kembali ke user
        bot.reply_to(message, response.text)
    except Exception as e:
        # Menampilkan pesan error jika terjadi masalah
        bot.reply_to(message, f"Aduh, ada error sedikit nih: {str(e)}")

# Menjalankan bot
if __name__ == "__main__":
    print("Bot sedang berjalan...")
    bot.infinity_polling()
