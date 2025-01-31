from aiogram.types import Message
import datetime

# Функция для отправки пользователю данных о погоде
async def send_weather_response(message: Message, weather_data):
    if weather_data:
        await message.reply(f"\n***{datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}***"
            f"\nПогода в городе: {weather_data['city']}\nТемпература: {weather_data['cur_weather']}°C {weather_data['wd']}\n"
            f"Влажность: {weather_data['humidity']}%\nДавление: {weather_data['pressure']} мм.рт.ст.\nСкорость ветра: {weather_data['wind']} м/с\n"
            f"Рассвет: {weather_data['sunrise_timestamp']}\nЗакат: {weather_data['sunset_timestamp']}\nСветовой день: {weather_data['length_of_the_day']}\nХорошего дня!"
        )
    else:
        await message.reply("⚠️ Не удалось найти город. Проверьте название. ⚠️")

# Функция для отправки ответа о регистрации города
async def send_registration_response(message: Message, city: str):
    await message.reply(f"Город {city} успешно зарегистрирован!")
