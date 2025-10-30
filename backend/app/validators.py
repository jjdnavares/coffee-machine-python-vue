"""Input validation and sanitization utilities."""
import re
from typing import Any


class ValidationHelpers:
    """Helper class for input validation and sanitization."""
    
    @staticmethod
    def validate_positive_number(value: float, field_name: str = "value") -> float:
        """
        Ensure number is positive.
        
        Args:
            value: Number to validate
            field_name: Name of the field for error messages
            
        Returns:
            Validated positive number
            
        Raises:
            ValueError: If value is not positive
        """
        if value <= 0:
            raise ValueError(f"{field_name} must be positive, got {value}")
        return value
    
    @staticmethod
    def validate_reasonable_amount(
        value: float,
        max_value: float,
        field_name: str = "value"
    ) -> float:
        """
        Ensure amount is reasonable (not too large).
        
        Args:
            value: Amount to validate
            max_value: Maximum allowed value
            field_name: Name of the field for error messages
            
        Returns:
            Validated amount
            
        Raises:
            ValueError: If value exceeds maximum
        """
        if value > max_value:
            raise ValueError(
                f"{field_name} too large. Maximum: {max_value}, got: {value}"
            )
        return value
    
    @staticmethod
    def sanitize_string(value: str, max_length: int = 1000) -> str:
        """
        Remove potentially dangerous characters from string.
        
        Args:
            value: String to sanitize
            max_length: Maximum allowed length
            
        Returns:
            Sanitized string
            
        Raises:
            ValueError: If string is too long
        """
        if len(value) > max_length:
            raise ValueError(f"String too long. Max: {max_length}")
        
        # Remove control characters (keep newlines and tabs for formatted text)
        sanitized = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', value)
        
        return sanitized.strip()
    
    @staticmethod
    def validate_container_amount(
        current: float,
        to_add: float,
        capacity: float,
        container_name: str
    ) -> None:
        """
        Validate container fill operation.
        
        Args:
            current: Current amount in container
            to_add: Amount to add
            capacity: Container capacity
            container_name: Name of container for error messages
            
        Raises:
            ValueError: If validation fails
        """
        if to_add <= 0:
            raise ValueError("Amount to add must be positive")
        
        if to_add > capacity:
            raise ValueError(
                f"Cannot add {to_add} to {container_name}. "
                f"Exceeds total capacity ({capacity})"
            )
        
        new_amount = current + to_add
        if new_amount > capacity:
            raise ValueError(
                f"Adding {to_add} would overflow {container_name}. "
                f"Current: {current}, Capacity: {capacity}, "
                f"Available space: {capacity - current}"
            )
    
    @staticmethod
    def validate_coffee_type(value: str) -> str:
        """
        Validate coffee type value.
        
        Args:
            value: Coffee type string to validate
            
        Returns:
            Validated coffee type
            
        Raises:
            ValueError: If coffee type is invalid
        """
        valid_types = ["espresso", "double_espresso", "ristretto", "americano"]
        if value.lower() not in valid_types:
            raise ValueError(
                f"Invalid coffee type: {value}. "
                f"Valid types: {', '.join(valid_types)}"
            )
        return value.lower()
    
    @staticmethod
    def validate_percentage(value: float, field_name: str = "percentage") -> float:
        """
        Validate percentage value (0-100).
        
        Args:
            value: Percentage to validate
            field_name: Name of the field for error messages
            
        Returns:
            Validated percentage
            
        Raises:
            ValueError: If value is not a valid percentage
        """
        if value < 0 or value > 100:
            raise ValueError(f"{field_name} must be between 0 and 100, got {value}")
        return value


class SecureFloat(float):
    """Float that validates on creation."""
    
    def __new__(cls, value, min_value=0, max_value=10000):
        """
        Create a secure float with validation.
        
        Args:
            value: Float value
            min_value: Minimum allowed value
            max_value: Maximum allowed value
            
        Returns:
            SecureFloat instance
            
        Raises:
            ValueError: If value is out of range
        """
        if value < min_value or value > max_value:
            raise ValueError(
                f"Value must be between {min_value} and {max_value}"
            )
        return super().__new__(cls, value)

