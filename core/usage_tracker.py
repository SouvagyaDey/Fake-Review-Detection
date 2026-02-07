from sqlalchemy import Column, Integer, String, DateTime
from core.database import Base

# APIusage table schema to track usage(only for Admin)

class APIUsage(Base):
    __tablename__ = "api_usage"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    endpoint = Column(String, index=True)
    minute_bucket = Column(DateTime, index=True)
    request_count = Column(Integer, default=1)
