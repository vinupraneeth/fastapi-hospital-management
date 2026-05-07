from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.patient import Patient


def create_patient(db: Session, patient_data):
    patient = Patient(
        name=patient_data.name,
        age=patient_data.age,
        phone=patient_data.phone
    )

    db.add(patient)
    db.commit()
    db.refresh(patient)

    return patient


def get_all_patients(db: Session):
    return db.query(Patient).all()


def get_patient_by_id(db: Session, patient_id: int):
    patient = db.query(Patient).filter(
        Patient.id == patient_id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    return patient