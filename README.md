**SaylaniAIAgentCourse-CRUDoperation-HospitalManagementSystem**

A layered, PostgreSQL-backed REST API for managing Doctors, Patients, and Staff, with a real foreign-key relationship between Patients and Doctors, and Alembic-managed schema migrations.

**Hospital Management System (FastAPI CRUD API)**

This project is a Hospital Management System built with FastAPI, PostgreSQL, SQLAlchemy, and Alembic. It provides REST APIs for managing Doctors, Patients, and Staff while following a clean layered architecture.

One of the main features of this project is the relationship between Doctors and Patients. Every patient is assigned to a doctor, and the API checks whether the doctor exists before saving the patient, preventing invalid data from being added to the database.

The project also uses Alembic for database migrations, making it easy to update the database schema without deleting existing data.

 **Folder Structure**

```
HospitalManagement/
├── app/
│   ├── main.py           - creates the app, includes all routers
│   ├── database.py       - SQLAlchemy engine/session + get_db()
│   ├── config.py         - loads DB credentials from .env
│   │
│   ├── models/            - SQLAlchemy tables
│   │   ├── doctor.py
│   │   ├── patient.py     - has a Foreign Key to doctors
│   │   └── staff.py
│   │
│   ├── schemas/            - Pydantic request/response validation
│   │   ├── doctor.py
│   │   ├── patient.py
│   │   └── staff.py
│   │
│   ├── crud/                - database logic, one file per entity
│   │   ├── doctor.py
│   │   ├── patient.py
│   │   └── staff.py
│   │
│   ├── routes/               - API endpoints, one file per entity
│   │   ├── doctor.py
│   │   ├── patient.py
│   │   └── staff.py
│   │
│   └── utils/                 - reserved for future shared helpers
│
├── alembic/                    - migration scripts
├── .env.example                 - template for your real .env (not committed)
├── .gitignore
├── requirements.txt
└── README.md
```

 **Technologies Used**
. FastAPI
. PostgreSQL
. SQLAlchemy
. Alembic
. Pydantic
. Python


**Quick Start**

```bash
python -m venv venv
venv\Scripts\activate        - Windows
pip install -r requirements.txt
- create a .env file (copy .env.example and fill in your Postgres password)
alembic upgrade head
uvicorn app.main:app reload
```

Then open `http://127.0.0.1:8000/docs`.

**API Endpoints**

All three entities follow the same pattern:

| Method | Endpoint            |
|||
| POST   | `/doctor/`, `/patient/`, `/staff/`         |
| GET    | `/doctor/`, `/patient/`, `/staff/`         |
| GET    | `/doctor/{id}`, `/patient/{id}`, `/staff/{id}` |
| PUT    | `/doctor/{id}`, `/patient/{id}`, `/staff/{id}` |
| DELETE | `/doctor/{id}`, `/patient/{id}`, `/staff/{id}` |

**Doctor and Patient Relationship**

Patients are linked to doctors using a foreign key (doctor_id).
Before creating or updating a patient, the application checks whether the provided doctor exists. If the doctor isn't found, the API returns a 404 Not Found response with a helpful error message instead of letting PostgreSQL raise a foreign key error.
This makes the API easier to use and provides clearer feedback to anyone consuming it.

A patient's `doctor_id` is validated on create/update — assigning a
non-existent doctor returns a `404` with a clear message rather than a
raw database error.

**Project Architecture**

The project follows a simple layered architecture to keep the code organized and easier to maintain.

Models define the database tables.
Schemas handle request validation and API responses.
CRUD contains all database-related logic.
Routes define the API endpoints.
main.py brings everything together by registering the routes.

Keeping responsibilities separated makes the project easier to understand and extend as it grows.


**Database Configuration**

Database credentials are stored in a .env file rather than hardcoded in the project.
The repository only includes a .env.example file so other developers know which variables are required without exposing sensitive information.


 **Design Notes
**
- Layered architecture: `models` (DB tables) → `schemas` (API
  validation) → `crud` (DB logic) → `routes` (HTTP endpoints) → `main.py`
  (wiring). Each layer only knows about the one below it.
- config.py + .env: real credentials never get hardcoded or
  committed — only `.env.example` is tracked.
- Alembic: schema changes go through migrations, not by dropping and
  recreating tables

**Future Improvements**

Some ideas that could be added later include:

. User authentication and authorization
. Search and filtering
. Pagination
. Appointment management
. Medical records
. Role-based access control
. Unit and integration tests
