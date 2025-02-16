from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import db_url

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    city = Column(String, nullable=True)

class UserRepository:
    def __init__(self):
        self.engine = create_engine(db_url, echo=False)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def get_user(self, username: str):
        with self.Session() as session:
            return session.query(User).filter_by(username=username).first()

    def add_or_update_user(self, username: str, city: str):
        with self.Session() as session:
            user = session.query(User).filter_by(username=username).first()
            if user:
                user.city = city
            else:
                user = User(username=username, city=city)
                session.add(user)
            session.commit()
            return user