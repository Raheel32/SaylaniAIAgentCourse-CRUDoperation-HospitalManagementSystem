"""
schemas/patient.py
--------------------
Defines what JSON data the API accepts (Create/Update) and returns
(Response) for patients.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class PatientBase(BaseModel):
    name: str = Field(..., example="Ayesha Khan")
    age: int = Field(..., gt=0, lt=150, example=32)
    gender: str = Field(..., example="Female")
    disease: Optional[str] = Field(None, example="Diabetes")
    doctor_id: Optional[int] = Field(None, example=1)
    admission_date: Optional[date] = Field(None, example="2026-07-10")


class PatientCreate(PatientBase):
    """Used when creating a new patient (POST)."""
    pass


class PatientUpdate(BaseModel):
    """Used when updating a patient (PUT) — every field optional."""
    name: Optional[str] = None
    age: Optional[int] = Field(None, gt=0, lt=150)
    gender: Optional[str] = None
    disease: Optional[str] = None
    doctor_id: Optional[int] = None
    admission_date: Optional[date] = None


class PatientResponse(PatientBase):
    """Used when sending a patient back to the client — includes the id."""
    patient_id: int

    class Config:
        from_attributes = True
