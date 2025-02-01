from aiogram import Bot, Dispatcher
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from data import get_user, add_or_update_user
from view import send_weather_response, send_registration_response
from weather import get_weather_data
from config import tg_token

bot = Bot(token=tg_token)  # Замените на свой токен
dp = Dispatcher()

# Создаем клавиатуру с кнопкой "Получить погоду"
weather_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Получить погоду")]
    ],
    resize_keyboard=True  # Клавиатура будет автоматически подстраиваться под размер экрана
)

# Обработчик команды /start
@dp.message(Command("start"))
async def start_command(message: Message):
    await message.reply(
        "Привет! Напиши мне название города, и я пришлю тебе сводку погоды!\n"
        "Чтобы зарегистрировать свой город, используй команду: /reg [город]",
        reply_markup=weather_keyboard  # Добавляем клавиатуру с кнопкой
    )

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

    # Если пользователь нажал на кнопку "Получить погоду"
    if city_name == "Получить погоду":
        user = get_user(username)
        if user and user.city:
            city_name = user.city
        else:
            await message.reply(
                "Вы не зарегистрированы. Используйте /reg [город], чтобы сохранить свой город.",
                reply_markup=weather_keyboard  # Кнопка остается всегда
            )
            return

    # Если пользователь ввел название города вручную
    if not city_name:
        await message.reply(
            "Пожалуйста, введите название города.",
            reply_markup=weather_keyboard  # Кнопка остается всегда
        )
        return

    weather_data = await get_weather_data(city_name)
    if weather_data:
        await send_weather_response(message, weather_data)
    else:
        await message.reply(
            "⚠️ Не удалось найти город. Проверьте название. ⚠️",
            reply_markup=weather_keyboard  # Кнопка остается всегда
        )

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())