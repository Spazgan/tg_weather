import logging
import asyncio
from aiogram import Bot, Dispatcher
from controller import main
from config import tg_token

# Настройка логирования
logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w", format="%(asctime)s %(levelname)s %(message)s")

# Замените на свой токен
bot = Bot(token=tg_token)  
dp = Dispatcher()

# Запуск бота
if __name__ == "__main__":
    asyncio.run(main())
