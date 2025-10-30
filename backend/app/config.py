"""Configuration management for the coffee machine application."""
from functools import lru_cache
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Storage configuration
    storage_type: str = "json"
    data_path: str = "data/machine_state.json"
    
    # Container default configurations
    water_capacity: float = 2000.0
    coffee_capacity: float = 500.0
    
    # Allow custom container sizes (optional, overrides defaults)
    custom_water_capacity: Optional[float] = None
    custom_coffee_capacity: Optional[float] = None
    
    # CORS and logging
    cors_origins: str = "http://localhost:5173"
    log_level: str = "INFO"
    
    # Rate limiting
    rate_limit_enabled: bool = True
    rate_limit_storage: str = "memory://"
    
    # API configuration
    api_title: str = "Coffee Machine API"
    api_version: str = "1.0.0"
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": False
    }
    
    @property
    def effective_water_capacity(self) -> float:
        """Return custom or default water capacity."""
        return self.custom_water_capacity if self.custom_water_capacity is not None else self.water_capacity
    
    @property
    def effective_coffee_capacity(self) -> float:
        """Return custom or default coffee capacity."""
        return self.custom_coffee_capacity if self.custom_coffee_capacity is not None else self.coffee_capacity


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance (singleton pattern)."""
    return Settings()

