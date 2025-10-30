# Coffee Machine Simulator

A production-quality coffee machine simulation with FastAPI backend and Vue.js frontend, fully containerized with Docker.

## Features

- ☕ Three coffee types: Espresso, Double Espresso, and Americano
- 📊 Real-time status monitoring with visual progress bars
- 💧 Container management (water and coffee)
- 💾 State persistence between restarts
- 🐳 Full Docker containerization
- 🧪 Comprehensive test coverage
- 📝 RESTful API with automatic documentation
- 🎨 Modern, responsive Vue.js interface

## Technology Stack

- **Backend:** FastAPI (Python 3.11+), Pydantic, Uvicorn
- **Frontend:** Vue 3 (Composition API), Vite, Axios
- **Infrastructure:** Docker, Docker Compose
- **Storage:** JSON file (extensible to Redis/SQLite)
- **Testing:** Pytest (backend), Vitest (frontend)

## Prerequisites

- Docker & Docker Compose, OR
- Python 3.11+ and Node.js 18+

## Quick Start with Docker

### Step 1: Navigate to project directory
```bash
cd coffee-machine-python-vue
```

### Step 2: Copy environment file (optional)
```bash
cp .env.example .env
```

### Step 3: Start services
```bash
docker-compose up --build
```

### Step 4: Access the application
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000/api
- API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Manual Setup (Without Docker)

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend Setup (separate terminal)

```bash
cd frontend
npm install
npm run dev
```

## Project Structure

```
coffee-machine-python-vue/
├── backend/          # FastAPI application
│   ├── app/          # Application code
│   ├── tests/        # Test files
│   ├── data/         # Persistent storage
│   └── Dockerfile
├── frontend/         # Vue.js application
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   └── utils/
│   └── Dockerfile
├── postman/          # Postman collection
├── docker-compose.yml
└── README.md
```

## API Versioning

All endpoints are exposed under both `/api/v1/` (recommended) and `/api/` prefixes for backward compatibility.
For all new integrations and documentation, use `/api/v1/`.

Example:
- `/api/v1/coffee/espresso`
- `/api/coffee/espresso`
(Both work, but `/api/v1/` is future-proof.)

### Coffee Making Endpoints

| Method | Endpoint                         | Description                              |
|--------|----------------------------------|------------------------------------------|
| POST   | `/api/v1/coffee/espresso`        | Make espresso                            |
| POST   | `/api/v1/coffee/double-espresso` | Make double espresso                     |
| POST   | `/api/v1/coffee/americano`       | Make americano                           |

### Management Endpoints

| Method | Endpoint                | Description              |
|--------|-------------------------|--------------------------|
| GET    | `/api/v1/status`        | Get machine status       |
| POST   | `/api/v1/fill/water`    | Fill water container     |
| POST   | `/api/v1/fill/coffee`   | Fill coffee container    |
| GET    | `/api/v1/health`        | Health check             |
| POST   | `/api/v1/reset`         | Reset machine            |

### Example Requests

**Make Espresso:**
```bash
curl -X POST http://localhost:8000/api/v1/coffee/espresso
```

**Fill Water:**
```bash
curl -X POST http://localhost:8000/api/v1/fill/water \
  -H "Content-Type: application/json" \
  -d '{"amount": 500}'
```

**Get Status:**
```bash
curl http://localhost:8000/api/v1/status
```

## Testing

### Run Backend Tests
```bash
cd backend
pytest
```

### Run with Coverage
```bash
cd backend
pytest --cov=app --cov-report=html
```

## Environment Variables

See `.env.example` for all available configuration options.

## Architecture

The application follows a clean architecture pattern:

- **Models:** Pydantic models for data validation
- **Services:** Business logic layer
- **Storage:** Abstract storage interface (JSON implementation)
- **API:** FastAPI endpoints with dependency injection
- **Frontend:** Component-based Vue.js application

## Assumptions Made

1. Machine starts with empty containers
2. Container sizes are configurable via environment variables
3. Fill operations add to existing amount (not replace)
4. State persists across container restarts via volume mount
5. All amounts must be positive numbers

## Future Enhancements

- [ ] Redis storage implementation
- [ ] SQLite storage implementation
- [ ] Frontend unit tests with Vitest
- [ ] WebSocket support for real-time updates
- [ ] Analytics dashboard
- [ ] Multiple machine instances

## License

MIT

## Author

Jay

---

**Note:** This is a coding project demonstrating clean architecture, TDD, and modern web development practices.

