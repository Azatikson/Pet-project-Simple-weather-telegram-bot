import telebot
from telebot import types   
import requests

BOT_TOKEN = # свой токен
bot = telebot.TeleBot(BOT_TOKEN)

def get_weather(city: str) -> str:
    url = f"https://wttr.in/{city}?format=3&lang=ru"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.text.strip()
    except requests.exceptions.RequestException as e:
        return f"⚠️ Не удалось получить погоду: {e}"

def main_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_moscow = types.KeyboardButton("Москва")
    btn_spb = types.KeyboardButton("Санкт-Петербург")
    btn_help = types.KeyboardButton("Помощь")
    btn_other = types.KeyboardButton("Другой город")
    keyboard.add(btn_moscow, btn_spb, btn_help, btn_other)
    return keyboard

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "Привет! 👋\nВыбери город из кнопок или напиши название своего.",
        reply_markup=main_menu()
    )

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text.strip()

    if text == "Помощь":
        bot.send_message(
            message.chat.id,
            "Я умею показывать текущую погоду.\n"
            "Просто напиши название города или выбери одну из кнопок.",
            reply_markup=main_menu()
        )
    elif text == "Другой город":
        bot.send_message(
            message.chat.id,
            "Введи название города вручную.",
            reply_markup=main_menu()
        )
    else:
        bot.send_chat_action(message.chat.id, 'typing')
        weather = get_weather(text)
        bot.send_message(message.chat.id, weather, reply_markup=main_menu())

if __name__ == "__main__":
    print("✅ Бот запущен. Нажмите Ctrl+C для остановки.")
    bot.infinity_polling()


    


