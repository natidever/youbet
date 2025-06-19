# this is the gateway in which the endpoint reside like ws://this is websocket endpoint


from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.websocket.websocket_manager import ConnectionManager


websocket_router = APIRouter(tags=["Websockets"])
manager=ConnectionManager()


@websocket_router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            # Just keep connection open, no need to receive messages
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, client_id)