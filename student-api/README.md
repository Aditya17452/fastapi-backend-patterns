# Student Management API

A FastAPI service for managing student records, built to practise production backend patterns: layered architecture, JWT authentication, password hashing, Redis caching and database migrations.

## Highlights

- **Layered design** — routers (HTTP) → services (business logic) → SQLAlchemy models, with separate Pydantic models for input and output
- **Authentication** — register / login, Argon2 password hashing (`pwdlib`), JWT bearer tokens (PyJWT) checked by a reusable dependency
- **Redis cache-aside** — `GET /student/{id}` reads from Redis first and caches the result for 60 seconds; updates and deletes invalidate the key. If Redis is down the API keeps working straight from the database
- **Migrations** — Alembic, reading the database URL from the environment
- **Safe responses** — password hashes are never returned

## Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/student/register` | — | Register (`id`, `name`, `email`, `password`) |
| POST | `/student/login?id=…&password=…` | — | Get a bearer token |
| GET | `/students` | ✓ | List students |
| POST | `/students` | ✓ | Create a student |
| GET | `/student/{id}` | ✓ | Get a student (cached) |
| PUT | `/student/{id}` | ✓ | Update name and email |
| DELETE | `/student/{id}` | ✓ | Delete a student |
| GET | `/health` | — | Health check |

## Run locally

Requires PostgreSQL (or set `DATABASE_URL=sqlite:///./students.db` to try it without Postgres) and optionally Redis.

```bash
pip install -r requirements.txt
cp .env.example .env        # set DATABASE_URL, REDIS_URL, JWT_SECRET
uvicorn main:app --reload
```

Tables are created on startup. When the schema changes, generate and apply a migration:

```bash
alembic revision --autogenerate -m "describe change"
alembic upgrade head
```

On a fresh database created by the app, run `alembic stamp head` once so Alembic knows the schema is current.

## Structure

```
├── main.py                       app and startup
├── routers/student.py            endpoints, caching
├── services/services.py          business logic
├── models/student.py             SQLAlchemy model
├── schemas/student.py            request / response models
├── auth/                         hashing, JWT, current-user dependency
├── database/config.py            engine and sessions
├── infrastructure/redis_client.py  Redis helpers with graceful fallback
└── alembic/                      migrations
```
