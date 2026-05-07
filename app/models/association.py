from sqlalchemy import Column, Integer, ForeignKey
from app.db.base import Base


class DoctorPatient(Base):
    __tablename__ = "doctor_patients"

    id = Column(Integer, primary_key=True, index=True)

    doctor_id = Column(
        Integer,
        ForeignKey("doctors.id")
    )

    patient_id = Column(
        Integer,
        ForeignKey("patients.id")
    )