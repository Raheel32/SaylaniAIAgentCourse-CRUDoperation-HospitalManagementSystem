"""
crud/staff.py
--------------
All database logic for staff members.
"""

from sqlalchemy.orm import Session
from app.models.staff import Staff
from app.schemas.staff import StaffCreate, StaffUpdate


def create_staff(db: Session, staff: StaffCreate) -> Staff:
    db_staff = Staff(**staff.dict())
    db.add(db_staff)
    db.commit()
    db.refresh(db_staff)
    return db_staff


def get_staff(db: Session, staff_id: int) -> Staff | None:
    return db.query(Staff).filter(Staff.staff_id == staff_id).first()


def get_all_staff(db: Session, skip: int = 0, limit: int = 100) -> list[Staff]:
    return db.query(Staff).offset(skip).limit(limit).all()


def update_staff(db: Session, staff_id: int, staff_update: StaffUpdate) -> Staff | None:
    db_staff = get_staff(db, staff_id)
    if db_staff is None:
        return None

    update_data = staff_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_staff, key, value)

    db.commit()
    db.refresh(db_staff)
    return db_staff


def delete_staff(db: Session, staff_id: int) -> Staff | None:
    db_staff = get_staff(db, staff_id)
    if db_staff is None:
        return None

    db.delete(db_staff)
    db.commit()
    return db_staff
