from fastapi import WebSocket, APIRouter
from app.websocket.manager import ws_manager
import asyncio

router = APIRouter()

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await websocket.accept()
    try:
        while True:
            while notification := ws_manager.pop_notification(user_id):
                await websocket.send_json(notification)
            await asyncio.sleep(0.1)
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await websocket.close()