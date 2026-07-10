"""
models/patient.py
------------------
Database table for patients. Each patient can (optionally) be assigned
to one doctor, via the doctor_id foreign key.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.database import Base


class Patient(Base):
    __tablename__ = "patients"

    patient_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    disease = Column(String, nullable=True)

    # Foreign key: links this patient to a row in the "doctors" table.
    # nullable=True means a patient can exist without a doctor assigned yet.
    doctor_id = Column(Integer, ForeignKey("doctors.doctor_id"), nullable=True)

    admission_date = Column(Date, nullable=True)

    # Lets us write `patient.doctor` in Python to get the assigned
    # doctor's full record (name, specialization, etc.), not just the id.
    doctor = relationship("Doctor", back_populates="patients")
