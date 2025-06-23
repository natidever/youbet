# import os
# from sqlmodel import create_engine, Session
# from sqlmodel import Session
# from sqlalchemy import  StaticPool


# from sqlalchemy.orm import sessionmaker

# DATABASE_URL = "sqlite:///:memory:"

# engine = create_engine(
#     DATABASE_URL,
#     connect_args={"check_same_thread": False},
#     poolclass=StaticPool,
# )

# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# # Dependency to override the get_db dependency in the main app
# def override_get_db():
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# # Example usage with FastAPI
# # from app.main import app, get_db
# # app.dependency_overrides[get_db] = override_get_db


import pytest
from sqlmodel import SQLModel, create_engine, Session, select

@pytest.fixture(name="engine")
def engine_fixture():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    yield engine
    # The database disappears when tests are done

# This gives us a database session to work with
@pytest.fixture(name="session")
def session_fixture(engine):
    with Session(engine) as session:
        yield session