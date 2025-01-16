import requests
import logging
import datetime
from DB import get_user_by_username, get_session, add_user
from config import tg_token, open_weather_token
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
import asyncio
import json

# Настройка логирования
logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")

# Создаем бота
bot = Bot(token=tg_token)
dp = Dispatcher()

# Функция для получения погоды
async def get_weather_data(city_name: str):
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
        logging.info(f"Запрос погоды для города: {city_name}")

        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        if data.get("cod") != 200:
            return None

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

        weather_data = {
            "city": city,
            "cur_weather": cur_weather,
            "wd": wd, 
            "humidity": humidity,
            "pressure": pressure,
            "wind": wind,
            "sunrise_timestamp": sunrise_timestamp,
            "sunset_timestamp": sunset_timestamp,
            "length_of_the_day": length_of_the_day
        }
        return weather_data
    except Exception as ex:
        logging.info(f"Ошибка при получении данных: {ex}")

# Функция для отправки ответа с погодой пользователю
async def send_weather_response(message: Message, weather_data):
    if weather_data:
        logging.info(f"Отправка данных пользователю: {weather_data['city']}, {weather_data['cur_weather']}, {weather_data['wd']}")
        await message.reply(f"\n***{datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}***"
            f"\nПогода в городе: {weather_data['city']}\nТемпература: {weather_data['cur_weather']}°C {weather_data['wd']}\n"
            f"Влажность: {weather_data['humidity']}%\nДавление: {weather_data['pressure']} мм.рт.ст.\nСкорость ветра: {weather_data['wind']} м/с\n"
            f"Рассвет: {weather_data['sunrise_timestamp']}\nЗакат: {weather_data['sunset_timestamp']}\nСветовой день: {weather_data['length_of_the_day']}\nХорошего дня!"
        )
    else:
        await message.reply("\U00002620 Не удалось найти город. Проверьте название. \U00002620")

# Обработчик команды /start
@dp.message(Command("start"))
async def start_command(message: Message):
    await message.reply("Привет! Напиши мне название города, и я пришлю тебе сводку погоды!")

# Обработчик команды /reg
@dp.message(Command("reg"))
async def registration(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username
    city = message.text.split(" ", 1)[1] if len(message.text.split(" ", 1)) > 1 else None  # Получаем город из сообщения

    # Проверка, зарегистрирован ли уже пользователь
    existing_user = await get_user_by_username(username)
    if existing_user:
        # Если пользователь существует, обновляем его город
        existing_user.city = city
        async for session in get_session():
            session.add(existing_user)
            await session.commit()
        await message.reply(f"Вы уже зарегистрированы. Ваш город был обновлён на {city}.")
    else:
        # Если пользователя нет, регистрируем нового
        await add_user(user_id=user_id, username=username, first_name=message.from_user.first_name, last_name=message.from_user.last_name)
        # После регистрации пользователя, обновляем его город
        new_user = await get_user_by_username(username)
        new_user.city = city
        async for session in get_session():
            session.add(new_user)
            await session.commit()
        await message.reply(f"Вы успешно зарегистрированы, ваш город: {city}!")

# Обработчик для получения погоды
@dp.message()
async def get_weather(message: Message):
    city_name = message.text
    weather_data = await get_weather_data(city_name)
    await send_weather_response(message, weather_data)

# Запуск бота
async def main():
    logging.info("Бот запущен")  # Логирование запуска бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
