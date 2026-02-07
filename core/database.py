from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

#SQLITE3 Database URL
DATABASE_URL = "sqlite:///./usage.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
