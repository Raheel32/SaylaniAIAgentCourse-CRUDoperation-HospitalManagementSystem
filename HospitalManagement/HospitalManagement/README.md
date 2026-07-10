# Hospital Management System — FastAPI CRUD API

A layered, PostgreSQL-backed REST API for managing Doctors,
Patients, and Staff, with a real foreign-key relationship
between Patients and Doctors, and Alembic-managed schema migrations.

## Folder Structure

```
HospitalManagement/
├── app/
│   ├── main.py           # creates the app, includes all routers
│   ├── database.py       # SQLAlchemy engine/session + get_db()
│   ├── config.py         # loads DB credentials from .env
│   │
│   ├── models/            # SQLAlchemy tables
│   │   ├── doctor.py
│   │   ├── patient.py     # has a Foreign Key to doctors
│   │   └── staff.py
│   │
│   ├── schemas/            # Pydantic request/response validation
│   │   ├── doctor.py
│   │   ├── patient.py
│   │   └── staff.py
│   │
│   ├── crud/                # database logic, one file per entity
│   │   ├── doctor.py
│   │   ├── patient.py
│   │   └── staff.py
│   │
│   ├── routes/               # API endpoints, one file per entity
│   │   ├── doctor.py
│   │   ├── patient.py
│   │   └── staff.py
│   │
│   └── utils/                 # reserved for future shared helpers
│
├── alembic/                    # migration scripts
├── .env.example                 # template for your real .env (not committed)
├── .gitignore
├── requirements.txt
└── README.md
```

See `STEP_BY_STEP_GUIDE.md` for full beginner-friendly setup instructions.

## Quick Start

```bash
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
# create a .env file (copy .env.example and fill in your Postgres password)
alembic upgrade head
uvicorn app.main:app --reload
```

Then open `http://127.0.0.1:8000/docs`.

## API Endpoints

All three entities follow the same pattern:

| Method | Endpoint            |
|--------|----------------------|
| POST   | `/doctor/`, `/patient/`, `/staff/`         |
| GET    | `/doctor/`, `/patient/`, `/staff/`         |
| GET    | `/doctor/{id}`, `/patient/{id}`, `/staff/{id}` |
| PUT    | `/doctor/{id}`, `/patient/{id}`, `/staff/{id}` |
| DELETE | `/doctor/{id}`, `/patient/{id}`, `/staff/{id}` |

A patient's `doctor_id` is validated on create/update — assigning a
non-existent doctor returns a `404` with a clear message rather than a
raw database error.

## Design Notes

- Layered architecture: `models` (DB tables) → `schemas` (API
  validation) → `crud` (DB logic) → `routes` (HTTP endpoints) → `main.py`
  (wiring). Each layer only knows about the one below it.
- config.py + .env: real credentials never get hardcoded or
  committed — only `.env.example` (a template) is tracked.
- Alembic: schema changes go through migrations, not by dropping and
  recreating tables — see `STEP_BY_STEP_GUIDE.md` Phase 9 for the workflow.
