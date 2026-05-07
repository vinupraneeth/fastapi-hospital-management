from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.doctor import Doctor

def create_doctor(db: Session, doctor_data):
    existing = db.query(Doctor).filter(
        Doctor.email == doctor_data.email
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Doctor email already exists"
        )

    doctor = Doctor(
        name=doctor_data.name,
        specialization=doctor_data.specialization,
        email=doctor_data.email
    )

    db.add(doctor)
    db.commit()
    db.refresh(doctor)

    return doctor


def get_all_doctors(db: Session):
    return db.query(Doctor).all()


def get_doctor_by_id(db: Session, doctor_id: int):
    doctor = db.query(Doctor).filter(
        Doctor.id == doctor_id
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    return doctor

def assign_patient_to_doctor(
    db: Session,
    doctor_id: int,
    patient_id: int
):
    doctor = db.query(Doctor).filter(
        Doctor.id == doctor_id
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    patient = db.query(Patient).filter(
        Patient.id == patient_id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    existing = db.query(DoctorPatient).filter(
        DoctorPatient.doctor_id == doctor_id,
        DoctorPatient.patient_id == patient_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Patient already assigned"
        )

    assignment = DoctorPatient(
        doctor_id=doctor_id,
        patient_id=patient_id
    )

    db.add(assignment)
    db.commit()

    return {
        "message": "Patient assigned successfully"
    }


from app.models.patient import Patient
from app.models.association import DoctorPatient

def get_doctor_patients(
    db: Session,
    doctor_id: int
):
    doctor = db.query(Doctor).filter(
        Doctor.id == doctor_id
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    patients = (
        db.query(Patient)
        .join(
            DoctorPatient,
            Patient.id == DoctorPatient.patient_id
        )
        .filter(
            DoctorPatient.doctor_id == doctor_id
        )
        .all()
    )

    return patients

def update_doctor(
    db: Session,
    doctor_id: int,
    doctor_data
):
    doctor = db.query(Doctor).filter(
        Doctor.id == doctor_id
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    existing_email = db.query(Doctor).filter(
        Doctor.email == doctor_data.email,
        Doctor.id != doctor_id
    ).first()

    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    doctor.name = doctor_data.name
    doctor.specialization = doctor_data.specialization
    doctor.email = doctor_data.email
    doctor.is_active = doctor_data.is_active

    db.commit()
    db.refresh(doctor)

    return doctor

def soft_delete_doctor(
    db: Session,
    doctor_id: int
):
    doctor = db.query(Doctor).filter(
        Doctor.id == doctor_id
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    doctor.is_active = False

    db.commit()

    return {
        "message": "Doctor soft deleted successfully"
    }