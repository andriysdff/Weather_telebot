import requests
import datetime
from pprint import pprint
from config import open_weather_token, bot_token_key
#from config import bot_token_key
import telebot

bot = telebot.TeleBot(bot_token_key)


def get_weather(city):
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Хмарно \U00002601",
        "Rain": "Дощ \U00002614",
        "Drizzle": "Дощить \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Сніг \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric"
        )
        data = r.json()
        pprint(data)

        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Подивись в вікно, не розумію що там за погода!"

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])
        
        message = (f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                   f"Погода в місті: {city}\nТемпература: {cur_weather}C° {wd}\n"
                   f"Волога: {humidity}%\nТиск: {pressure} мм.рт.ст\nВітер: {wind} м/с\n"
                   f"Схід сонця: {sunrise_timestamp}\nЗахід сонця: {sunset_timestamp}\nТривалість дня: {length_of_the_day}\n"
                   f"Гарного дня!"
                   )
        return message

    except Exception as ex:
        return "Перевірте назву міста"


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привіт, введіть назву міста, щоб дізнатися погоду!")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    city = message.text
    weather_message = get_weather(city)
    bot.reply_to(message, weather_message)


bot.polling()
