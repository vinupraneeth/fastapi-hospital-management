from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.prescription import Prescription
from app.models.appointment import Appointment
from app.models.doctor import Doctor
from app.models.patient import Patient

#Creating Prescription
def create_prescription(
    db: Session,
    prescription_data
):
    appointment = db.query(Appointment).filter(
        Appointment.id == prescription_data.appointment_id
    ).first()

    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    if appointment.status == "cancelled":
        raise HTTPException(
            status_code=400,
            detail="Cannot create prescription for cancelled appointment"
        )

    if appointment.status != "completed":
        raise HTTPException(
            status_code=400,
            detail="Prescription allowed only for completed appointments"
        )

    existing = db.query(Prescription).filter(
        Prescription.appointment_id == prescription_data.appointment_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Prescription already exists for this appointment"
        )

    doctor = db.query(Doctor).filter(
        Doctor.id == prescription_data.doctor_id
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    patient = db.query(Patient).filter(
        Patient.id == prescription_data.patient_id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    prescription = Prescription(
        appointment_id=prescription_data.appointment_id,
        doctor_id=prescription_data.doctor_id,
        patient_id=prescription_data.patient_id,
        diagnosis=prescription_data.diagnosis,
        medicines=prescription_data.medicines,
        dosage_instructions=prescription_data.dosage_instructions,
        remarks=prescription_data.remarks
    )

    db.add(prescription)
    db.commit()
    db.refresh(prescription)

    return prescription


#Listing Prescriptions
def get_all_prescriptions(
    db: Session,
    user
):
    query = db.query(Prescription)

    if user.role == "doctor":

        doctor = db.query(Doctor).filter(
            Doctor.email == user.email
        ).first()

        if doctor:
            query = query.filter(
                Prescription.doctor_id == doctor.id
            )

    elif user.role == "patient":

        patient = db.query(Patient).filter(
            Patient.email == user.email
        ).first()

        if patient:
            query = query.filter(
                Prescription.patient_id == patient.id
            )

    return query.all()


#GET by ID
def get_prescription_by_id(
    db: Session,
    prescription_id: int
):
    prescription = db.query(Prescription).filter(
        Prescription.id == prescription_id
    ).first()

    if not prescription:
        raise HTTPException(
            status_code=404,
            detail="Prescription not found"
        )

    return prescription

