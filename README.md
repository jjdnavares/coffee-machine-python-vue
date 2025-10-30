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
cd coffee-machine
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
coffee-machine/
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

## API Documentation

### Coffee Making Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/coffee/espresso` | Make espresso (8g coffee, 24ml water) |
| POST | `/api/coffee/double-espresso` | Make double espresso (16g coffee, 48ml water) |
| POST | `/api/coffee/americano` | Make americano (16g coffee, 148ml water) |

### Management Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/status` | Get machine status |
| POST | `/api/fill/water` | Fill water container |
| POST | `/api/fill/coffee` | Fill coffee container |
| GET | `/api/health` | Health check |
| POST | `/api/reset` | Reset machine |

### Example Requests

**Make Espresso:**
```bash
curl -X POST http://localhost:8000/api/coffee/espresso
```

**Fill Water:**
```bash
curl -X POST http://localhost:8000/api/fill/water \
  -H "Content-Type: application/json" \
  -d '{"amount": 500}'
```

**Get Status:**
```bash
curl http://localhost:8000/api/status
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

Coffee Machine Project

---

**Note:** This is a coding assessment project demonstrating clean architecture, TDD, and modern web development practices.

