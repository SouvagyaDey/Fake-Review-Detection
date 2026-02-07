from sqlalchemy import Column, Integer, String, Boolean
from core.database import Base

#User table schema to store user information and API keys

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    api_key = Column(String, unique=True, index=True)
    is_admin = Column(Boolean, default=False)
