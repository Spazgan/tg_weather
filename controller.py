from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from data import get_user, add_or_update_user
from view import send_weather_response, send_registration_response
from weather import get_weather_data
from config import tg_token

bot = Bot(token=tg_token)  # Замените на свой токен
dp = Dispatcher()

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
    username = message.from_user.username or str(message.from_user.id)

    add_or_update_user(username, city)
    await send_registration_response(message, city)

# Обработчик запроса погоды
@dp.message()
async def get_weather(message: Message):
    city_name = message.text.strip()
    username = message.from_user.username or str(message.from_user.id)

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
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
