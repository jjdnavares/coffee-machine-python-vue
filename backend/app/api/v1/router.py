"""Main router for v1 API that combines all endpoint routers."""
from fastapi import APIRouter
from app.api.v1.endpoints import coffee, management, health, websocket

api_router = APIRouter()

# Include coffee endpoints
api_router.include_router(
    coffee.router,
    prefix="/coffee",
    tags=["Coffee Making"]
)

# Include management endpoints
api_router.include_router(
    management.router,
    prefix="",
    tags=["Machine Management"]
)

# Include health check endpoints
api_router.include_router(
    health.router,
    prefix="/health",
    tags=["System Health"]
)

# Include WebSocket endpoints
api_router.include_router(
    websocket.router,
    prefix="",
    tags=["WebSocket"]
)

