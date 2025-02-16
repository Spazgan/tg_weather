from aiogram import Bot, Dispatcher
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from services.user_service import UserService
from services.weather_service import WeatherService
from view import send_weather_response, send_registration_response
from config import tg_token
import logging

bot = Bot(token=tg_token)
dp = Dispatcher()

weather_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Получить погоду")]],
    resize_keyboard=True
)

user_service = UserService()
weather_service = WeatherService()

@dp.message(Command("start"))
async def start_command(message: Message):
    await message.reply(
        "Привет! Напиши мне название города, и я пришлю сводку погоды!\n"
        "Зарегистрируй город: /reg [город]",
        reply_markup=weather_keyboard
    )

@dp.message(Command("reg"))
async def registration(message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.reply("Укажите город: /reg Moscow")
        return

    username = message.from_user.username or str(message.from_user.id)
    try:
        user_service.update_user_city(username, args[1].strip())
        await send_registration_response(message, args[1].strip())
    except Exception as e:
        logging.error(f"Registration error: {e}")
        await message.reply("Ошибка регистрации")

@dp.message()
async def handle_message(message: Message):
    username = message.from_user.username or str(message.from_user.id)
    city = message.text.strip()
    
    if city == "Получить погоду":
        city = None

    weather_data, error = await weather_service.get_weather(username, city)
    
    if error:
        await message.reply(error)
    elif weather_data:
        await send_weather_response(message, weather_data)
    else:
        await message.reply("Город не найден")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())