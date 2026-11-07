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

# Словарь для хранения связки: ID сообщения у владельца -> ID пользователя, отправившего анонимку
message_map = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет, здесь можешь написать для моего господина Тимурчика, что ты хотел(а) бы написать ему?")

@bot.message_handler(content_types=['text'])
def handle_message(message):
    if message.chat.id == OWNER_ID:
        # Если пишет сам владелец (Тимур)
        if message.reply_to_message:
            # Если это ответ на пересланное сообщение
            replied_msg_id = message.reply_to_message.message_id
            
            # Ищем, кто отправлял это сообщение
            if replied_msg_id in message_map:
                user_id = message_map[replied_msg_id]
                try:
                    # Отправляем ответ пользователю
                    bot.send_message(user_id, f"Ответ от Тимура:\n\n{message.text}")
                    bot.send_message(OWNER_ID, "Ответ успешно отправлен!")
                except Exception as e:
                    bot.send_message(OWNER_ID, "Не удалось отправить ответ. Возможно, пользователь заблокировал бота.")
            else:
                bot.send_message(OWNER_ID, "Не могу найти, кому отвечать. Возможно, сообщение слишком старое или бот перезагружался.")
        else:
            bot.send_message(message.chat.id, "Чтобы ответить анонимщику, зажми на его сообщение и выбери «Ответить» (Reply).")
        return

    # Если пишет обычный пользователь (анонимщик)
    bot.send_message(message.chat.id, "Сообщение отправлено, Тимур ответит вам сегодня (наверное)")
    bot.send_message(OWNER_ID, "ПРИКИНЬ, ТЕБЕ НАПИСАЛИ, СРОЧНО ЗАХОДИ")
    
    hidden_text = f"<tg-spoiler>{message.text}</tg-spoiler>"
    
    # Отправляем тебе сообщение и сохраняем его ID
    sent_msg = bot.send_message(OWNER_ID, hidden_text, parse_mode='HTML')
    
    # Запоминаем: это сообщение (sent_msg.message_id) пришло от пользователя (message.chat.id)
    message_map[sent_msg.message_id] = message.chat.id

if __name__ == "__main__":
    keep_alive()
    print("Бот запущен!")
    bot.polling(none_stop=True)
