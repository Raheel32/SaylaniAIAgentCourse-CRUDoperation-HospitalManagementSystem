"""
routes/patient.py
--------------------
API endpoints for patients. Also validates that doctor_id, if provided,
actually refers to a real doctor — otherwise the foreign key would fail
at the database level with a less friendly error.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.patient import PatientCreate, PatientUpdate, PatientResponse
from app.crud import patient as patient_crud
from app.crud import doctor as doctor_crud

router = APIRouter(prefix="/patient", tags=["Patients"])


def _validate_doctor_id(doctor_id: int | None, db: Session):
    """Raise a clear 404 if the given doctor_id doesn't exist."""
    if doctor_id is not None and doctor_crud.get_doctor(db, doctor_id) is None:
        raise HTTPException(status_code=404, detail=f"Doctor with id {doctor_id} not found")


@router.post("/", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    _validate_doctor_id(patient.doctor_id, db)
    return patient_crud.create_patient(db, patient)


@router.get("/", response_model=List[PatientResponse])
def get_all_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return patient_crud.get_all_patients(db, skip=skip, limit=limit)


@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    db_patient = patient_crud.get_patient(db, patient_id)
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return db_patient


@router.put("/{patient_id}", response_model=PatientResponse)
def update_patient(patient_id: int, patient: PatientUpdate, db: Session = Depends(get_db)):
    _validate_doctor_id(patient.doctor_id, db)
    db_patient = patient_crud.update_patient(db, patient_id, patient)
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return db_patient


@router.delete("/{patient_id}", response_model=PatientResponse)
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    db_patient = patient_crud.delete_patient(db, patient_id)
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return db_patient
