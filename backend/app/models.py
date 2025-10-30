"""Data models for the coffee machine."""
from datetime import datetime
from enum import Enum
from typing import Dict
from pydantic import BaseModel, Field, field_validator
from app.validators import ValidationHelpers


class CoffeeType(str, Enum):
    """Enumeration of available coffee types."""
    ESPRESSO = "espresso"
    DOUBLE_ESPRESSO = "double_espresso"
    RISTRETTO = "ristretto"
    AMERICANO = "americano"


# Coffee recipes in grams and milliliters
RECIPES: Dict[CoffeeType, Dict[str, float]] = {
    CoffeeType.ESPRESSO: {"coffee": 8.0, "water": 24.0},
    CoffeeType.DOUBLE_ESPRESSO: {"coffee": 16.0, "water": 48.0},
    CoffeeType.RISTRETTO: {"coffee": 8.0, "water": 16.0},  # Short shot with less water
    CoffeeType.AMERICANO: {"coffee": 16.0, "water": 148.0},
}


class WaterContainer(BaseModel):
    """Container for water with capacity management."""
    capacity: float = 2000.0  # ml
    current_amount: float = 0.0

    @field_validator("current_amount")
    @classmethod
    def validate_current_amount(cls, v: float, info) -> float:
        """Validate that current_amount is within bounds."""
        capacity = info.data.get("capacity", 2000.0)
        if v < 0:
            raise ValueError("current_amount cannot be negative")
        if v > capacity:
            raise ValueError(f"current_amount ({v}) cannot exceed capacity ({capacity})")
        return v

    def can_dispense(self, amount: float) -> bool:
        """Check if container can dispense the requested amount."""
        return self.current_amount >= amount

    def can_fill(self, amount: float) -> bool:
        """Check if container can be filled by the requested amount."""
        return (self.current_amount + amount) <= self.capacity

    def dispense(self, amount: float) -> None:
        """Dispense water from container."""
        if not self.can_dispense(amount):
            raise ValueError(f"Cannot dispense {amount}ml, only {self.current_amount}ml available")
        self.current_amount -= amount

    def fill(self, amount: float) -> None:
        """Fill container with water."""
        if not self.can_fill(amount):
            raise ValueError(f"Cannot add {amount}ml, would exceed capacity")
        self.current_amount += amount


class CoffeeContainer(BaseModel):
    """Container for coffee with capacity management."""
    capacity: float = 500.0  # grams
    current_amount: float = 0.0

    @field_validator("current_amount")
    @classmethod
    def validate_current_amount(cls, v: float, info) -> float:
        """Validate that current_amount is within bounds."""
        capacity = info.data.get("capacity", 500.0)
        if v < 0:
            raise ValueError("current_amount cannot be negative")
        if v > capacity:
            raise ValueError(f"current_amount ({v}) cannot exceed capacity ({capacity})")
        return v

    def can_dispense(self, amount: float) -> bool:
        """Check if container can dispense the requested amount."""
        return self.current_amount >= amount

    def can_fill(self, amount: float) -> bool:
        """Check if container can be filled by the requested amount."""
        return (self.current_amount + amount) <= self.capacity

    def dispense(self, amount: float) -> None:
        """Dispense coffee from container."""
        if not self.can_dispense(amount):
            raise ValueError(f"Cannot dispense {amount}g, only {self.current_amount}g available")
        self.current_amount -= amount

    def fill(self, amount: float) -> None:
        """Fill container with coffee."""
        if not self.can_fill(amount):
            raise ValueError(f"Cannot add {amount}g, would exceed capacity")
        self.current_amount += amount


class MachineState(BaseModel):
    """Machine state including containers and statistics."""
    water_container: WaterContainer
    coffee_container: CoffeeContainer
    total_coffees_made: int = 0
    last_updated: datetime = Field(default_factory=datetime.now)


# Request/Response Models
class FillRequest(BaseModel):
    """Request model for filling containers."""
    amount: float = Field(gt=0, description="Amount to fill (must be positive)")

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, v: float) -> float:
        """Validate that amount is positive and reasonable."""
        # Use ValidationHelpers for consistent validation
        ValidationHelpers.validate_positive_number(v, "amount")
        # Max 10L water or 2kg coffee in single fill
        ValidationHelpers.validate_reasonable_amount(v, 10000, "amount")
        return v


class MessageResponse(BaseModel):
    """Response model for operations returning a message."""
    success: bool
    message: str


class StatusResponse(BaseModel):
    """Response model for status requests."""
    success: bool
    data: dict


class ErrorResponse(BaseModel):
    """Response model for errors."""
    success: bool = False
    message: str
    error_type: str
    details: dict = {}

