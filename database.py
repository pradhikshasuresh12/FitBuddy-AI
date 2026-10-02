"""
database.py — SQLite + SQLAlchemy setup for FitBuddy.

Creates the engine, session factory, declarative base, and User model.
The database file (fitbuddy.db) is created automatically on first run.
"""

import os
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./fitbuddy.db")

# check_same_thread=False lets FastAPI use the SQLite connection across request threads
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    """Stores a user's profile and their generated 7-day fitness plan."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    age = Column(Integer, nullable=False)
    fitness_goal = Column(String(120), nullable=False)
    workout_intensity = Column(String(120), nullable=False)
    plan = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


def init_db():
    """Create all tables if they don't exist yet."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """FastAPI dependency that yields a database session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
