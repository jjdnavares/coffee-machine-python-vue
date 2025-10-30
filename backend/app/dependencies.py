"""FastAPI dependencies for dependency injection."""
from app.services import CoffeeMachineService
from app.config import get_settings
from app.storage import get_storage

# Global service instance (set in main.py during startup)
_service_instance: CoffeeMachineService = None


def set_service_instance(service: CoffeeMachineService) -> None:
    """Set the global service instance."""
    global _service_instance
    _service_instance = service


def get_service() -> CoffeeMachineService:
    """Dependency to get coffee machine service."""
    if _service_instance is None:
        # Fallback: create service if not initialized
        settings = get_settings()
        storage = get_storage(settings.storage_type, file_path=settings.data_path)
        return CoffeeMachineService(storage)
    return _service_instance

