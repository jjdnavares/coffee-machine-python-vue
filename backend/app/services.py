"""Business logic service for coffee machine operations."""
import asyncio
from datetime import datetime
from app.models import (
    MachineState,
    CoffeeType,
    RECIPES,
    WaterContainer,
    CoffeeContainer
)
from app.exceptions import (
    InsufficientResourcesException,
    ContainerOverflowException,
    InvalidAmountException
)
from app.storage import StorageInterface
from app.config import get_settings
from app.logger import logger
from app.websocket_manager import manager


class CoffeeMachineService:
    """Service for managing coffee machine operations."""
    
    def __init__(self, storage: StorageInterface):
        """Initialize service with storage backend."""
        self.storage = storage
        self.state = self.storage.load_state()
        logger.info("service_initialized", storage_type=type(storage).__name__)
    
    def make_coffee(self, coffee_type: CoffeeType) -> dict:
        """
        Make coffee of the specified type.
        
        Args:
            coffee_type: Type of coffee to make
            
        Returns:
            Dictionary with success status and message
            
        Raises:
            InsufficientResourcesException: If resources are insufficient
        """
        logger.info(f"Making {coffee_type.value}", coffee_type=coffee_type.value)
        
        recipe = RECIPES.get(coffee_type)
        if not recipe:
            logger.error("Unknown coffee type", coffee_type=coffee_type.value)
            raise ValueError(f"Unknown coffee type: {coffee_type}")
        
        water_needed = recipe["water"]
        coffee_needed = recipe["coffee"]
        
        # Check water availability
        if not self.state.water_container.can_dispense(water_needed):
            logger.warning(
                "Insufficient water",
                coffee_type=coffee_type.value,
                needed=water_needed,
                available=self.state.water_container.current_amount
            )
            raise InsufficientResourcesException(
                "water",
                water_needed,
                self.state.water_container.current_amount
            )
        
        # Check coffee availability
        if not self.state.coffee_container.can_dispense(coffee_needed):
            logger.warning(
                "Insufficient coffee",
                coffee_type=coffee_type.value,
                needed=coffee_needed,
                available=self.state.coffee_container.current_amount
            )
            raise InsufficientResourcesException(
                "coffee",
                coffee_needed,
                self.state.coffee_container.current_amount
            )
        
        # Dispense resources
        self.state.water_container.dispense(water_needed)
        self.state.coffee_container.dispense(coffee_needed)
        
        # Increment counter
        self.state.total_coffees_made += 1
        self.state.last_updated = datetime.now()
        
        # Log success
        logger.info(
            "Coffee made successfully",
            coffee_type=coffee_type.value,
            total_coffees=self.state.total_coffees_made,
            water_remaining=self.state.water_container.current_amount,
            coffee_remaining=self.state.coffee_container.current_amount
        )
        
        # Broadcast to WebSocket clients
        try:
            asyncio.create_task(manager.broadcast_coffee_made(
                coffee_type.value,
                {"coffee": coffee_needed, "water": water_needed}
            ))
            # Broadcast updated status
            status = self.get_status()
            asyncio.create_task(manager.broadcast_status_update(status["data"]))
        except Exception as e:
            logger.warning("Failed to broadcast WebSocket message", error=str(e))
        
        # Check if resources are low
        water_percentage = (self.state.water_container.current_amount / 
                           self.state.water_container.capacity) * 100
        coffee_percentage = (self.state.coffee_container.current_amount / 
                            self.state.coffee_container.capacity) * 100
        
        if water_percentage < 20:
            logger.warning("Water level low", percentage=round(water_percentage, 1))
        if coffee_percentage < 20:
            logger.warning("Coffee level low", percentage=round(coffee_percentage, 1))
        
        # Persist state
        self.storage.save_state(self.state)
        
        # Return success message
        messages = {
            CoffeeType.ESPRESSO: "Espresso ready! ☕",
            CoffeeType.DOUBLE_ESPRESSO: "Double espresso ready! ☕",
            CoffeeType.RISTRETTO: "Ristretto ready! ☕",
            CoffeeType.AMERICANO: "Americano ready! ☕",
        }
        
        return {
            "success": True,
            "message": messages.get(coffee_type, "Coffee ready! ☕")
        }
    
    def get_status(self) -> dict:
        """
        Get current machine status.
        
        Returns:
            Dictionary with success status and status data
        """
        water_percentage = (
            (self.state.water_container.current_amount / self.state.water_container.capacity) * 100
            if self.state.water_container.capacity > 0 else 0.0
        )
        coffee_percentage = (
            (self.state.coffee_container.current_amount / self.state.coffee_container.capacity) * 100
            if self.state.coffee_container.capacity > 0 else 0.0
        )
        
        return {
            "success": True,
            "data": {
                "water_level": self.state.water_container.current_amount,
                "water_capacity": self.state.water_container.capacity,
                "water_percentage": round(water_percentage, 2),
                "coffee_level": self.state.coffee_container.current_amount,
                "coffee_capacity": self.state.coffee_container.capacity,
                "coffee_percentage": round(coffee_percentage, 2),
                "total_coffees_made": self.state.total_coffees_made,
                "last_updated": self.state.last_updated.isoformat()
            }
        }
    
    def fill_water(self, amount: float) -> dict:
        """
        Fill water container.
        
        Args:
            amount: Amount of water to add (ml)
            
        Returns:
            Dictionary with success status and message
            
        Raises:
            InvalidAmountException: If amount is invalid
            ContainerOverflowException: If fill would exceed capacity
        """
        logger.info("Filling water", amount=amount)
        
        if amount <= 0:
            logger.warning("Invalid water amount", amount=amount)
            raise InvalidAmountException(amount, "Amount must be greater than 0")
        
        if not self.state.water_container.can_fill(amount):
            logger.warning(
                "Water fill would overflow",
                amount=amount,
                current=self.state.water_container.current_amount,
                capacity=self.state.water_container.capacity
            )
            raise ContainerOverflowException(
                "water",
                self.state.water_container.capacity,
                self.state.water_container.current_amount + amount
            )
        
        self.state.water_container.fill(amount)
        self.state.last_updated = datetime.now()
        
        # Persist state
        self.storage.save_state(self.state)
        
        logger.info(
            "Water filled successfully",
            amount=amount,
            new_total=self.state.water_container.current_amount
        )
        
        # Broadcast status update to WebSocket clients
        try:
            status = self.get_status()
            asyncio.create_task(manager.broadcast_status_update(status["data"]))
        except Exception as e:
            logger.warning("Failed to broadcast WebSocket message", error=str(e))
        
        return {
            "success": True,
            "message": f"Added {amount}ml of water. Container now at {self.state.water_container.current_amount}ml/{self.state.water_container.capacity}ml"
        }
    
    def fill_coffee(self, amount: float) -> dict:
        """
        Fill coffee container.
        
        Args:
            amount: Amount of coffee to add (grams)
            
        Returns:
            Dictionary with success status and message
            
        Raises:
            InvalidAmountException: If amount is invalid
            ContainerOverflowException: If fill would exceed capacity
        """
        logger.info("Filling coffee", amount=amount)
        
        if amount <= 0:
            logger.warning("Invalid coffee amount", amount=amount)
            raise InvalidAmountException(amount, "Amount must be greater than 0")
        
        if not self.state.coffee_container.can_fill(amount):
            logger.warning(
                "Coffee fill would overflow",
                amount=amount,
                current=self.state.coffee_container.current_amount,
                capacity=self.state.coffee_container.capacity
            )
            raise ContainerOverflowException(
                "coffee",
                self.state.coffee_container.capacity,
                self.state.coffee_container.current_amount + amount
            )
        
        self.state.coffee_container.fill(amount)
        self.state.last_updated = datetime.now()
        
        # Persist state
        self.storage.save_state(self.state)
        
        logger.info(
            "Coffee filled successfully",
            amount=amount,
            new_total=self.state.coffee_container.current_amount
        )
        
        # Broadcast status update to WebSocket clients
        try:
            status = self.get_status()
            asyncio.create_task(manager.broadcast_status_update(status["data"]))
        except Exception as e:
            logger.warning("Failed to broadcast WebSocket message", error=str(e))
        
        return {
            "success": True,
            "message": f"Added {amount}g of coffee. Container now at {self.state.coffee_container.current_amount}g/{self.state.coffee_container.capacity}g"
        }
    
    def reset(self) -> dict:
        """
        Reset machine to empty state.
        
        Returns:
            Dictionary with success status and message
        """
        logger.info("Resetting machine")
        
        settings = get_settings()
        self.state = MachineState(
            water_container=WaterContainer(capacity=settings.water_capacity),
            coffee_container=CoffeeContainer(capacity=settings.coffee_capacity),
            total_coffees_made=0,
            last_updated=datetime.now()
        )
        
        # Persist state
        self.storage.save_state(self.state)
        
        logger.info("Machine reset successfully")
        
        return {
            "success": True,
            "message": "Machine reset to empty state."
        }

