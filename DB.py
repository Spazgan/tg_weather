import asyncio
import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, BigInteger, String, Boolean, select
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    user_id = Column(BigInteger, primary_key= True)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    is_blocked = Column(Boolean, default=False)

DATABASE_URL = "postgresql+asyncpg://username:12345@localhost:5432/database_name"

engine = create_async_engine(DATABASE_URL, echo = True)

async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
async def get_all_users():
    async with async_session() as session:
     
     result = await session.execute(select(User))
    users = result.scalars().all()
    print(f"Fetched {len(users)} users from the database.")
    return users

async def get_user_by_id(user_id:int):
   async with async_session() as session:
      result = await session.execute(select(User).filter(User.user_id == user_id))
      user = result.scalar()
      print(f"Fetched user {user_id} from the database.")
      return user

async def add_user(user_id: int, username: str, first_name: str, last_name: str):
   async with async_session() as session:
      async with session.begin():
         new_user = User(user_id=user_id, username=username,first_name=first_name, last_name=last_name)
         session.add(new_user)
         await select.commit()
         print(f"Added user {user_id} to the database.")
