from flask import Flask, request
import telebot
import os

# --- TOKEN ---
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("❌ BOT_TOKEN not set")

bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

# --- FORCE HTTPS FIX (Render proxy issue) ---
@app.before_request
def force_https():
    if request.headers.get('X-Forwarded-Proto') == 'http':
        return '', 200

# --- START COMMAND ---
@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(
        telebot.types.InlineKeyboardButton("📚 Courses", callback_data="courses"),
        telebot.types.InlineKeyboardButton("💰 Pricing", callback_data="pricing"),
    )

    bot.send_message(message.chat.id, "🔥 Welcome to KAC Bot!", reply_markup=markup)

# --- BUTTON HANDLER ---
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "courses":
        bot.send_message(call.message.chat.id, "📚 Python / Web / AI")
    elif call.data == "pricing":
        bot.send_message(call.message.chat.id, "💰 $10 - $20")

# --- WEBHOOK (IMPORTANT FIX INCLUDED) ---
@app.route(f"/{TOKEN}", methods=['POST'])
@app.route(f"/{TOKEN}/", methods=['POST'])
def webhook():
    try:
        print("🔥 WEBHOOK HIT")

        json_str = request.get_data().decode('utf-8')
        print(json_str)

        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])

        return "ok", 200
    except Exception as e:
        print("❌ ERROR:", e)
        return "error", 200

# --- HOME ---
@app.route("/")
def home():
    return "KAC Bot Running on Render 🚀"