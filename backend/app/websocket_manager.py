"""WebSocket connection manager for real-time updates."""
from typing import List, Dict, Any
from fastapi import WebSocket
from app.logger import logger
from datetime import datetime


class ConnectionManager:
    """Manages WebSocket connections and broadcasts messages to clients."""
    
    def __init__(self):
        """Initialize connection manager."""
        self.active_connections: List[WebSocket] = []
        self.connection_metadata: Dict[WebSocket, Dict[str, Any]] = {}
    
    async def connect(self, websocket: WebSocket, client_id: str = None):
        """
        Accept and register a new WebSocket connection.
        
        Args:
            websocket: WebSocket connection
            client_id: Optional client identifier
        """
        await websocket.accept()
        self.active_connections.append(websocket)
        self.connection_metadata[websocket] = {
            "client_id": client_id,
            "connected_at": datetime.now().isoformat(),
        }
        logger.info(
            "WebSocket connected",
            client_id=client_id,
            total_connections=len(self.active_connections)
        )
    
    def disconnect(self, websocket: WebSocket):
        """
        Remove a WebSocket connection.
        
        Args:
            websocket: WebSocket connection to remove
        """
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            metadata = self.connection_metadata.pop(websocket, {})
            logger.info(
                "WebSocket disconnected",
                client_id=metadata.get("client_id"),
                total_connections=len(self.active_connections)
            )
    
    async def send_personal_message(self, message: Dict[str, Any], websocket: WebSocket):
        """
        Send a message to a specific client.
        
        Args:
            message: Message to send
            websocket: Target WebSocket connection
        """
        try:
            await websocket.send_json(message)
        except Exception as e:
            logger.error("Error sending message to client", error=str(e))
            self.disconnect(websocket)
    
    async def broadcast(self, message: Dict[str, Any], exclude: WebSocket = None):
        """
        Broadcast a message to all connected clients.
        
        Args:
            message: Message to broadcast
            exclude: WebSocket connection to exclude from broadcast
        """
        disconnected = []
        for connection in self.active_connections:
            if connection == exclude:
                continue
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error("Error broadcasting to client", error=str(e))
                disconnected.append(connection)
        
        # Clean up disconnected clients
        for conn in disconnected:
            self.disconnect(conn)
    
    async def broadcast_status_update(self, status: Dict[str, Any]):
        """
        Broadcast machine status update to all clients.
        
        Args:
            status: Machine status data
        """
        message = {
            "type": "status_update",
            "data": status,
            "timestamp": datetime.now().isoformat()
        }
        await self.broadcast(message)
    
    async def broadcast_coffee_made(self, coffee_type: str, resources_used: Dict[str, float]):
        """
        Broadcast coffee making event.
        
        Args:
            coffee_type: Type of coffee made
            resources_used: Resources consumed
        """
        message = {
            "type": "coffee_made",
            "coffee_type": coffee_type,
            "resources_used": resources_used,
            "timestamp": datetime.now().isoformat()
        }
        await self.broadcast(message)
    
    async def broadcast_error(self, error_message: str, error_type: str):
        """
        Broadcast error to all clients.
        
        Args:
            error_message: Error message
            error_type: Type of error
        """
        message = {
            "type": "error",
            "error_type": error_type,
            "message": error_message,
            "timestamp": datetime.now().isoformat()
        }
        await self.broadcast(message)
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get connection statistics.
        
        Returns:
            Dictionary with connection statistics
        """
        return {
            "total_connections": len(self.active_connections),
            "connections": [
                {
                    "client_id": meta.get("client_id"),
                    "connected_at": meta.get("connected_at")
                }
                for meta in self.connection_metadata.values()
            ]
        }


# Global connection manager instance
manager = ConnectionManager()

