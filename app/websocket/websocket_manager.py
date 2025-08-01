# this will handler websocket connection including hadling connection ,disconnection 
# and retry mechanism if needed



from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast_game_data(self, data: dict):
        for connection in self.active_connections:
         await connection.send_json(data)
        # """Send game data to all connected clients"""
        # for connection in self.active_connections.values():
        #     await connection.send_json(data)
      


            