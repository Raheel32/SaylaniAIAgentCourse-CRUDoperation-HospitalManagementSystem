"""
database.py
------------
Sets up the connection to PostgreSQL and provides a session that the
rest of the app uses to talk to the database.

Unlike the earlier SQLite project, this one uses a real database server
(PostgreSQL) — connection details come from config.py / .env, not
hardcoded here.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import settings

# --- Engine ---
# The engine is the actual connection point to PostgreSQL.
engine = create_engine(settings.database_url)

# --- Session ---
# Each request gets its own session (see get_db() in main.py).
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- Base ---
# All models (Doctor, Patient, Staff) inherit from this.
Base = declarative_base()


def get_db():
    """
    Dependency that provides a database session to each request,
    and closes it afterwards automatically — even if an error occurs.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
