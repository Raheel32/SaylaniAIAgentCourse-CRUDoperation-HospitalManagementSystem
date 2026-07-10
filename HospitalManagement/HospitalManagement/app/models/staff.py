"""
models/staff.py
----------------
Database table for hospital staff (non-doctor employees — e.g. nurses,
receptionists, technicians). Independent table, no foreign keys.
"""

from sqlalchemy import Column, Integer, String, Float
from app.database import Base


class Staff(Base):
    __tablename__ = "staff"

    staff_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    shift = Column(String, nullable=True)  # e.g. "Morning", "Evening", "Night"
    salary = Column(Float, nullable=True)
