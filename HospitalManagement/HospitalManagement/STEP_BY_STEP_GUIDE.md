# Step-by-Step Guide: Hospital Management System

This walks you through setting up and understanding the entire project,
phase by phase, matching the plan you were given. I've already built and
tested all the code (including running real CRUD requests against a real
PostgreSQL database) — this guide gets it running on your machine and
explains what everything does.

---

## Before You Start: Install PostgreSQL

Unlike the earlier Patient project (which used SQLite, a file-based
database needing no setup), this project uses PostgreSQL, a real
database server that runs in the background on your computer.

1. Download the installer from [postgresql.org/download](https://www.postgresql.org/download/)
   and pick your OS (Windows/Mac).
2. During installation, it will ask you to set a password for the
   `postgres` user — remember this, you'll need it shortly.
3. It will also ask for a port — leave it as the default, `5432`.
4. Once installed, you should have a tool called pgAdmin installed
   alongside it — a visual interface for browsing your databases. You
   can also just use the command line (`psql`), whichever you prefer.

---

## Phase 1 — Project Setup

Extract the zip I've given you. It already matches this exact structure:

```
HospitalManagement/
├── app/
│   ├── main.py, database.py, config.py
│   ├── models/    (doctor.py, patient.py, staff.py)
│   ├── schemas/   (doctor.py, patient.py, staff.py)
│   ├── crud/      (doctor.py, patient.py, staff.py)
│   ├── routes/    (doctor.py, patient.py, staff.py)
│   └── utils/     (empty for now — reserved for shared helpers later)
├── alembic/
├── requirements.txt
└── README.md
```

Open a terminal, navigate into it:
```bash
cd path/to/HospitalManagement
```

---

## Phase 2 — Install Dependencies

Create and activate a virtual environment (same as before):
```bash
python -m venv venv
venv\Scripts\activate       # Windows
```
> If PowerShell blocks this with a script-execution error, run:
> `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
> (same fix as last time).

Install everything:
```bash
pip install -r requirements.txt
```

This installs: `fastapi`, `uvicorn`, `sqlalchemy`, `alembic`, `pydantic`,
`pydantic-settings`, `psycopg2-binary` (lets Python talk to PostgreSQL),
and `python-dotenv` (reads `.env` files).

---

## Phase 3 — Create the PostgreSQL Database

Open a terminal (or use pgAdmin's Query Tool) and run:

Using the command line:
```bash

psql -U postgres

or 
if you dont know the path try this one 

& "C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres
```
It'll ask for the password you set during install. Once connected:
```sql
CREATE DATABASE hospital_db;
\q
```

Using pgAdmin instead: right-click "Databases" → Create → Database →
name it `hospital_db` → Save.

---

## Phase 4 — Configure SQLAlchemy (.env + config.py + database.py)

1. In the project root, copy `.env.example` to a new file named exactly
   `.env`:
   ```bash
   copy .env.example .env      # Windows
   ```
2. Open `.env` and fill in your real Postgres password:
   ```
   DATABASE_HOSTNAME=localhost
   DATABASE_PORT=5432
   DATABASE_NAME=hospital_db
   DATABASE_USERNAME=postgres
   DATABASE_PASSWORD=your_real_password_here
   ```
3. That's it — `app/config.py` reads this file automatically, builds the
   full connection URL, and `app/database.py` uses it to connect.

Verify it's wired correctly before moving on:
```bash
python -c "from app.config import settings; print(settings.database_url)"
```
You should see something like:
```
postgresql://postgres:your_real_password_here@localhost:5432/hospital_db
```
If this errors out, your `.env` is missing, misnamed, or missing a field
— double check spelling exactly matches `.env.example`.

---

## Phase 5 — The Models (Already Built)

Open `app/models/doctor.py`, `patient.py`, and `staff.py`. Key things to
notice:

- `Patient.doctor_id` is a `ForeignKey("doctors.doctor_id")` — this
  is what links a patient to a specific doctor at the database level.
- `relationship(...)` on both `Doctor` and `Patient` isn't a real
  database column — it's a convenience so that in Python you can write
  `doctor.patients` (get all patients for a doctor) or `patient.doctor`
  (get the full doctor record for a patient), instead of manually
  writing a join query every time.

---

## Phase 6 — The Schemas (Already Built)

Open `app/schemas/doctor.py` as an example. Every entity has 3 classes:
- `...Create` — required fields when adding a new record
- `...Update` — all fields optional, since you might only change one
  thing (e.g. just a doctor's salary)
- `...Response` — what gets sent back to the client, includes the id

This 3-way split is what lets FastAPI auto-generate clean, accurate
Swagger documentation and reject bad input before it ever reaches your
database.

---

## Phase 7 — The CRUD Layer (Already Built)

Open `app/crud/doctor.py`. Each file has the same 5 functions:
`create_x()`, `get_x()`, `get_all_x()`, `update_x()`, `delete_x()`.

These are plain Python functions that take a database session and
return SQLAlchemy objects — they know nothing about HTTP, routes, or
JSON. That separation means you could reuse this exact logic in a
script, a scheduled job, or a test, not just through the API.

---

## Phase 8 — The API Routes (Already Built)

Open `app/routes/doctor.py`. Each entity has its own `APIRouter` with
the 5 standard endpoints (`POST`, `GET` all, `GET` one, `PUT`, `DELETE`).
`app/main.py` then plugs all three routers into one app with
`app.include_router(...)`.

Worth noticing in `routes/patient.py`: there's an extra
`_validate_doctor_id()` check before creating/updating a patient. This
catches an invalid `doctor_id` early and returns a clean
`404 Doctor not found`, instead of letting a confusing raw database
error bubble up.

---

## Phase 9 — Alembic Migrations (Already Set Up — Just Run It)

I already ran `alembic init alembic`, wired `alembic/env.py` to read your
`.env` (via `config.py`) and to know about all 3 models, and generated
the first migration. You just need to apply it:

```bash
alembic upgrade head
```

This creates the `doctors`, `patients`, and `staff` tables — with the
real foreign key constraint — directly in your `hospital_db`.

Going forward, whenever you change a model (e.g. add a field to
`Staff`):
```bash
alembic revision --autogenerate -m "describe your change"
alembic upgrade head
```
(Same workflow as the earlier SQLite project's Alembic guide — nothing
new here, just now pointed at PostgreSQL.)

---

## Phase 10 — Run and Test

```bash
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs`. Test in this order (so foreign keys
resolve correctly):

1. POST `/doctor/` — create a doctor first. Note the `doctor_id` it
   returns (probably `1`).
2. POST `/patient/` — create a patient, and set `doctor_id` to the
   id from step 1.
3. Try creating a patient with a made-up `doctor_id` like `999` —
   confirm you get a clean `404`, not a server crash.
4. POST `/staff/` — create a staff member (no relationships here).
5. Try `GET`, `PUT`, and `DELETE` on each of the three, the same way you
   tested the earlier Patient project.

I already ran this exact sequence myself against a real PostgreSQL
database before handing this to you, so the code is confirmed working
— any errors you hit will be about local setup (Postgres connection,
`.env` values), not the code itself.

---

## What's *Not* Built Yet

The "Features We'll Add" list at the bottom of your plan (JWT auth,
password hashing, role-based authorization, search/filtering/pagination,
file uploads, appointments, prescriptions, logging, pytest, Docker,
CI/CD) are future additions, not part of Phases 1–10. The current
project is a complete, working foundation for all of those — but none
of them are built yet. Tackle Phases 1–10 first, get comfortable with
the layered structure, then come back and we can add these one at a
time (JWT auth is usually the natural next step, since search/pagination
and appointments/prescriptions build on top of the same CRUD pattern
you've just learned).

---

## Troubleshooting

| Problem | Likely Fix |
|---|---|
| `password authentication failed for user "postgres"` | Your `.env` password doesn't match what you set during PostgreSQL install |
| `could not connect to server` | PostgreSQL service isn't running — on Windows, check the "Services" app for "postgresql-x64-..." and start it |
| `database "hospital_db" does not exist` | Repeat Phase 3 — you need to create it first |
| `ModuleNotFoundError: No module named 'app'` | You're running commands from the wrong folder — make sure you're in the project root (the one containing `app/`, not inside `app/` itself) |
| Alembic says "Target database is not up to date" | Run `alembic upgrade head` before generating a new migration |
