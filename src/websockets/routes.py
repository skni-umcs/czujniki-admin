import logging
from .manager import sensor_manager, service_manager

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter(prefix="/ws", tags=["websockets"])

@router.websocket("/sensors")
async def websocket_ping(websocket: WebSocket):
    await sensor_manager.connect(websocket)
    try:
        while True:
            msg = await websocket.receive_text()
            if msg == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        sensor_manager.disconnect(websocket)
        logging.info("WebSocket disconnected")

@router.websocket("/service")
async def websocket_ping(websocket: WebSocket):
    await service_manager.connect(websocket)
    try:
        while True:
            msg = await websocket.receive_text()
            if msg == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        service_manager.disconnect(websocket)
        logging.info("WebSocket disconnected")