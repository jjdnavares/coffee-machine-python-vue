"""Machine management endpoints for v1 API."""
from fastapi import APIRouter, Depends, status
from starlette.requests import Request
from typing import Optional

from app.models import FillRequest, MessageResponse, StatusResponse
from app.services import CoffeeMachineService
from app.dependencies import get_service
from app.config import get_settings
from app.rate_limiter import limiter

router = APIRouter()


@router.get(
    "/status",
    response_model=StatusResponse,
    tags=["Machine Management"],
    summary="Get Machine Status",
    description="Retrieve the current status of the coffee machine including container levels and statistics. Rate limit: 60/minute",
    responses={
        200: {
            "description": "Machine status retrieved successfully",
        },
        429: {
            "description": "Rate limit exceeded",
        }
    }
)
@limiter.limit("60/minute")
async def get_status(
    request: Request,
    service: CoffeeMachineService = Depends(get_service)
):
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


@router.post(
    "/fill/water",
    response_model=MessageResponse,
    tags=["Machine Management"],
    summary="Fill Water Container",
    description="Add water to the water container. The amount is added to the current level. Rate limit: 30/minute",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Water successfully added to container",
        },
        409: {
            "description": "Container overflow - amount exceeds capacity",
        },
        422: {
            "description": "Invalid amount (must be positive)",
        },
        429: {
            "description": "Rate limit exceeded",
        }
    }
)
@limiter.limit("30/minute")
async def fill_water(
    request: Request,
    fill_request: FillRequest,
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
    return service.fill_water(fill_request.amount)


@router.post(
    "/fill/coffee",
    response_model=MessageResponse,
    tags=["Machine Management"],
    summary="Fill Coffee Container",
    description="Add coffee to the coffee container. The amount is added to the current level. Rate limit: 30/minute",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Coffee successfully added to container",
        },
        409: {
            "description": "Container overflow - amount exceeds capacity",
        },
        422: {
            "description": "Invalid amount (must be positive)",
        },
        429: {
            "description": "Rate limit exceeded",
        }
    }
)
@limiter.limit("30/minute")
async def fill_coffee(
    request: Request,
    fill_request: FillRequest,
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
    return service.fill_coffee(fill_request.amount)


@router.post(
    "/reset",
    response_model=MessageResponse,
    tags=["Machine Management"],
    summary="Reset Machine",
    description="Reset the coffee machine to its initial empty state.",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Machine successfully reset",
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


@router.get("/config/containers")
async def get_container_config():
    """
    Get current container configuration.
    
    Returns:
        - Default capacities configured
        - Custom capacities (if set via environment variables)
        - Effective capacities (custom or default)
    """
    settings = get_settings()
    return {
        "default_water_capacity": settings.water_capacity,
        "default_coffee_capacity": settings.coffee_capacity,
        "custom_water_capacity": settings.custom_water_capacity,
        "custom_coffee_capacity": settings.custom_coffee_capacity,
        "effective_water_capacity": settings.effective_water_capacity,
        "effective_coffee_capacity": settings.effective_coffee_capacity,
    }

