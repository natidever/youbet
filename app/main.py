from fastapi import FastAPI, Depends
from sqlmodel import select
# from app.models.core_models import User
from app.api.agent.agent_router import agent_router
from app.api.auth.auth_router import auth_router
from app.api.auth.auth_service import get_password_hash
from app.api.casino.casino_router import casino_router
from app.config.db import init_db, get_session
from app.constants.role import UserRole
from app.models.core_models import User
from app.websocket.websocket_consumer import websocket_consumer
from app.websocket.websocket_router import websocket_router

import asyncio

async def lifespan(app: FastAPI):
    print("Initializing Socket Consumer...")
    # init_db()
    task=asyncio.create_task(websocket_consumer())

    yield
    task.cancel()
    await task
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)


app.include_router(agent_router)
app.include_router(casino_router)
app.include_router(auth_router)
app.include_router(websocket_router)





# @app.post("/users/")
# def create_user(user: User, session = Depends(get_session)):
#     session.add(user)
#     session.commit()
#     session.refresh(user)
#     return user

@app.get("/")
def create_admin(session=Depends(get_session)):
    password=get_password_hash(password="hana@teshager")

    # return "Server  runnin" 


    try:
        admin = User(
            username="natnael",
            password_hash=password,
            role=UserRole.ADMIN
        )

        session.add(admin)
        session.commit()
        session.refresh(admin)
        print("admin:created")
        return admin
    except Exception as e :
        print(f"error:{e}")
   







def create_first_admin():
    pass


    
    
    