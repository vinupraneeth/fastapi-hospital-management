from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.patient import Patient
from app.schemas.patient import PatientCreate


def create_patient(
    db: Session,
    request: PatientCreate
):
    existing = db.query(Patient).filter(
        Patient.email == request.email
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    patient = Patient(
        name=request.name,
        email=request.email,
        age=request.age,
        phone=request.phone
    )

    db.add(patient)
    db.commit()
    db.refresh(patient)

    return patient


def get_all_patients(db: Session):
    return db.query(Patient).all()


def get_patient_by_id(
    db: Session,
    patient_id: int
):
    patient = db.query(Patient).filter(
        Patient.id == patient_id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    return patient