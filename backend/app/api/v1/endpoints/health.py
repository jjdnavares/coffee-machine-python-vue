"""Health check endpoints for v1 API."""
from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse
from datetime import datetime

router = APIRouter()

# Global health checker instance (set during startup)
_health_checker = None


def set_health_checker(checker):
    """Set the global health checker instance."""
    global _health_checker
    _health_checker = checker


@router.get(
    "",
    tags=["System Health"],
    summary="Health Check",
    description="Comprehensive health check including storage, system resources, and machine state.",
    responses={
        200: {
            "description": "Detailed health status",
        }
    }
)
async def health_check():
    """
    Comprehensive health check endpoint.
    
    Returns detailed information about:
    - Storage system status
    - System resource usage (CPU, memory, disk)
    - Machine state (container levels, warnings)
    
    Overall status can be: healthy, degraded, or unhealthy
    """
    if _health_checker is None:
        return {"status": "unknown", "message": "Health checker not initialized"}
    
    return await _health_checker.check_health()


@router.get(
    "/live",
    tags=["System Health"],
    summary="Liveness Probe",
    description="Kubernetes-style liveness probe. Returns 200 if server is running.",
)
async def liveness_probe():
    """
    Kubernetes-style liveness probe.
    Returns 200 if server is running.
    """
    return {"status": "alive"}


@router.get(
    "/ready",
    tags=["System Health"],
    summary="Readiness Probe",
    description="Kubernetes-style readiness probe. Returns 200 if server is ready to accept traffic.",
)
async def readiness_probe():
    """
    Kubernetes-style readiness probe.
    Returns 200 if server is ready to accept traffic.
    Returns 503 if server is not ready.
    """
    if _health_checker is None:
        return JSONResponse(
            status_code=503,
            content={"status": "not_ready", "message": "Health checker not initialized"}
        )
    
    health = await _health_checker.check_health()
    
    if health["status"] == "unhealthy":
        return JSONResponse(
            status_code=503,
            content=health
        )
    
    return {"status": "ready"}

