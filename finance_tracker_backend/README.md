# Finance Tracker Backend

A lightweight Flask REST API for managing finance entries. Supports basic CRUD endpoints for finance records.

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
   python app.py
   ```
