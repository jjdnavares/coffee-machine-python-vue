"""Storage layer for persisting machine state."""
import json
import os
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional
from app.models import MachineState, WaterContainer, CoffeeContainer
from app.config import get_settings


class StorageInterface(ABC):
    """Abstract base class for storage implementations."""
    
    @abstractmethod
    def load_state(self) -> MachineState:
        """Load machine state from storage."""
        pass
    
    @abstractmethod
    def save_state(self, state: MachineState) -> None:
        """Save machine state to storage."""
        pass


class JSONStorage(StorageInterface):
    """JSON file-based storage implementation."""
    
    def __init__(self, file_path: str):
        """Initialize JSON storage with file path."""
        self.file_path = file_path
    
    def load_state(self) -> MachineState:
        """Load state from JSON file. Returns new state if file doesn't exist or is invalid."""
        if not os.path.exists(self.file_path):
            return self._create_default_state()
        
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Deserialize containers
            water_container = WaterContainer(**data.get("water_container", {}))
            coffee_container = CoffeeContainer(**data.get("coffee_container", {}))
            
            # Handle datetime deserialization
            last_updated_str = data.get("last_updated")
            if isinstance(last_updated_str, str):
                last_updated = datetime.fromisoformat(last_updated_str)
            else:
                last_updated = datetime.now()
            
            return MachineState(
                water_container=water_container,
                coffee_container=coffee_container,
                total_coffees_made=data.get("total_coffees_made", 0),
                last_updated=last_updated
            )
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            # Log error and return default state
            print(f"Error loading state from {self.file_path}: {e}. Creating new state.")
            return self._create_default_state()
    
    def save_state(self, state: MachineState) -> None:
        """Save state to JSON file atomically."""
        # Create parent directories if needed
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        
        # Prepare data for serialization
        data = {
            "water_container": {
                "capacity": state.water_container.capacity,
                "current_amount": state.water_container.current_amount
            },
            "coffee_container": {
                "capacity": state.coffee_container.capacity,
                "current_amount": state.coffee_container.current_amount
            },
            "total_coffees_made": state.total_coffees_made,
            "last_updated": state.last_updated.isoformat()
        }
        
        # Atomic write: write to temp file, then rename
        temp_path = f"{self.file_path}.tmp"
        try:
            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            # Rename (atomic on most filesystems)
            os.replace(temp_path, self.file_path)
        except Exception as e:
            # Clean up temp file on error
            if os.path.exists(temp_path):
                os.unlink(temp_path)
            raise IOError(f"Failed to save state to {self.file_path}: {e}") from e
    
    def _create_default_state(self) -> MachineState:
        """Create a new default machine state."""
        settings = get_settings()
        return MachineState(
            water_container=WaterContainer(capacity=settings.water_capacity),
            coffee_container=CoffeeContainer(capacity=settings.coffee_capacity),
            total_coffees_made=0,
            last_updated=datetime.now()
        )


def get_storage(storage_type: str, **kwargs) -> StorageInterface:
    """Factory function to create storage instances."""
    if storage_type == "json":
        file_path = kwargs.get("file_path")
        if not file_path:
            settings = get_settings()
            file_path = settings.data_path
        return JSONStorage(file_path)
    else:
        raise ValueError(f"Unsupported storage type: {storage_type}")

