"""Tests for configuration module."""
import pytest
from app.config import Settings, get_settings


class TestSettings:
    """Test Settings configuration class."""

    def test_settings_has_default_values(self):
        """Test that Settings has default values."""
        settings = Settings()
        assert settings.storage_type == "json"
        assert settings.data_path == "data/machine_state.json"
        assert settings.water_capacity == 2000.0
        assert settings.coffee_capacity == 500.0
        assert "localhost:5173" in settings.cors_origins

    def test_settings_can_be_overridden_by_env(self, monkeypatch):
        """Test that environment variables override defaults."""
        monkeypatch.setenv("STORAGE_TYPE", "redis")
        monkeypatch.setenv("WATER_CAPACITY", "3000.0")
        
        # Force clear the cache
        get_settings.cache_clear()
        settings = get_settings()
        
        assert settings.storage_type == "redis"
        assert settings.water_capacity == 3000.0
        get_settings.cache_clear()

    def test_get_settings_returns_singleton(self):
        """Test that get_settings returns the same instance."""
        settings1 = get_settings()
        settings2 = get_settings()
        assert settings1 is settings2

