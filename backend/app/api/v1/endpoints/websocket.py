"""WebSocket endpoints for real-time updates."""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, WebSocketException, status
from app.websocket_manager import manager
from app.services import CoffeeMachineService
from app.dependencies import get_service
from app.logger import logger
from app.config import get_settings
from datetime import datetime

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    client_id: str = None
):
    """
    WebSocket endpoint for real-time updates.
    
    Clients will receive:
    - status_update: When machine status changes
    - coffee_made: When coffee is made
    - container_filled: When containers are filled
    - error: When errors occur
    
    Args:
        websocket: WebSocket connection
        client_id: Optional client identifier
    """
    # Validate origin for WebSocket (FastAPI doesn't automatically validate WebSocket origins)
    origin = websocket.headers.get("origin")
    settings = get_settings()
    allowed_origins = settings.cors_origins.split(",") if "," in settings.cors_origins else [settings.cors_origins]
    allowed_origins = [o.strip() for o in allowed_origins]
    
    if origin and origin not in allowed_origins and "*" not in allowed_origins:
        logger.warning(f"WebSocket connection rejected: origin {origin} not in allowed origins")
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    
    # Accept WebSocket connection
    await manager.connect(websocket, client_id)

    # Safe status push: try and log error if it fails
    try:
        service = get_service()
        status = service.get_status()
        await manager.send_personal_message(
            {
                "type": "status_update",
                "data": status["data"],
                "timestamp": datetime.now().isoformat(),
            },
            websocket,
        )
    except Exception as err:
        logger.error(f"Failed to send initial status_update after connect: {err}")
    
    try:
        while True:
            # Wait for messages from client
            data = await websocket.receive_text()
            
            # Handle different message types from client
            if data == "ping":
                await manager.send_personal_message(
                    {"type": "pong", "timestamp": datetime.now().isoformat()},
                    websocket
                )
            elif data == "request_status":
                # Client requesting current status
                # Note: This would need proper dependency injection
                # For now, we'll broadcast a status update request
                pass
    
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info("Client disconnected normally")
    
    except Exception as e:
        logger.error("WebSocket error", error=str(e))
        manager.disconnect(websocket)


@router.get("/ws/stats")
async def get_websocket_stats():
    """
    Get WebSocket connection statistics.
    
    Returns:
        Dictionary with active connections and statistics
    """
    return manager.get_stats()

