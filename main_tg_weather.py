import requests
import logging
import datetime
import asyncio
from config import tg_token, open_weather_token
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, KeyboardButton, InlineKeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import Command
from DB import get_user, SessionLocal, User  

# Настройка логирования
logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")

# Создаем бота
bot = Bot(token=tg_token)
dp = Dispatcher()



# Функция для получения погоды
async def get_weather_data(city_name: str):
    code_to_smile = {
        "Clear": "Ясно ☀️",
        "Clouds": "Облачно ☁️",
        "Rain": "Дождь 🌧",
        "Drizzle": "Дождь 🌧",
        "Thunderstorm": "Гроза ⚡",
        "Snow": "Снег ❄️",
        "Mist": "Туман 🌫"
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
            "sunrise_timestamp": sunrise_timestamp.strftime('%H:%M'),
            "sunset_timestamp": sunset_timestamp.strftime('%H:%M'),
            "length_of_the_day": str(length_of_the_day)
        }
        return weather_data
    except Exception as ex:
        logging.error(f"Ошибка при получении данных: {ex}")
        return None

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
        await message.reply("⚠️ Не удалось найти город. Проверьте название. ⚠️")

# Обработчик команды /start
@dp.message(Command("start"))
async def start_command(message: Message):
    await message.reply("Привет! Напиши мне название города, и я пришлю тебе сводку погоды!\n"
                        "Чтобы зарегистрировать свой город, используй команду: /reg [город]")

# Обработчик команды /reg (регистрация города)
@dp.message(Command("reg"))
async def registration(message: Message):
    args = message.text.split(maxsplit=1)
    
    if len(args) < 2:
        await message.reply("Пожалуйста, укажите город после команды. Например: /reg Moscow.")
        return

    city = args[1].strip()
    username = message.from_user.username or str(message.from_user.id)  # Используем username, если есть, иначе id

    session = SessionLocal()
    user = session.query(User).filter_by(username=username).first()

    if user:
        user.city = city  # Обновляем город
    else:
        user = User(username=username, city=city)
        session.add(user)  # Добавляем нового пользователя

    session.commit()  # Сохраняем изменения
    session.close()

    await message.reply(f"Город {city} успешно зарегистрирован!")

# Обработчик запроса погоды
@dp.message()
async def get_weather(message: Message):
    city_name = message.text.strip()
    username = message.from_user.username or str(message.from_user.id)

    # Если пользователь не ввёл город, пытаемся взять его из базы
    if not city_name:
        user = get_user(username)
        if user and user.city:
            city_name = user.city
        else:
            await message.reply("Вы не зарегистрированы. Используйте /reg [город], чтобы сохранить свой город.")
            return

    weather_data = await get_weather_data(city_name)
    await send_weather_response(message, weather_data)

# Запуск бота
async def main():
    logging.info("Бот запущен")  # Логирование запуска бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
 