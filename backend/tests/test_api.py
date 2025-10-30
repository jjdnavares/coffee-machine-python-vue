"""Tests for API endpoints."""
import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from app.main import app
from app.models import MachineState, WaterContainer, CoffeeContainer
from app.storage import StorageInterface
from app.services import CoffeeMachineService


class MockStorageForAPI(StorageInterface):
    """Mock storage for API testing."""
    
    def __init__(self):
        self.state = MachineState(
            water_container=WaterContainer(current_amount=1000.0, capacity=2000.0),
            coffee_container=CoffeeContainer(current_amount=500.0, capacity=500.0),
            total_coffees_made=0,
            last_updated=datetime.now()
        )
    
    def load_state(self) -> MachineState:
        return self.state
    
    def save_state(self, state: MachineState) -> None:
        self.state = state


@pytest.fixture
def client():
    """Create test client with dependency override."""
    from app.main import get_service
    
    # Create mock storage and service
    mock_storage = MockStorageForAPI()
    mock_service = CoffeeMachineService(mock_storage)
    
    # Override dependency
    app.dependency_overrides[get_service] = lambda: mock_service
    
    yield TestClient(app)
    
    # Clean up
    app.dependency_overrides.clear()


class TestHealthEndpoint:
    """Test health check endpoint."""
    
    def test_health_check(self, client):
        """Test health endpoint returns healthy status."""
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data


class TestStatusEndpoint:
    """Test status endpoint."""
    
    def test_get_status(self, client):
        """Test getting machine status."""
        response = client.get("/api/status")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "data" in data
        assert "water_level" in data["data"]
        assert "coffee_level" in data["data"]
        assert "total_coffees_made" in data["data"]


class TestCoffeeEndpoints:
    """Test coffee making endpoints."""
    
    def test_make_espresso(self, client):
        """Test making espresso."""
        response = client.post("/api/coffee/espresso")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "espresso" in data["message"].lower()
    
    def test_make_double_espresso(self, client):
        """Test making double espresso."""
        response = client.post("/api/coffee/double-espresso")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
    
    def test_make_americano(self, client):
        """Test making americano."""
        response = client.post("/api/coffee/americano")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
    
    def test_make_espresso_with_insufficient_resources(self, client):
        """Test making espresso with insufficient resources."""
        # Override to have no water
        from app.main import get_service
        mock_storage = MockStorageForAPI()
        mock_storage.state.water_container.current_amount = 10.0
        mock_service = CoffeeMachineService(mock_storage)
        app.dependency_overrides[get_service] = lambda: mock_service
        
        response = client.post("/api/coffee/espresso")
        assert response.status_code == 409
        data = response.json()
        assert data["success"] is False
        assert "water" in data["message"].lower()
        
        app.dependency_overrides.clear()


class TestFillEndpoints:
    """Test fill endpoints."""
    
    def test_fill_water(self, client):
        """Test filling water container."""
        response = client.post("/api/fill/water", json={"amount": 500.0})
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "water" in data["message"].lower()
    
    def test_fill_coffee(self, client):
        """Test filling coffee container."""
        # Need to reduce coffee first
        from app.main import get_service
        mock_storage = MockStorageForAPI()
        mock_storage.state.coffee_container.current_amount = 300.0
        mock_service = CoffeeMachineService(mock_storage)
        app.dependency_overrides[get_service] = lambda: mock_service
        
        response = client.post("/api/fill/coffee", json={"amount": 100.0})
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "coffee" in data["message"].lower()
        
        app.dependency_overrides.clear()
    
    def test_fill_water_overflow(self, client):
        """Test water fill overflow."""
        from app.main import get_service
        mock_storage = MockStorageForAPI()
        mock_storage.state.water_container.current_amount = 1800.0
        mock_service = CoffeeMachineService(mock_storage)
        app.dependency_overrides[get_service] = lambda: mock_service
        
        response = client.post("/api/fill/water", json={"amount": 500.0})
        assert response.status_code == 409
        data = response.json()
        assert data["success"] is False
        
        app.dependency_overrides.clear()
    
    def test_fill_invalid_amount(self, client):
        """Test fill with invalid (negative) amount."""
        response = client.post("/api/fill/water", json={"amount": -10.0})
        assert response.status_code == 422  # Validation error


class TestResetEndpoint:
    """Test reset endpoint."""
    
    def test_reset(self, client):
        """Test resetting machine."""
        response = client.post("/api/reset")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

