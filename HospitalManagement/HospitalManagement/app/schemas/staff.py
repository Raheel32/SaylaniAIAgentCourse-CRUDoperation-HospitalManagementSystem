"""
schemas/staff.py
-----------------
Defines what JSON data the API accepts (Create/Update) and returns
(Response) for staff members.
"""

from pydantic import BaseModel, Field
from typing import Optional


class StaffBase(BaseModel):
    name: str = Field(..., example="Muhammad Bilal")
    role: str = Field(..., example="Nurse")
    shift: Optional[str] = Field(None, example="Morning")
    salary: Optional[float] = Field(None, example=60000.0)


class StaffCreate(StaffBase):
    """Used when creating a new staff member (POST)."""
    pass


class StaffUpdate(BaseModel):
    """Used when updating a staff member (PUT) — every field optional."""
    name: Optional[str] = None
    role: Optional[str] = None
    shift: Optional[str] = None
    salary: Optional[float] = None


class StaffResponse(StaffBase):
    """Used when sending a staff member back to the client — includes the id."""
    staff_id: int

    class Config:
        from_attributes = True
