"""Tests for custom exceptions."""
import pytest
from fastapi import HTTPException
from app.exceptions import (
    CoffeeMachineException,
    InsufficientResourcesException,
    ContainerOverflowException,
    InvalidAmountException,
    exception_handler
)


class TestCustomExceptions:
    """Test custom exception classes."""

    def test_coffee_machine_exception_base(self):
        """Test base exception class."""
        exc = CoffeeMachineException("Test message")
        assert str(exc) == "Test message"
        assert exc.status_code == 500

    def test_insufficient_resources_exception(self):
        """Test InsufficientResourcesException."""
        exc = InsufficientResourcesException("water", 100.0, 50.0)
        assert "water" in exc.message.lower()
        assert exc.resource_type == "water"
        assert exc.needed == 100.0
        assert exc.available == 50.0
        assert exc.status_code == 409
        assert "details" in exc.to_dict()

    def test_container_overflow_exception(self):
        """Test ContainerOverflowException."""
        exc = ContainerOverflowException("water", 2000.0, 2500.0)
        assert "water" in exc.message.lower()
        assert exc.container_type == "water"
        assert exc.capacity == 2000.0
        assert exc.attempted_amount == 2500.0
        assert exc.status_code == 409

    def test_invalid_amount_exception(self):
        """Test InvalidAmountException."""
        exc = InvalidAmountException(-10.0, "Cannot be negative")
        assert "negative" in exc.message.lower()
        assert exc.amount == -10.0
        assert exc.reason == "Cannot be negative"
        assert exc.status_code == 400

    def test_exception_handler(self):
        """Test exception handler converts exceptions to HTTP responses."""
        exc = InsufficientResourcesException("water", 100.0, 50.0)
        response = exception_handler(None, exc)
        assert response.status_code == 409
        assert "success" in response.body.decode()


class TestExceptionHandler:
    """Test exception handler integration."""

    def test_exception_handler_with_insufficient_resources(self):
        """Test handler with InsufficientResourcesException."""
        exc = InsufficientResourcesException("coffee", 16.0, 10.0)
        response = exception_handler(None, exc)
        assert response.status_code == 409

