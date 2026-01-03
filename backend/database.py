from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL

# Configure engine with proper SSL settings for PostgreSQL
if DATABASE_URL and DATABASE_URL.startswith("postgresql"):
    # Add SSL mode for PostgreSQL connections
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
else:
    # Use SQLite for fallback
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()