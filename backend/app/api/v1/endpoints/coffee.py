"""Coffee making endpoints for v1 API."""
from fastapi import APIRouter, Depends, status
from starlette.requests import Request

from app.models import CoffeeType, MessageResponse
from app.services import CoffeeMachineService
from app.dependencies import get_service
from app.rate_limiter import limiter

router = APIRouter()


@router.post(
    "/espresso",
    response_model=MessageResponse,
    tags=["Coffee Making"],
    summary="Make Espresso",
    description="Brew a single espresso using 8g of coffee and 24ml of water. Rate limit: 20/minute",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Espresso successfully brewed",
        },
        409: {
            "description": "Insufficient resources to make espresso",
        },
        429: {
            "description": "Rate limit exceeded",
        }
    }
)
@limiter.limit("20/minute")
async def make_espresso(
    request: Request,
    service: CoffeeMachineService = Depends(get_service)
):
    """
    Make a single espresso.
    
    Requires:
    - 8g of coffee
    - 24ml of water
    
    The machine will automatically deduct resources and increment the coffee counter.
    
    Returns a success message if the espresso is successfully brewed.
    
    Raises InsufficientResourcesException (409) if there aren't enough resources.
    """
    return service.make_coffee(CoffeeType.ESPRESSO)


@router.post(
    "/double-espresso",
    response_model=MessageResponse,
    tags=["Coffee Making"],
    summary="Make Double Espresso",
    description="Brew a double espresso using 16g of coffee and 48ml of water. Rate limit: 20/minute",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Double espresso successfully brewed",
        },
        409: {
            "description": "Insufficient resources to make double espresso",
        },
        429: {
            "description": "Rate limit exceeded",
        }
    }
)
@limiter.limit("20/minute")
async def make_double_espresso(
    request: Request,
    service: CoffeeMachineService = Depends(get_service)
):
    """
    Make a double espresso.
    
    Requires:
    - 16g of coffee
    - 48ml of water
    
    Returns a success message if the double espresso is successfully brewed.
    
    Raises InsufficientResourcesException (409) if there aren't enough resources.
    """
    return service.make_coffee(CoffeeType.DOUBLE_ESPRESSO)


@router.post(
    "/ristretto",
    response_model=MessageResponse,
    tags=["Coffee Making"],
    summary="Make Ristretto",
    description="Brew a ristretto (short espresso) using 8g of coffee and 16ml of water. Rate limit: 20/minute",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Ristretto successfully brewed",
        },
        409: {
            "description": "Insufficient resources to make ristretto",
        },
        429: {
            "description": "Rate limit exceeded",
        }
    }
)
@limiter.limit("20/minute")
async def make_ristretto(
    request: Request,
    service: CoffeeMachineService = Depends(get_service)
):
    """
    Make a ristretto.
    
    A ristretto is a short shot of espresso made with less water.
    It uses the same amount of coffee as an espresso but with less water,
    resulting in a more concentrated, intense flavor.
    
    Requires:
    - 8g of coffee
    - 16ml of water
    
    Returns a success message if the ristretto is successfully brewed.
    
    Raises InsufficientResourcesException (409) if there aren't enough resources.
    """
    return service.make_coffee(CoffeeType.RISTRETTO)


@router.post(
    "/americano",
    response_model=MessageResponse,
    tags=["Coffee Making"],
    summary="Make Americano",
    description="Brew an americano using 16g of coffee and 148ml of water. Rate limit: 20/minute",
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Americano successfully brewed",
        },
        409: {
            "description": "Insufficient resources to make americano",
        },
        429: {
            "description": "Rate limit exceeded",
        }
    }
)
@limiter.limit("20/minute")
async def make_americano(
    request: Request,
    service: CoffeeMachineService = Depends(get_service)
):
    """
    Make an americano.
    
    Requires:
    - 16g of coffee
    - 148ml of water
    
    Returns a success message if the americano is successfully brewed.
    
    Raises InsufficientResourcesException (409) if there aren't enough resources.
    """
    return service.make_coffee(CoffeeType.AMERICANO)

