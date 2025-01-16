from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.future import select
from config import db_tok
import logging

# Настройка подключения
DATABASE_URL = "postgresql+asyncpg://postgres:12345@localhost/weather_bot"

# Создание асинхронного движка для PostgreSQL
engine = create_async_engine(DATABASE_URL, echo=True)

# Создание сессии
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

# Модель для таблицы пользователей
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    city = Column(String(50))

# Асинхронная функция для получения сессии
async def get_session():
    async with AsyncSessionLocal() as session:
        yield session

# Асинхронная функция для добавления пользователя
async def add_user(user_id, username, first_name, last_name):
    async for session in get_session():
        try:
            # Проверка, существует ли уже пользователь
            result = await session.execute(select(User).filter(User.username == username))
            existing_user = result.scalars().first()

            if existing_user:
                logging.info(f"Пользователь {username} уже зарегистрирован.")
                return  # Пользователь уже существует, ничего не делаем

            # Если не существует, добавляем нового пользователя
            new_user = User(id=user_id, username=username, first_name=first_name, last_name=last_name)
            session.add(new_user)
            await session.commit()  # Принудительный коммит
            logging.info(f"Пользователь {username} успешно добавлен.")
        except Exception as ex:
            await session.rollback()  # Откат в случае ошибки
            logging.error(f"Ошибка при добавлении пользователя: {ex}")

# Асинхронная функция для получения пользователя по ID
async def get_user_by_id(user_id: int):
    async for session in get_session():
        result = await session.execute(select(User).filter(User.id == user_id))
        return result.scalars().first()

# Асинхронная функция для получения пользователя по имени пользователя
async def get_user_by_username(username: str):
    async for session in get_session():
        result = await session.execute(select(User).filter(User.username == username))
        return result.scalars().first()

# Асинхронная функция для получения всех пользователей
async def get_all_users():
    async for session in get_session():
        result = await session.execute(select(User))
        return result.scalars().all()
