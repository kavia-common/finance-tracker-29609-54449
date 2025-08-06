# Finance Tracker Backend

A lightweight Flask REST API for managing finance entries (using DDD).

> **NOTE:** The backend is designed using Domain Driven Design (DDD) layering:
> - `domain/` – Pure business/domain logic (entities, value objects, repo interface)
> - `application/` – Orchestrates business operations
> - `infrastructure/` – DB/ORM/CORS/Flask config and repository implementation
> - `api/` – Thin Flask routes/controllers
> - `config/` – Settings

## Endpoints

- `GET /entries`: List all finance entries.
- `POST /entries`: Add a new entry.
- `PUT /entries/<id>`: Edit an existing entry.
- `DELETE /entries/<id>`: Delete an entry.
- `GET /health`: Health check.

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Run the application:
   ```
   python -m finance_tracker_backend.app
   ```

The HTTP API is backward compatible but now sharply separated into layers for maintainability and testing.

