"""
User model for the application.
"""

from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from ..core.database import Base
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# SQLAlchemy Model
class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    software_hardware_background = Column(Text, nullable=True)  # Stores user's background
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

# Pydantic Models for API requests/responses
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str
    software_hardware_background: Optional[str] = None

class UserUpdate(BaseModel):
    software_hardware_background: Optional[str] = None

class UserResponse(UserBase):
    id: int
    software_hardware_background: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True