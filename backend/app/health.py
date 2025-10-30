"""Health check functionality for the coffee machine."""
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from app.storage import StorageInterface
from app.logger import logger
from app.dependencies import get_service


class HealthChecker:
    """Comprehensive health checker for the coffee machine system."""
    
    def __init__(self, storage: StorageInterface):
        """Initialize health checker with storage backend."""
        self.storage = storage
        self.start_time = datetime.now()
        self._service = None
    
    async def check_health(self) -> Dict[str, Any]:
        """
        Perform comprehensive health check.
        
        Returns:
            Dictionary with overall status and individual check results
        """
        health_status = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "uptime": str(datetime.now() - self.start_time),
            "checks": {}
        }
        
        # Check storage
        storage_check = await self._check_storage()
        health_status["checks"]["storage"] = storage_check
        
        # Check system resources
        system_check = self._check_system_resources()
        health_status["checks"]["system"] = system_check
        
        # Check coffee machine state
        machine_check = await self._check_machine_state()
        health_status["checks"]["machine"] = machine_check
        
        # Determine overall status
        if any(check.get("status") == "unhealthy" for check in health_status["checks"].values()):
            health_status["status"] = "unhealthy"
        elif any(check.get("status") == "degraded" for check in health_status["checks"].values()):
            health_status["status"] = "degraded"
        
        return health_status
    
    async def _check_storage(self) -> Dict[str, Any]:
        """Check if storage is accessible and working."""
        try:
            state = self.storage.load_state()
            return {
                "status": "healthy",
                "message": "Storage accessible",
                "type": type(self.storage).__name__
            }
        except Exception as e:
            logger.error("Storage health check failed", error=str(e))
            return {
                "status": "unhealthy",
                "message": f"Storage error: {str(e)}"
            }
    
    def _check_system_resources(self) -> Dict[str, Any]:
        """Check system CPU and memory usage."""
        try:
            import psutil
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            status = "healthy"
            warnings = []
            
            if cpu_percent > 80 or memory.percent > 80:
                status = "degraded"
                if cpu_percent > 80:
                    warnings.append(f"High CPU usage: {cpu_percent:.1f}%")
                if memory.percent > 80:
                    warnings.append(f"High memory usage: {memory.percent:.1f}%")
            
            if cpu_percent > 95 or memory.percent > 95:
                status = "unhealthy"
            
            result = {
                "status": status,
                "cpu_percent": round(cpu_percent, 2),
                "memory_percent": round(memory.percent, 2),
                "disk_percent": round(disk.percent, 2),
            }
            
            if warnings:
                result["warnings"] = warnings
            
            return result
        except Exception as e:
            logger.warning("Could not check system resources", error=str(e))
            return {
                "status": "unknown",
                "message": f"Could not check system resources: {str(e)}"
            }
    
    async def _check_machine_state(self) -> Dict[str, Any]:
        """Check coffee machine state."""
        try:
            state = self.storage.load_state()
            
            water_percent = (state.water_container.current_amount / 
                           state.water_container.capacity) * 100 if state.water_container.capacity > 0 else 0
            coffee_percent = (state.coffee_container.current_amount / 
                            state.coffee_container.capacity) * 100 if state.coffee_container.capacity > 0 else 0
            
            status = "healthy"
            warnings = []
            
            if water_percent < 10 or coffee_percent < 10:
                status = "degraded"
                if water_percent < 10:
                    warnings.append("Water level critically low")
                if coffee_percent < 10:
                    warnings.append("Coffee level critically low")
            
            result = {
                "status": status,
                "water_level_percent": round(water_percent, 2),
                "coffee_level_percent": round(coffee_percent, 2),
                "total_coffees_made": state.total_coffees_made,
            }
            
            if warnings:
                result["warnings"] = warnings
            
            return result
        except Exception as e:
            logger.error("Machine state health check failed", error=str(e))
            return {
                "status": "unhealthy",
                "message": f"Cannot read machine state: {str(e)}"
            }

