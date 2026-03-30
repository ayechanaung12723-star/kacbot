from flask import Flask, request
import telebot
import os

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

# --- START ---
@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(
        telebot.types.InlineKeyboardButton("📚 Courses", callback_data="courses"),
        telebot.types.InlineKeyboardButton("💰 Pricing", callback_data="pricing"),
    )

    bot.send_message(message.chat.id, "🔥 Welcome to KAC Bot!", reply_markup=markup)

# --- BUTTON ---
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "courses":
        bot.send_message(call.message.chat.id, "📚 Python / Web / AI")
    elif call.data == "pricing":
        bot.send_message(call.message.chat.id, "💰 $10 - $20")

# --- WEBHOOK ---
@app.route(f"/{TOKEN}", methods=['POST'])
def webhook():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "ok", 200

@app.route("/")
def home():
    return "KAC Bot Running on Render 🚀"