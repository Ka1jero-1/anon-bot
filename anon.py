import telebot
import os
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Бот работает!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

TOKEN = '9181002407:AAE5jWHSYXsMPokM5_S79oSJl0L2DOmoS4'
OWNER_ID = 5419168665
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет, здесь можешь написать для моего господина Тимурчика, что ты хотел(а) бы написать ему?")

@bot.message_handler(content_types=['text'])
def handle_message(message):
    if message.chat.id == OWNER_ID:
        bot.send_message(message.chat.id, "Ты сам себе пишешь, господин.")
        return
    bot.send_message(message.chat.id, "Сообщение отправлено, Тимур ответит вам сегодня (наверное)")
    bot.send_message(OWNER_ID, "ПРИКИНЬ, ТЕБЕ НАПИСАЛИ, СРОЧНО ЗАХОДИ")
    hidden_text = f"<tg-spoiler>{message.text}</tg-spoiler>"
    bot.send_message(OWNER_ID, hidden_text, parse_mode='HTML')

if __name__ == "__main__":
    keep_alive()
    print("Бот запущен!")
    bot.polling(none_stop=True)
