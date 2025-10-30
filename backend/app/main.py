"""FastAPI application for coffee machine API."""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.models import (
    CoffeeType,
    FillRequest,
    MessageResponse,
    StatusResponse,
    ErrorResponse
)
from app.services import CoffeeMachineService
from app.storage import get_storage
from app.exceptions import (
    CoffeeMachineException,
    exception_handler
)


# Global service instance
_service_instance: CoffeeMachineService = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown."""
    # Startup
    global _service_instance
    settings = get_settings()
    storage = get_storage(settings.storage_type, file_path=settings.data_path)
    _service_instance = CoffeeMachineService(storage)
    print(f"Coffee Machine API started. Storage: {settings.storage_type}")
    yield
    # Shutdown (if needed)


app = FastAPI(
    title="Coffee Machine API",
    version="1.0.0",
    description="""
    ## Coffee Machine API Documentation
    
    This API manages a virtual coffee machine with the following features:
    
    * **Coffee Types:** Espresso, Double Espresso, and Americano
    * **Container Management:** Fill water and coffee containers
    * **Status Monitoring:** Real-time status of containers and statistics
    * **State Persistence:** Machine state persists between requests
    
    ### Coffee Recipes
    
    - **Espresso:** 8g coffee, 24ml water
    - **Double Espresso:** 16g coffee, 48ml water
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add exception handler
app.add_exception_handler(CoffeeMachineException, exception_handler)


def get_service() -> CoffeeMachineService:
    """Dependency to get coffee machine service."""
    if _service_instance is None:
        settings = get_settings()
        storage = get_storage(settings.storage_type, file_path=settings.data_path)
        return CoffeeMachineService(storage)
    return _service_instance


@app.get(
    "/api/health",
    tags=["Health"],
    summary="Health Check",
    description="Check if the API is running and healthy.",
    responses={
        200: {
            "description": "API is healthy",
            "content": {
                "application/json": {
                    "example": {
                        "status": "healthy",
                        "timestamp": "2024-01-15T10:30:00.123456"
                    }
                }
            }
        }
    }
)
async def health_check():
    """
    Health check endpoint to verify the API is running.
    
    Returns:
        - **status**: Always "healthy" if the API is running
        - **timestamp**: Current server time in ISO format
    """
    from datetime import datetime
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.get(
    "/api/status",
    response_model=StatusResponse,
    tags=["Status"],
    summary="Get Machine Status",
    description="Retrieve the current status of the coffee machine including container levels and statistics.",
    responses={
        200: {
            "description": "Machine status retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "data": {
                            "water_level": 1750.0,
                            "water_capacity": 2000.0,
                            "water_percentage": 87.5,
                            "coffee_level": 420.0,
                            "coffee_capacity": 500.0,
                            "coffee_percentage": 84.0,
                            "total_coffees_made": 42
                        }
                    }
                }
            }
        }
    }
)
async def get_status(service: CoffeeMachineService = Depends(get_service)):
    """
    Get the current status of the coffee machine.
    
    Returns detailed information about:
    - Water container level and capacity
    - Coffee container level and capacity
    - Percentage fill levels for both containers
    - Total number of coffees made
    
    Response includes all data needed for displaying machine status in the UI.
    """
    return service.get_status()


@app.post(
    "/api/coffee/espresso",
    response_model=MessageResponse,
    tags=["Coffee"],
    summary="Make Espresso",
    description="Brew a single espresso using 8g of coffee and 24ml of water.",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Espresso successfully brewed",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "message": "Espresso ready!"
                    }
                }
            }
        },
        409: {
            "description": "Insufficient resources to make espresso",
            "content": {
                "application/json": {
                    "example": {
                        "success": False,
                        "message": "Cannot make espresso. Need 24.0ml water but only 10.0ml available.",
                        "error_type": "InsufficientResourcesException",
                        "details": {
                            "resource_type": "water",
                            "needed": 24.0,
                            "available": 10.0
                        }
                    }
                }
            }
        }
    }
)
async def make_espresso(service: CoffeeMachineService = Depends(get_service)):
    """
    Make a single espresso.
    
    Requires:
    - 8g of coffee
    - 24ml of water
    
    The machine will automatically deduct resources and increment the coffee counter.
    
    Returns a success message if the espresso is successfully brewed.
    
    Raises InsufficientResourcesException (409) if there aren't enough resources.
    """
    try:
        return service.make_coffee(CoffeeType.ESPRESSO)
    except CoffeeMachineException:
        raise


@app.post(
    "/api/coffee/double-espresso",
    response_model=MessageResponse,
    tags=["Coffee"],
    summary="Make Double Espresso",
    description="Brew a double espresso using 16g of coffee and 48ml of water.",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Double espresso successfully brewed",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "message": "Double espresso ready!"
                    }
                }
            }
        },
        409: {
            "description": "Insufficient resources to make double espresso",
            "content": {
                "application/json": {
                    "example": {
                        "success": False,
                        "message": "Cannot make double espresso. Need 48.0ml water but only 30.0ml available.",
                        "error_type": "InsufficientResourcesException",
                        "details": {
                            "resource_type": "water",
                            "needed": 48.0,
                            "available": 30.0
                        }
                    }
                }
            }
        }
    }
)
async def make_double_espresso(service: CoffeeMachineService = Depends(get_service)):
    """
    Make a double espresso.
    
    Requires:
    - 16g of coffee
    - 48ml of water
    
    Returns a success message if the double espresso is successfully brewed.
    
    Raises InsufficientResourcesException (409) if there aren't enough resources.
    """
    try:
        return service.make_coffee(CoffeeType.DOUBLE_ESPRESSO)
    except CoffeeMachineException:
        raise


@app.post(
    "/api/coffee/americano",
    response_model=MessageResponse,
    tags=["Coffee"],
    summary="Make Americano",
    description="Brew an americano using 16g of coffee and 148ml of water.",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Americano successfully brewed",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "message": "Americano ready!"
                    }
                }
            }
        },
        409: {
            "description": "Insufficient resources to make americano",
            "content": {
                "application/json": {
                    "example": {
                        "success": False,
                        "message": "Cannot make americano. Need 148.0ml water but only 100.0ml available.",
                        "error_type": "InsufficientResourcesException",
                        "details": {
                            "resource_type": "water",
                            "needed": 148.0,
                            "available": 100.0
                        }
                    }
                }
            }
        }
    }
)
async def make_americano(service: CoffeeMachineService = Depends(get_service)):
    """
    Make an americano.
    
    Requires:
    - 16g of coffee
    - 148ml of water
    
    Returns a success message if the americano is successfully brewed.
    
    Raises InsufficientResourcesException (409) if there aren't enough resources.
    """
    try:
        return service.make_coffee(CoffeeType.AMERICANO)
    except CoffeeMachineException:
        raise


@app.post(
    "/api/fill/water",
    response_model=MessageResponse,
    tags=["Management"],
    summary="Fill Water Container",
    description="Add water to the water container. The amount is added to the current level.",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Water successfully added to container",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "message": "Added 500.0ml of water. Container now at 500.0ml/2000.0ml"
                    }
                }
            }
        },
        409: {
            "description": "Container overflow - amount exceeds capacity",
            "content": {
                "application/json": {
                    "example": {
                        "success": False,
                        "message": "Cannot add 2500.0ml to water container. Current: 1800.0ml, Capacity: 2000.0ml, Would overflow by 2300.0ml.",
                        "error_type": "ContainerOverflowException",
                        "details": {
                            "container_type": "water",
                            "capacity": 2000.0,
                            "current_amount": 1800.0,
                            "attempted_amount": 2500.0
                        }
                    }
                }
            }
        },
        422: {
            "description": "Invalid amount (must be positive)",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "type": "value_error",
                                "loc": ["body", "amount"],
                                "msg": "Value error, amount must be greater than 0",
                                "input": -10
                            }
                        ]
                    }
                }
            }
        }
    }
)
async def fill_water(
    request: FillRequest,
    service: CoffeeMachineService = Depends(get_service)
):
    """
    Fill the water container with the specified amount.
    
    **Request Body:**
    - `amount` (float): Amount of water to add in milliliters (must be positive)
    
    **Example Request:**
    ```json
    {
        "amount": 500
    }
    ```
    
    The amount is added to the current water level. The operation will fail if:
    - The amount is not positive (422 error)
    - Adding the amount would exceed the container capacity (409 error)
    
    Returns a message indicating the new water level.
    """
    try:
        return service.fill_water(request.amount)
    except CoffeeMachineException:
        raise


@app.post(
    "/api/fill/coffee",
    response_model=MessageResponse,
    tags=["Management"],
    summary="Fill Coffee Container",
    description="Add coffee to the coffee container. The amount is added to the current level.",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Coffee successfully added to container",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "message": "Added 250.0g of coffee. Container now at 250.0g/500.0g"
                    }
                }
            }
        },
        409: {
            "description": "Container overflow - amount exceeds capacity",
            "content": {
                "application/json": {
                    "example": {
                        "success": False,
                        "message": "Cannot add 600.0g to coffee container. Current: 200.0g, Capacity: 500.0g, Would overflow by 300.0g.",
                        "error_type": "ContainerOverflowException",
                        "details": {
                            "container_type": "coffee",
                            "capacity": 500.0,
                            "current_amount": 200.0,
                            "attempted_amount": 600.0
                        }
                    }
                }
            }
        },
        422: {
            "description": "Invalid amount (must be positive)",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "type": "value_error",
                                "loc": ["body", "amount"],
                                "msg": "Value error, amount must be greater than 0",
                                "input": 0
                            }
                        ]
                    }
                }
            }
        }
    }
)
async def fill_coffee(
    request: FillRequest,
    service: CoffeeMachineService = Depends(get_service)
):
    """
    Fill the coffee container with the specified amount.
    
    **Request Body:**
    - `amount` (float): Amount of coffee to add in grams (must be positive)
    
    **Example Request:**
    ```json
    {
        "amount": 250
    }
    ```
    
    The amount is added to the current coffee level. The operation will fail if:
    - The amount is not positive (422 error)
    - Adding the amount would exceed the container capacity (409 error)
    
    Returns a message indicating the new coffee level.
    """
    try:
        return service.fill_coffee(request.amount)
    except CoffeeMachineException:
        raise


@app.post(
    "/api/reset",
    response_model=MessageResponse,
    tags=["Management"],
    summary="Reset Machine",
    description="Reset the coffee machine to its initial empty state. This clears all containers and resets all counters.",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Machine successfully reset",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "message": "Machine reset successfully. All containers emptied and counters reset."
                    }
                }
            }
        }
    }
)
async def reset_machine(service: CoffeeMachineService = Depends(get_service)):
    """
    Reset the coffee machine to empty state.
    
    This operation:
    - Empties the water container (sets to 0ml)
    - Empties the coffee container (sets to 0g)
    - Resets the total coffees made counter to 0
    
    Useful for testing or starting fresh. The reset state is persisted immediately.
    
    **Warning:** This operation cannot be undone. All state is permanently lost.
    """
    return service.reset()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

