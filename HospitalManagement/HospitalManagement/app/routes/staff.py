"""
routes/staff.py
-----------------
API endpoints for staff members.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.staff import StaffCreate, StaffUpdate, StaffResponse
from app.crud import staff as staff_crud

router = APIRouter(prefix="/staff", tags=["Staff"])


@router.post("/", response_model=StaffResponse, status_code=status.HTTP_201_CREATED)
def create_staff(staff: StaffCreate, db: Session = Depends(get_db)):
    return staff_crud.create_staff(db, staff)


@router.get("/", response_model=List[StaffResponse])
def get_all_staff(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return staff_crud.get_all_staff(db, skip=skip, limit=limit)


@router.get("/{staff_id}", response_model=StaffResponse)
def get_staff(staff_id: int, db: Session = Depends(get_db)):
    db_staff = staff_crud.get_staff(db, staff_id)
    if db_staff is None:
        raise HTTPException(status_code=404, detail="Staff member not found")
    return db_staff


@router.put("/{staff_id}", response_model=StaffResponse)
def update_staff(staff_id: int, staff: StaffUpdate, db: Session = Depends(get_db)):
    db_staff = staff_crud.update_staff(db, staff_id, staff)
    if db_staff is None:
        raise HTTPException(status_code=404, detail="Staff member not found")
    return db_staff


@router.delete("/{staff_id}", response_model=StaffResponse)
def delete_staff(staff_id: int, db: Session = Depends(get_db)):
    db_staff = staff_crud.delete_staff(db, staff_id)
    if db_staff is None:
        raise HTTPException(status_code=404, detail="Staff member not found")
    return db_staff
