"""Custom exceptions for the coffee machine."""
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from typing import Dict, Any


class CoffeeMachineException(Exception):
    """Base exception for coffee machine errors."""
    
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
    
    @property
    def status_code(self) -> int:
        """Default HTTP status code."""
        return 500
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary for API responses."""
        return {
            "success": False,
            "message": self.message,
            "error_type": self.__class__.__name__,
            "details": {}
        }


class InsufficientResourcesException(CoffeeMachineException):
    """Raised when there are insufficient resources to make coffee."""
    
    def __init__(self, resource_type: str, needed: float, available: float):
        self.resource_type = resource_type
        self.needed = needed
        self.available = available
        
        if resource_type == "water":
            message = f"Not enough water. Need {needed}ml but only {available}ml available."
        elif resource_type == "coffee":
            message = f"Not enough coffee. Need {needed}g but only {available}g available."
        else:
            message = f"Insufficient {resource_type}. Need {needed} but only {available} available."
        
        super().__init__(message)
    
    @property
    def status_code(self) -> int:
        """HTTP status code for conflict."""
        return 409
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with resource details."""
        base_dict = super().to_dict()
        base_dict["details"] = {
            "resource_type": self.resource_type,
            "needed": self.needed,
            "available": self.available
        }
        return base_dict


class ContainerOverflowException(CoffeeMachineException):
    """Raised when trying to fill a container beyond capacity."""
    
    def __init__(self, container_type: str, capacity: float, attempted_amount: float):
        self.container_type = container_type
        self.capacity = capacity
        self.attempted_amount = attempted_amount
        
        if container_type == "water":
            current = attempted_amount - capacity
            message = f"Cannot fill water container. Capacity is {capacity}ml. Attempted to add {current}ml which would overflow."
        elif container_type == "coffee":
            current = attempted_amount - capacity
            message = f"Cannot fill coffee container. Capacity is {capacity}g. Attempted to add {current}g which would overflow."
        else:
            message = f"Cannot fill {container_type} container. Capacity is {capacity}. Would overflow."
        
        super().__init__(message)
    
    @property
    def status_code(self) -> int:
        """HTTP status code for conflict."""
        return 409
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with container details."""
        base_dict = super().to_dict()
        base_dict["details"] = {
            "container_type": self.container_type,
            "capacity": self.capacity,
            "attempted_amount": self.attempted_amount
        }
        return base_dict


class InvalidAmountException(CoffeeMachineException):
    """Raised when an invalid amount is provided."""
    
    def __init__(self, amount: float, reason: str):
        self.amount = amount
        self.reason = reason
        message = f"Invalid amount: {reason}. Amount: {amount}"
        super().__init__(message)
    
    @property
    def status_code(self) -> int:
        """HTTP status code for bad request."""
        return 400
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary with amount details."""
        base_dict = super().to_dict()
        base_dict["details"] = {
            "amount": self.amount,
            "reason": self.reason
        }
        return base_dict


def exception_handler(request: Request, exc: CoffeeMachineException) -> JSONResponse:
    """Convert custom exceptions to JSON responses."""
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_dict()
    )

