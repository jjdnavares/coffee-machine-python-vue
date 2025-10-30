"""Tests for storage layer."""
import pytest
import json
import tempfile
import os
from datetime import datetime
from app.storage import StorageInterface, JSONStorage, get_storage
from app.models import MachineState, WaterContainer, CoffeeContainer


class TestJSONStorage:
    """Test JSONStorage implementation."""

    def test_save_and_load_state(self):
        """Test saving and loading state from JSON file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            file_path = f.name
        
        try:
            storage = JSONStorage(file_path)
            
            # Create initial state
            initial_state = MachineState(
                water_container=WaterContainer(current_amount=100.0, capacity=2000.0),
                coffee_container=CoffeeContainer(current_amount=50.0, capacity=500.0),
                total_coffees_made=5,
                last_updated=datetime.now()
            )
            
            # Save state
            storage.save_state(initial_state)
            
            # Load state
            loaded_state = storage.load_state()
            
            assert loaded_state.water_container.current_amount == 100.0
            assert loaded_state.coffee_container.current_amount == 50.0
            assert loaded_state.total_coffees_made == 5
        finally:
            if os.path.exists(file_path):
                os.unlink(file_path)

    def test_load_state_creates_new_if_file_doesnt_exist(self):
        """Test that loading from non-existent file returns new state."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            file_path = f.name
        
        try:
            os.unlink(file_path)  # Ensure file doesn't exist
            
            storage = JSONStorage(file_path)
            state = storage.load_state()
            
            assert state.water_container.current_amount == 0.0
            assert state.coffee_container.current_amount == 0.0
            assert state.total_coffees_made == 0
        finally:
            if os.path.exists(file_path):
                os.unlink(file_path)

    def test_load_state_handles_invalid_json(self):
        """Test that loading invalid JSON returns new state."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            f.write("invalid json content")
            file_path = f.name
        
        try:
            storage = JSONStorage(file_path)
            state = storage.load_state()
            
            # Should return new state on error
            assert state.water_container.current_amount == 0.0
            assert state.coffee_container.current_amount == 0.0
        finally:
            if os.path.exists(file_path):
                os.unlink(file_path)

    def test_save_state_creates_parent_directory(self):
        """Test that save_state creates parent directories if needed."""
        temp_dir = tempfile.mkdtemp()
        file_path = os.path.join(temp_dir, "subdir", "machine_state.json")
        
        try:
            storage = JSONStorage(file_path)
            state = MachineState(
                water_container=WaterContainer(),
                coffee_container=CoffeeContainer(),
                total_coffees_made=0,
                last_updated=datetime.now()
            )
            
            storage.save_state(state)
            
            assert os.path.exists(file_path)
        finally:
            import shutil
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)


class TestStorageFactory:
    """Test storage factory function."""

    def test_get_storage_returns_json_storage(self):
        """Test that get_storage returns JSONStorage for json type."""
        storage = get_storage("json", file_path="test.json")
        assert isinstance(storage, JSONStorage)

    def test_get_storage_raises_for_unsupported_type(self):
        """Test that get_storage raises error for unsupported types."""
        with pytest.raises(ValueError, match="Unsupported storage type"):
            get_storage("redis", file_path="test.json")

