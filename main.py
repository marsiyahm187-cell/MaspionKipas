import os
import telebot
import google.generativeai as genai

# Pastikan nama variabel sesuai dengan di Railway
BOT_TOKEN = os.environ.get('TELEGRAM_TOKEN')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

bot = telebot.TeleBot(BOT_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)

# PERBAIKAN: Gunakan 'gemini-1.5-flash' yang lebih cepat dan stabil
model = genai.GenerativeModel('gemini-1.5-flash')

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Halo! Saya sudah diperbaiki. Silakan tanya apa saja!")

@bot.message_handler(func=lambda message: True)
def chat_with_ai(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        
        # Menggunakan model terbaru
        response = model.generate_content(message.text)
        
        bot.reply_to(message, response.text)
    except Exception as e:
        # Memberikan detail error jika terjadi masalah lagi
        bot.reply_to(message, f"Terjadi kesalahan teknis: {str(e)}")

bot.infinity_polling()
