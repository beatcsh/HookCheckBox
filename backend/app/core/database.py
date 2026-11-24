import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")

engine = create_async_engine( DB_URL, echo = True )

AsyncSessionLocal = async_sessionmaker( bind = engine, expire_on_commit = False )

class Base(DeclarativeBase):
    pass