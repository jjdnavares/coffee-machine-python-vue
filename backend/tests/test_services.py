"""Tests for business logic service."""
import pytest
from datetime import datetime
from app.services import CoffeeMachineService
from app.models import MachineState, WaterContainer, CoffeeContainer, CoffeeType, RECIPES
from app.exceptions import InsufficientResourcesException, ContainerOverflowException
from app.storage import StorageInterface


class MockStorage(StorageInterface):
    """Mock storage for testing."""
    
    def __init__(self):
        self.state = MachineState(
            water_container=WaterContainer(current_amount=1000.0, capacity=2000.0),
            coffee_container=CoffeeContainer(current_amount=500.0, capacity=500.0),
            total_coffees_made=0,
            last_updated=datetime.now()
        )
        self.save_count = 0
    
    def load_state(self) -> MachineState:
        return self.state
    
    def save_state(self, state: MachineState) -> None:
        self.state = state
        self.save_count += 1


class TestCoffeeMachineService:
    """Test CoffeeMachineService business logic."""
    
    @pytest.fixture
    def service(self):
        """Create service with mock storage."""
        storage = MockStorage()
        return CoffeeMachineService(storage)
    
    def test_make_espresso_success(self, service):
        """Test successful espresso making."""
        initial_water = service.state.water_container.current_amount
        initial_coffee = service.state.coffee_container.current_amount
        initial_count = service.state.total_coffees_made
        
        result = service.make_coffee(CoffeeType.ESPRESSO)
        
        assert result["success"] is True
        assert "espresso" in result["message"].lower()
        assert service.state.water_container.current_amount == initial_water - RECIPES[CoffeeType.ESPRESSO]["water"]
        assert service.state.coffee_container.current_amount == initial_coffee - RECIPES[CoffeeType.ESPRESSO]["coffee"]
        assert service.state.total_coffees_made == initial_count + 1
    
    def test_make_espresso_insufficient_water(self, service):
        """Test espresso making with insufficient water."""
        service.state.water_container.current_amount = 10.0
        
        with pytest.raises(InsufficientResourcesException) as exc_info:
            service.make_coffee(CoffeeType.ESPRESSO)
        
        assert exc_info.value.resource_type == "water"
        assert exc_info.value.needed == RECIPES[CoffeeType.ESPRESSO]["water"]
        assert exc_info.value.available == 10.0
    
    def test_make_espresso_insufficient_coffee(self, service):
        """Test espresso making with insufficient coffee."""
        service.state.coffee_container.current_amount = 5.0
        
        with pytest.raises(InsufficientResourcesException) as exc_info:
            service.make_coffee(CoffeeType.ESPRESSO)
        
        assert exc_info.value.resource_type == "coffee"
        assert exc_info.value.needed == RECIPES[CoffeeType.ESPRESSO]["coffee"]
        assert exc_info.value.available == 5.0
    
    def test_make_double_espresso_success(self, service):
        """Test successful double espresso making."""
        initial_water = service.state.water_container.current_amount
        initial_coffee = service.state.coffee_container.current_amount
        
        result = service.make_coffee(CoffeeType.DOUBLE_ESPRESSO)
        
        assert result["success"] is True
        assert service.state.water_container.current_amount == initial_water - RECIPES[CoffeeType.DOUBLE_ESPRESSO]["water"]
        assert service.state.coffee_container.current_amount == initial_coffee - RECIPES[CoffeeType.DOUBLE_ESPRESSO]["coffee"]
    
    def test_make_americano_success(self, service):
        """Test successful americano making."""
        initial_water = service.state.water_container.current_amount
        initial_coffee = service.state.coffee_container.current_amount
        
        result = service.make_coffee(CoffeeType.AMERICANO)
        
        assert result["success"] is True
        assert service.state.water_container.current_amount == initial_water - RECIPES[CoffeeType.AMERICANO]["water"]
        assert service.state.coffee_container.current_amount == initial_coffee - RECIPES[CoffeeType.AMERICANO]["coffee"]
    
    def test_get_status(self, service):
        """Test getting machine status."""
        status = service.get_status()
        
        assert status["success"] is True
        assert "data" in status
        assert "water_level" in status["data"]
        assert "coffee_level" in status["data"]
        assert "total_coffees_made" in status["data"]
    
    def test_fill_water_success(self, service):
        """Test successful water fill."""
        initial_amount = service.state.water_container.current_amount
        
        result = service.fill_water(500.0)
        
        assert result["success"] is True
        assert service.state.water_container.current_amount == initial_amount + 500.0
    
    def test_fill_water_overflow(self, service):
        """Test water fill overflow."""
        service.state.water_container.current_amount = 1800.0
        
        with pytest.raises(ContainerOverflowException) as exc_info:
            service.fill_water(500.0)  # Would exceed 2000ml capacity
        
        assert exc_info.value.container_type == "water"
        assert exc_info.value.capacity == 2000.0
    
    def test_fill_coffee_success(self, service):
        """Test successful coffee fill."""
        # Set coffee to a lower amount so we can fill
        service.state.coffee_container.current_amount = 300.0
        initial_amount = service.state.coffee_container.current_amount
        
        result = service.fill_coffee(100.0)
        
        assert result["success"] is True
        assert service.state.coffee_container.current_amount == initial_amount + 100.0
    
    def test_fill_coffee_overflow(self, service):
        """Test coffee fill overflow."""
        service.state.coffee_container.current_amount = 450.0
        
        with pytest.raises(ContainerOverflowException) as exc_info:
            service.fill_coffee(100.0)  # Would exceed 500g capacity
        
        assert exc_info.value.container_type == "coffee"
        assert exc_info.value.capacity == 500.0
    
    def test_reset(self, service):
        """Test resetting machine state."""
        # Make some changes
        service.state.water_container.current_amount = 500.0
        service.state.coffee_container.current_amount = 200.0
        service.state.total_coffees_made = 10
        
        result = service.reset()
        
        assert result["success"] is True
        assert service.state.water_container.current_amount == 0.0
        assert service.state.coffee_container.current_amount == 0.0
        assert service.state.total_coffees_made == 0
    
    def test_state_is_saved_after_operations(self, service):
        """Test that state is saved after each operation."""
        storage = MockStorage()
        service_with_storage = CoffeeMachineService(storage)
        
        initial_save_count = storage.save_count
        service_with_storage.make_coffee(CoffeeType.ESPRESSO)
        assert storage.save_count == initial_save_count + 1
        
        service_with_storage.fill_water(100.0)
        assert storage.save_count == initial_save_count + 2

