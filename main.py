import os
import telebot
import google.generativeai as genai

# Mengambil API Key dari Environment Variables di Railway (demi keamanan)
BOT_TOKEN = os.environ.get('TELEGRAM_TOKEN')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

# Konfigurasi Bot dan AI
bot = telebot.TeleBot(BOT_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)

# Pengaturan Model AI (Gemini Pro)
model = genai.GenerativeModel('gemini-pro')

# Fungsi saat bot pertama kali dimulai (/start)
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Halo! Saya AI yang berjalan di Telegram. Silakan tanya apa saja, saya siap membantu.")

# Fungsi untuk merespons semua pesan teks
@bot.message_handler(func=lambda message: True)
def chat_with_ai(message):
    try:
        # Menampilkan status "typing" di Telegram agar terasa nyata
        bot.send_chat_action(message.chat.id, 'typing')
        
        # Mengirim pesan user ke Gemini
        response = model.generate_content(message.text)
        
        # Mengirim jawaban AI kembali ke user
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"Aduh, ada error sedikit nih: {str(e)}")

# Menjalankan bot terus menerus
print("Bot sedang berjalan...")
bot.infinity_polling()
