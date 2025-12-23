from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.sql import func
from backend.database import Base
import enum

class ExperienceLevel(enum.Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    python_knowledge = Column(Boolean, default=False)
    has_nvidia_gpu = Column(Boolean, default=False)
    experience_level = Column(Enum(ExperienceLevel), default=ExperienceLevel.beginner)
    created_at = Column(DateTime(timezone=True), server_default=func.now())