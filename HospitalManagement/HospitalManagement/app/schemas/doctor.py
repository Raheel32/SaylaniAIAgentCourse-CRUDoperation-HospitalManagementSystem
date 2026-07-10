"""
schemas/doctor.py
------------------
Defines what JSON data the API accepts (Create/Update) and returns
(Response) for doctors. Separate from models/doctor.py, which defines
the actual database table.
"""

from pydantic import BaseModel, Field
from typing import Optional


class DoctorBase(BaseModel):
    name: str = Field(..., example="Dr. Sarah Ahmed")
    specialization: str = Field(..., example="Cardiology")
    # Using `str` here rather than Pydantic's EmailStr on purpose — EmailStr
    # needs an extra "email-validator" package, which isn't in this
    # project's requirements.txt. If you want real email format validation,
    # add `email-validator` to requirements.txt and change this to EmailStr.
    email: str = Field(..., example="sarah.ahmed@hospital.com")
    phone: Optional[str] = Field(None, example="03001234567")
    salary: Optional[float] = Field(None, example=250000.0)


class DoctorCreate(DoctorBase):
    """Used when creating a new doctor (POST)."""
    pass


class DoctorUpdate(BaseModel):
    """Used when updating a doctor (PUT) — every field optional."""
    name: Optional[str] = None
    specialization: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    salary: Optional[float] = None


class DoctorResponse(DoctorBase):
    """Used when sending a doctor back to the client — includes the id."""
    doctor_id: int

    class Config:
        from_attributes = True
