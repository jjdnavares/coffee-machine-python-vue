"""Configuration management for the coffee machine application."""
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    storage_type: str = "json"
    data_path: str = "data/machine_state.json"
    water_capacity: float = 2000.0
    coffee_capacity: float = 500.0
    cors_origins: str = "http://localhost:5173,http://localhost:5174"
    log_level: str = "INFO"
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": False
    }


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance (singleton pattern)."""
    return Settings()

