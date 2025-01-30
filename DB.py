from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Указываем данные для подключения
DATABASE_URL = "postgresql://postgres:12345@localhost/weather_bot"

# Создаём движок SQLAlchemy
engine = create_engine(DATABASE_URL, echo=False)

# Определяем базовый класс для моделей
Base = declarative_base()

# Определяем модель таблицы users
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    city = Column(String, nullable=True)

# Создаём таблицы, если их нет
Base.metadata.create_all(engine)

# Создаём сессию для работы с базой
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Функция для получения пользователя по username
def get_user(username: str):
    session = SessionLocal()
    user = session.query(User).filter_by(username=username).first()
    session.close()
    return user
