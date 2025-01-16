from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from typing import AsyncGenerator, Optional

# Создаем базовый класс для всех моделей
Base = declarative_base()

# Определяем модель User
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    city = Column(String)

# Создаем асинхронный движок для работы с PostgreSQL
DATABASE_URL = "postgresql+asyncpg://username:password@localhost/dbname"
engine = create_async_engine(DATABASE_URL, echo=True)

# Создаем асинхронную сессию
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Функция для получения сессии
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

# Функция для добавления нового пользователя
async def add_user(username: str, city: str) -> User:
    async for session in get_session():
        user = User(username=username, city=city)
        session.add(user)
        await session.commit()
        return user

# Функция для получения пользователя по имени пользователя
async def get_user_by_username(username: str) -> Optional[User]:
    async for session in get_session():
        result = await session.execute(select(User).filter_by(username=username))
        user = result.scalars().first()  # Получаем первого пользователя или None
        return user
