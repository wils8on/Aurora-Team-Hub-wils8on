import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base


load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///data/gestao.db"
)

engine_args = {}

if DATABASE_URL.startswith("sqlite"):
    engine_args["connect_args"] = {
        "check_same_thread": False
    }

engine = create_engine(
    DATABASE_URL,
    **engine_args
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()