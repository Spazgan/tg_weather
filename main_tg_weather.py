import requests
import datetime
from config import tg_token, open_weather_token
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
import asyncio

# Создаем бота
bot = Bot(token=tg_token)
dp = Dispatcher()

# Обработчик команды /start
@dp.message(Command("start"))
async def start_command(message: Message):
    await message.reply("Привет! Напиши мне название города, и я пришлю тебе сводку погоды!")

# Обработчик для получения погоды
@dp.message()
async def get_weather(message: Message):
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }
    try:
        # Логирование для отслеживания выполнения кода
        print(f"Запрос погоды для города: {message.text}")

        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        # Проверка на успешный ответ
        if data.get("cod") != 200:
            await message.reply("\U00002620 Не удалось найти город. Проверьте название. \U00002620")
            return

        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        wd = code_to_smile.get(weather_description, "Посмотри в окно, не пойму что там за погода")

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset_timestamp = datetime.datetime.fromtimestamp(data['sys']['sunset'])
        length_of_the_day = sunset_timestamp - sunrise_timestamp

        # Логирование перед отправкой данных
        print(f"Отправка данных пользователю: {city}, {cur_weather}, {wd}")

        # Отправка ответа пользователю
        await message.reply(f"\n***{datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}***"
        # await message.reply(
            f"\nПогода в городе: {city}\nТемпература: {cur_weather}°C {wd}\n"
            f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст.\nСкорость ветра: {wind} м/с\n"
            f"Рассвет: {sunrise_timestamp}\nЗакат: {sunset_timestamp}\nСветовой день: {length_of_the_day}\nХорошего дня!"
        )
    except Exception as ex:
        await message.reply(f"Ошибка: {ex}")
        await message.reply("\U00002620 Проверьте название города \U00002620")


# Запуск бота
async def main():
    print("Бот запущен")  # Логирование запуска бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
