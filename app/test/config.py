import os
from sqlmodel import create_engine, Session
from sqlmodel import Session
from sqlalchemy import  StaticPool



DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = Session.bind(engine)

# Dependency to override the get_db dependency in the main app
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Example usage with FastAPI
# from app.main import app, get_db
# app.dependency_overrides[get_db] = override_get_db


