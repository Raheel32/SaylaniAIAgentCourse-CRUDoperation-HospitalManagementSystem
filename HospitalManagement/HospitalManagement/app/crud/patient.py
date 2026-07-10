"""
crud/patient.py
-----------------
All database logic for patients.
"""

from sqlalchemy.orm import Session
from app.models.patient import Patient
from app.schemas.patient import PatientCreate, PatientUpdate


def create_patient(db: Session, patient: PatientCreate) -> Patient:
    db_patient = Patient(**patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient


def get_patient(db: Session, patient_id: int) -> Patient | None:
    return db.query(Patient).filter(Patient.patient_id == patient_id).first()


def get_all_patients(db: Session, skip: int = 0, limit: int = 100) -> list[Patient]:
    return db.query(Patient).offset(skip).limit(limit).all()


def update_patient(db: Session, patient_id: int, patient_update: PatientUpdate) -> Patient | None:
    db_patient = get_patient(db, patient_id)
    if db_patient is None:
        return None

    update_data = patient_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_patient, key, value)

    db.commit()
    db.refresh(db_patient)
    return db_patient


def delete_patient(db: Session, patient_id: int) -> Patient | None:
    db_patient = get_patient(db, patient_id)
    if db_patient is None:
        return None

    db.delete(db_patient)
    db.commit()
    return db_patient
