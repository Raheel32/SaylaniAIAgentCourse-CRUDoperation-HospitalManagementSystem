"""
crud/doctor.py
---------------
All database logic for doctors, kept separate from routes/doctor.py
(which only handles HTTP request/response wiring).
"""

from sqlalchemy.orm import Session
from app.models.doctor import Doctor
from app.schemas.doctor import DoctorCreate, DoctorUpdate


def create_doctor(db: Session, doctor: DoctorCreate) -> Doctor:
    db_doctor = Doctor(**doctor.dict())
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor


def get_doctor(db: Session, doctor_id: int) -> Doctor | None:
    return db.query(Doctor).filter(Doctor.doctor_id == doctor_id).first()


def get_all_doctors(db: Session, skip: int = 0, limit: int = 100) -> list[Doctor]:
    return db.query(Doctor).offset(skip).limit(limit).all()


def update_doctor(db: Session, doctor_id: int, doctor_update: DoctorUpdate) -> Doctor | None:
    db_doctor = get_doctor(db, doctor_id)
    if db_doctor is None:
        return None

    update_data = doctor_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_doctor, key, value)

    db.commit()
    db.refresh(db_doctor)
    return db_doctor


def delete_doctor(db: Session, doctor_id: int) -> Doctor | None:
    db_doctor = get_doctor(db, doctor_id)
    if db_doctor is None:
        return None

    db.delete(db_doctor)
    db.commit()
    return db_doctor
