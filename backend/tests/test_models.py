"""Tests for data models."""
import pytest
from datetime import datetime
from pydantic import ValidationError
from app.models import (
    WaterContainer,
    CoffeeContainer,
    MachineState,
    CoffeeType,
    RECIPES,
    FillRequest,
    MessageResponse,
    StatusResponse,
    ErrorResponse
)


class TestWaterContainer:
    """Test WaterContainer model."""

    def test_can_dispense_with_sufficient_water(self):
        """Test that can_dispense returns True when water is sufficient."""
        container = WaterContainer(current_amount=100.0, capacity=2000.0)
        assert container.can_dispense(50.0) is True
        assert container.can_dispense(100.0) is True

    def test_cannot_dispense_with_insufficient_water(self):
        """Test that can_dispense returns False when water is insufficient."""
        container = WaterContainer(current_amount=50.0, capacity=2000.0)
        assert container.can_dispense(100.0) is False

    def test_can_fill_within_capacity(self):
        """Test that can_fill returns True when within capacity."""
        container = WaterContainer(current_amount=100.0, capacity=2000.0)
        assert container.can_fill(500.0) is True
        assert container.can_fill(1900.0) is True

    def test_cannot_fill_beyond_capacity(self):
        """Test that can_fill returns False when beyond capacity."""
        container = WaterContainer(current_amount=100.0, capacity=2000.0)
        assert container.can_fill(2000.0) is False  # Would exceed
        assert container.can_fill(3000.0) is False

    def test_dispense_reduces_amount(self):
        """Test that dispense reduces the current amount."""
        container = WaterContainer(current_amount=100.0, capacity=2000.0)
        container.dispense(50.0)
        assert container.current_amount == 50.0

    def test_fill_increases_amount(self):
        """Test that fill increases the current amount."""
        container = WaterContainer(current_amount=100.0, capacity=2000.0)
        container.fill(500.0)
        assert container.current_amount == 600.0

    def test_cannot_have_negative_amount(self):
        """Test that current_amount cannot be negative."""
        with pytest.raises(ValidationError):
            WaterContainer(current_amount=-10.0, capacity=2000.0)

    def test_cannot_exceed_capacity(self):
        """Test that current_amount cannot exceed capacity."""
        with pytest.raises(ValidationError):
            WaterContainer(current_amount=3000.0, capacity=2000.0)


class TestCoffeeContainer:
    """Test CoffeeContainer model (same as WaterContainer)."""

    def test_can_dispense_with_sufficient_coffee(self):
        """Test coffee container dispense logic."""
        container = CoffeeContainer(current_amount=50.0, capacity=500.0)
        assert container.can_dispense(30.0) is True
        assert container.can_dispense(70.0) is False

    def test_cannot_fill_beyond_capacity(self):
        """Test coffee container fill logic."""
        container = CoffeeContainer(current_amount=100.0, capacity=500.0)
        assert container.can_fill(400.0) is True
        assert container.can_fill(500.0) is False


class TestMachineState:
    """Test MachineState model."""

    def test_initialization(self):
        """Test that MachineState can be initialized."""
        water = WaterContainer(current_amount=100.0, capacity=2000.0)
        coffee = CoffeeContainer(current_amount=50.0, capacity=500.0)
        state = MachineState(
            water_container=water,
            coffee_container=coffee,
            total_coffees_made=10,
            last_updated=datetime.now()
        )
        assert state.total_coffees_made == 10
        assert state.water_container.current_amount == 100.0
        assert state.coffee_container.current_amount == 50.0

    def test_serialization(self):
        """Test that MachineState can be serialized to dict."""
        water = WaterContainer(current_amount=100.0, capacity=2000.0)
        coffee = CoffeeContainer(current_amount=50.0, capacity=500.0)
        state = MachineState(
            water_container=water,
            coffee_container=coffee,
            total_coffees_made=10,
            last_updated=datetime.now()
        )
        data = state.model_dump()
        assert isinstance(data, dict)
        assert data["total_coffees_made"] == 10


class TestCoffeeType:
    """Test CoffeeType enum."""

    def test_coffee_types_exist(self):
        """Test that all coffee types exist."""
        assert CoffeeType.ESPRESSO == "espresso"
        assert CoffeeType.DOUBLE_ESPRESSO == "double_espresso"
        assert CoffeeType.AMERICANO == "americano"

    def test_recipes_exist(self):
        """Test that recipes exist for all coffee types."""
        assert CoffeeType.ESPRESSO in RECIPES
        assert CoffeeType.DOUBLE_ESPRESSO in RECIPES
        assert CoffeeType.AMERICANO in RECIPES

    def test_espresso_recipe(self):
        """Test espresso recipe values."""
        recipe = RECIPES[CoffeeType.ESPRESSO]
        assert recipe["coffee"] == 8
        assert recipe["water"] == 24

    def test_double_espresso_recipe(self):
        """Test double espresso recipe values."""
        recipe = RECIPES[CoffeeType.DOUBLE_ESPRESSO]
        assert recipe["coffee"] == 16
        assert recipe["water"] == 48

    def test_americano_recipe(self):
        """Test americano recipe values."""
        recipe = RECIPES[CoffeeType.AMERICANO]
        assert recipe["coffee"] == 16
        assert recipe["water"] == 148


class TestRequestModels:
    """Test request/response models."""

    def test_fill_request_validation(self):
        """Test FillRequest validation."""
        # Valid request
        request = FillRequest(amount=100.0)
        assert request.amount == 100.0

        # Invalid: negative amount
        with pytest.raises(ValidationError):
            FillRequest(amount=-10.0)

        # Invalid: zero amount
        with pytest.raises(ValidationError):
            FillRequest(amount=0.0)

    def test_message_response(self):
        """Test MessageResponse model."""
        response = MessageResponse(success=True, message="Test message")
        assert response.success is True
        assert response.message == "Test message"

    def test_status_response(self):
        """Test StatusResponse model."""
        response = StatusResponse(success=True, data={"key": "value"})
        assert response.success is True
        assert response.data == {"key": "value"}

    def test_error_response(self):
        """Test ErrorResponse model."""
        response = ErrorResponse(
            success=False,
            message="Error message",
            error_type="TestError",
            details={"key": "value"}
        )
        assert response.success is False
        assert response.message == "Error message"
        assert response.error_type == "TestError"
        assert response.details == {"key": "value"}

