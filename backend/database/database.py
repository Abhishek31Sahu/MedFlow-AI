"""
Database Configuration
"""

from sqlalchemy import create_engine,text

from sqlalchemy.orm import (
    declarative_base,
    sessionmaker
)
from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"
load_dotenv(ENV_FILE)

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")


engine = create_engine(
    DATABASE_URL
)

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version();"))
        print("✅ PostgreSQL connected!")
        print(result.fetchone())
except Exception as e:
    print("❌ PostgreSQL connection failed!")
    print(e)
SessionLocal = sessionmaker(

    autocommit=False,

    autoflush=False,

    bind=engine
)


Base = declarative_base()


def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()