from sqlalchemy import Column, String, Integer, DateTime
from app.database import Base
from datetime import datetime, timezone

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    email = Column(String, unique=True, index=True, nullable=True)
    phone = Column(String, nullable=True)
    city = Column(String, nullable=True)
    street = Column(String, nullable=True)
    building = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow) 