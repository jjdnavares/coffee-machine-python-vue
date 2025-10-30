"""FastAPI application for coffee machine API."""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.exceptions import (
    CoffeeMachineException,
    exception_handler
)
from app.services import CoffeeMachineService
from app.storage import get_storage
from app.dependencies import set_service_instance
from app.api.v1.router import api_router as api_v1_router
from app.rate_limiter import limiter, rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.middleware import RequestLoggingMiddleware, ErrorLoggingMiddleware
from app.logger import logger
from app.health import HealthChecker
from app.api.v1.endpoints.health import set_health_checker


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown."""
    # Startup
    global _service_instance
    settings = get_settings()
    storage = get_storage(settings.storage_type, file_path=settings.data_path)
    service_instance = CoffeeMachineService(storage)
    set_service_instance(service_instance)
    
    # Initialize health checker
    health_checker = HealthChecker(storage)
    set_health_checker(health_checker)
    
    logger.info(
        "api_started",
        storage_type=settings.storage_type,
        version="1.0.0"
    )
    yield
    # Shutdown (if needed)


app = FastAPI(
    title="Coffee Machine API",
    version="1.0.0",
    description="""
    ## Coffee Machine API Documentation
    
    This API manages a virtual coffee machine with the following features:
    
    * **Coffee Types:** Espresso, Double Espresso, Ristretto, and Americano
    * **Container Management:** Fill water and coffee containers
    * **Status Monitoring:** Real-time status of containers and statistics
    * **State Persistence:** Machine state persists between requests
    
    ### Coffee Recipes
    
    - **Espresso:** 8g coffee, 24ml water
    - **Double Espresso:** 16g coffee, 48ml water
    - **Ristretto:** 8g coffee, 16ml water (short concentrated shot)
    - **Americano:** 16g coffee, 148ml water
    
    ### Container Capacities
    
    - **Water Container:** 2000ml (default, configurable)
    - **Coffee Container:** 500g (default, configurable)
    
    ### Error Handling
    
    All errors return user-friendly messages with detailed information about what went wrong.
    """,
    lifespan=lifespan,
    contact={
        "name": "Coffee Machine API",
    },
    license_info={
        "name": "MIT",
    }
)

# Configure CORS
settings = get_settings()
origins = settings.cors_origins.split(",") if "," in settings.cors_origins else [settings.cors_origins]

# Add middleware in order (last added is outermost)
app.add_middleware(ErrorLoggingMiddleware)
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add exception handlers
app.add_exception_handler(CoffeeMachineException, exception_handler)
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)

# Add rate limiter to app state
app.state.limiter = limiter

# Include API v1 router with version prefix
app.include_router(api_v1_router, prefix="/api/v1")

# Include API v1 router without version prefix for backward compatibility
app.include_router(api_v1_router, prefix="/api")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
