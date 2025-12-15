"""
Database configuration for Neon Serverless Postgres.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

# Get database URL from environment variable
DATABASE_URL = os.getenv("NEON_DATABASE_URL", "postgresql+asyncpg://user:password@localhost/dbname")

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    # echo=True,  # Uncomment to log SQL queries
)

# Create async session maker
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base class for declarative models
Base = declarative_base()

async def get_db():
    """Dependency to get database session."""
    async with AsyncSessionLocal() as session:
        yield session