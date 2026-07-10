"""
main.py
-------
Entry point of the app. Brings together the doctor, patient, and staff
routers under one FastAPI app.

To run this app (from the project's root folder):

    uvicorn app.main:app --reload

Then open http://127.0.0.1:8000/docs for the interactive Swagger UI.
"""

from fastapi import FastAPI

from app.database import engine, Base
from app import models  # noqa: F401 — registers all tables on Base.metadata
from app.routes import doctor, patient, staff

# NOTE: Since this project uses Alembic (see Phase 9), Alembic — not this
# line — is what should manage your schema in real development. This
# line is harmless to leave in (it only creates tables that don't
# already exist) but don't rely on it once you're actively migrating.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Hospital Management System",
    description="CRUD API for managing doctors, patients, and staff.",
    version="1.0.0",
)

app.include_router(doctor.router)
app.include_router(patient.router)
app.include_router(staff.router)


@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the Hospital Management System API. Visit /docs to try it out."}
