# Coffee Machine Backend

FastAPI backend for the coffee machine simulator.

## API Endpoints

### Coffee Making

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| POST | `/api/coffee/espresso` | Make espresso | None | `{success: true, message: "Espresso ready!"}` |
| POST | `/api/coffee/double-espresso` | Make double espresso | None | `{success: true, message: "Double espresso ready!"}` |
| POST | `/api/coffee/americano` | Make americano | None | `{success: true, message: "Americano ready!"}` |

### Management

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| GET | `/api/status` | Get machine status | None | `{success: true, data: {...}}` |
| POST | `/api/fill/water` | Fill water container | `{amount: float}` | `{success: true, message: "..."}` |
| POST | `/api/fill/coffee` | Fill coffee container | `{amount: float}` | `{success: true, message: "..."}` |
| GET | `/api/health` | Health check | None | `{status: "healthy", timestamp: "..."}` |
| POST | `/api/reset` | Reset machine | None | `{success: true, message: "..."}` |

## Error Responses

All errors follow this format:

```json
{
  "success": false,
  "message": "Human-readable error message",
  "error_type": "InsufficientResourcesException|ContainerOverflowException|InvalidAmountException",
  "details": {
    "key": "value"
  }
}
```

### HTTP Status Codes

- `200` - Success
- `400` - Bad request (invalid input)
- `409` - Conflict (insufficient resources, overflow)
- `422` - Validation error
- `500` - Server error

## Setup

### Local Development

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### With Docker

```bash
docker-compose up backend
```

## Testing

```bash
pytest
pytest -v  # verbose
pytest --cov=app  # with coverage
```

## Architecture

- **models.py:** Pydantic models for data validation
- **services.py:** Business logic layer
- **storage.py:** Storage abstraction layer
- **exceptions.py:** Custom exceptions with user-friendly messages
- **config.py:** Configuration management
- **main.py:** FastAPI application and routes

## Environment Variables

- `STORAGE_TYPE`: Storage backend (default: "json")
- `DATA_PATH`: Path to state file (default: "data/machine_state.json")
- `WATER_CAPACITY`: Water container capacity in ml (default: 2000.0)
- `COFFEE_CAPACITY`: Coffee container capacity in grams (default: 500.0)
- `CORS_ORIGINS`: Allowed CORS origins (default: "http://localhost:5173")

