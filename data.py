from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import db_url

DATABASE_URL = db_url

# Создание движка для работы с базой данных
engine = create_engine(DATABASE_URL, echo=False)
Base = declarative_base()

# Определение модели User
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    city = Column(String, nullable=True)

# Создание всех таблиц в базе данных
Base.metadata.create_all(engine)

# Создание сессии для работы с базой данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Функция для получения пользователя по username
def get_user(username: str):
    session = SessionLocal()
    user = session.query(User).filter_by(username=username).first()
    session.close()
    return user

# Функция для добавления или обновления пользователя
def add_or_update_user(username: str, city: str):
    session = SessionLocal()
    user = session.query(User).filter_by(username=username).first()

    if user:
        user.city = city
    else:
        user = User(username=username, city=city)
        session.add(user)

    session.commit()
    session.close()
