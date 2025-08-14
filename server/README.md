# Artaban Pardaz Backend

FastAPI + SQLAlchemy + PostgreSQL + GraphQL backend for the Artaban Pardaz Client-Server application.

## Features

- 🚀 FastAPI for high-performance API
- 🗄️ SQLAlchemy 2.0 with async support
- 🐘 PostgreSQL database
- 📊 GraphQL with Strawberry
- 🔐 JWT authentication
- 🧪 Comprehensive test suite
- 🐳 Docker containerization
- 📝 API documentation with OpenAPI

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Redis (optional, for caching)
- Docker & Docker Compose (optional)

### Development Setup

1. **Clone and setup:**
   ```bash
   # The init script has already set up everything!
   source venv/bin/activate
   ```

2. **Start development services (ensure you are in the project root):**
   ```bash
   ./scripts/dev.sh
   ```

3. **Run tests (ensure you are in the project root):**
   ```bash
   ./scripts/test.sh
   ```

### Docker Setup

```bash
docker-compose up -d
```

## API Documentation

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **GraphQL Playground:** http://localhost:8000/graphql

## Project Structure

```
.
├── src/                    # All source code
│   ├── app/                # Main FastAPI application, shared models, schemas, utils
│   │   ├── api/            # API endpoints
│   │   ├── graphql/        # GraphQL schema and resolvers
│   │   ├── models/         # Shared database models
│   │   ├── schemas/        # Shared Pydantic schemas
│   │   ├── services/       # Shared business logic services
│   │   └── utils/          # General utilities
│   ├── core/               # Core functionalities (config, database, security)
│   │   ├── config/
│   │   ├── database/
│   │   ├── security/
│   │   │   ├── auth/
│   │   │   ├── data/
│   │   │   ├── domain/
│   │   │   └── utils/
│   │   └── utils/
│   ├── features/           # Domain-specific features (Accounts, Products, etc.)
│   │   └── accounts/
│   │       ├── data/
│   │       │   ├── datasource/
│   │       │   │   ├── daos/
│   │       │   │   └── tables/
│   │       │   ├── models/
│   │       │   └── repository/
│   │       ├── domain/
│   │       │   ├── entity/
│   │       │   ├── enums/
│   │       │   ├── repository/
│   │       │   └── usecases/
│   │       └── presentation/
│   │           ├── controllers/
│   │           └── services/
│   └── config/             # Application-wide configuration
│       ├── constants/
│       ├── exceptions/
│       ├── injection/
│       ├── localization/
│       │   └── languages/
│       ├── router/
│       └── settings/
├── tests/                  # Unit and integration tests
├── scripts/                # Utility scripts (db management, dev server)
├── docker/                 # Docker related files
├── docs/                   # Documentation files
├── .env.example
├── .env
├── requirements.txt
├── requirements-dev.txt
├── docker-compose.yml
├── Dockerfile
├── pytest.ini
└── README.md
```

## Environment Variables

Copy `.env.example` to `.env` and update the values:

```env
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/artaban_pardaz_db
REDIS_URL=redis://localhost:6379/0
```

## Development Commands

- **Format code:** `./scripts/format.sh`
- **Run tests:** `./scripts/test.sh`
- **Start dev server:** `./scripts/dev.sh`
- **Database management:** `python scripts/db/manage.py [command]`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request
