from fastapi import FastAPI, Depends
from sqlmodel import select
from app.models.user import User
from app.config.db import init_db, get_session

def lifespan(app: FastAPI):
    print("Initializing DB...")
    init_db()
    yield
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)

@app.post("/users/")
def create_user(user: User, session = Depends(get_session)):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@app.get("/users/")
def get_users(session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return users
