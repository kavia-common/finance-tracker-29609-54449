# Finance Tracker Backend – DDD Core Domain Concepts and Structure

## 1. Current State – Domain Concepts

### 1.1 Aggregates
- **FinanceEntry Aggregate**
  - The current application essentially treats all finance entries independently, with `FinanceEntry` as the central aggregate root.
  - There is no transactional boundary beyond single entry CRUD at present.

### 1.2 Entities
- **FinanceEntry**
  - Has identity: `id`
  - Attributes: description, amount, category, date
  - Mutable fields; persisted in database.

### 1.3 Value Objects
- No explicit value objects currently, but suitable candidates:
  - **Money**: Could encapsulate amount, currency (if ever extended).
  - **EntryDate**: Wrapping Python `date` for possible validation/enhancement.
  - **Description** and **Category** could also be value objects for encapsulation/validation.

### 1.4 Repositories
- The current codebase uses SQLAlchemy's ORM directly inside route handlers.
- No repository pattern abstraction exists yet.
- **Repository to be introduced:** `FinanceEntryRepository` for all persistence operations.

### 1.5 Domain Services
- No explicit domain or application services are present.
- All business logic currently resides inside Flask routes.
- Candidates for extraction:
  - **Entry Management Service**: Business logic around creation, update, and deletion.
  - **Reporting Service**: Calculating running totals, summaries, etc.
- Validation (entry data) is present as utility (`validate_entry_json`), but could be converted into value object logic or domain service/validator.

---

## 2. Proposed DDD Structure (For Refactor)

Below is a _suggested_ DDD directory and file layout for this backend, encapsulating responsibilities cleanly and following typical DDD layering and boundaries.

```
finance_tracker_backend/
├── domain/
│   ├── __init__.py
│   ├── finance_entry/
│   │   ├── __init__.py
│   │   ├── entities.py         # FinanceEntry entity
│   │   ├── value_objects.py    # Money, EntryDate, etc.
│   │   ├── repository.py       # Repository interface
│   │   └── services.py         # Domain services (business logic)
│   └── ... (other bounded contexts as needed)
├── infrastructure/
│   ├── __init__.py
│   ├── persistence/
│   │   ├── __init__.py
│   │   ├── sqlalchemy_repo.py  # SQLAlchemy implementation of repository
│   │   └── db_models.py        # ORM models if needed
│   └── ... (external service impls, etc.)
├── application/
│   ├── __init__.py
│   ├── entry_service.py        # Application/orchestrating services
│   └── ... (DTOs, mappers, etc.)
├── api/
│   ├── __init__.py
│   ├── routes.py               # Flask route handlers (thin controllers)
│   └── ... (schemas, validators)
├── config/
│   ├── __init__.py
│   └── settings.py             # DB/Flask configuration
├── app.py                      # App factory/bootstrap
└── requirements.txt
```

## 3. Mapping Current Logic to DDD

| Current Code Element       | DDD Role                   | New Location                 |
|---------------------------|----------------------------|------------------------------|
| `FinanceEntry` model      | Entity (Aggregate Root)    | `domain/finance_entry/entities.py`       |
| CRUD in Flask routes      | Application + API Layer    | `application/`, `api/routes.py`          |
| SQLAlchemy calls in routes| Infrastructure/Repository  | `infrastructure/persistence/*`           |
| Validation utils          | Domain/Value Object logic  | `domain/finance_entry/value_objects.py`  |
| Business rules (currently minimal) | Domain Services    | `domain/finance_entry/services.py`       |

## 4. Next Steps

- Extract `FinanceEntry` as a pure domain entity, decoupled from SQLAlchemy.
- Introduce value objects for Amount, Date, Category, Description (add logic if needed).
- Implement repository interfaces in domain; infra layer for SQLAlchemy.
- Move validation/business logic to services/value objects.
- Make Flask routes thin: only orchestrate application layer services.

---

**Prepared by: DDD Analysis Agent**

Task: "Analyze backend code, document domain concepts, and outline DDD structure."
