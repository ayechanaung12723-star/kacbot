from flask import Flask, request
import telebot
import os

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🔥 Bot Working!")

@app.route(f"/{TOKEN}", methods=['POST'])
def webhook():
    print("WEBHOOK HIT")

    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])

    return "ok", 200

@app.route("/")
def home():
    return "Bot Alive"