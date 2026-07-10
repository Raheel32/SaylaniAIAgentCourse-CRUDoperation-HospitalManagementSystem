"""
models/doctor.py
----------------
Database table for doctors. Has a one-to-many relationship with
Patient — one doctor can have many patients.
"""

from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.database import Base


class Doctor(Base):
    __tablename__ = "doctors"

    doctor_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    specialization = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=True)
    salary = Column(Float, nullable=True)

    # This isn't a real database column — it lets us write
    # `doctor.patients` in Python to get all patients assigned to this
    # doctor. The actual link is the foreign key on the Patient table.
    patients = relationship("Patient", back_populates="doctor")
