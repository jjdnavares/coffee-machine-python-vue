"""Business logic service for coffee machine operations."""
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


class CoffeeMachineService:
    """Service for managing coffee machine operations."""
    
    def __init__(self, storage: StorageInterface):
        """Initialize service with storage backend."""
        self.storage = storage
        self.state = self.storage.load_state()
    
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
        recipe = RECIPES.get(coffee_type)
        if not recipe:
            raise ValueError(f"Unknown coffee type: {coffee_type}")
        
        water_needed = recipe["water"]
        coffee_needed = recipe["coffee"]
        
        # Check water availability
        if not self.state.water_container.can_dispense(water_needed):
            raise InsufficientResourcesException(
                "water",
                water_needed,
                self.state.water_container.current_amount
            )
        
        # Check coffee availability
        if not self.state.coffee_container.can_dispense(coffee_needed):
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
        
        # Persist state
        self.storage.save_state(self.state)
        
        # Return success message
        messages = {
            CoffeeType.ESPRESSO: "Espresso ready!",
            CoffeeType.DOUBLE_ESPRESSO: "Double espresso ready!",
            CoffeeType.AMERICANO: "Americano ready!",
        }
        
        return {
            "success": True,
            "message": messages.get(coffee_type, "Coffee ready!")
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
        if amount <= 0:
            raise InvalidAmountException(amount, "Amount must be greater than 0")
        
        if not self.state.water_container.can_fill(amount):
            raise ContainerOverflowException(
                "water",
                self.state.water_container.capacity,
                self.state.water_container.current_amount + amount
            )
        
        self.state.water_container.fill(amount)
        self.state.last_updated = datetime.now()
        
        # Persist state
        self.storage.save_state(self.state)
        
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
        if amount <= 0:
            raise InvalidAmountException(amount, "Amount must be greater than 0")
        
        if not self.state.coffee_container.can_fill(amount):
            raise ContainerOverflowException(
                "coffee",
                self.state.coffee_container.capacity,
                self.state.coffee_container.current_amount + amount
            )
        
        self.state.coffee_container.fill(amount)
        self.state.last_updated = datetime.now()
        
        # Persist state
        self.storage.save_state(self.state)
        
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
        settings = get_settings()
        self.state = MachineState(
            water_container=WaterContainer(capacity=settings.water_capacity),
            coffee_container=CoffeeContainer(capacity=settings.coffee_capacity),
            total_coffees_made=0,
            last_updated=datetime.now()
        )
        
        # Persist state
        self.storage.save_state(self.state)
        
        return {
            "success": True,
            "message": "Machine reset to empty state."
        }

