from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.appointment import Appointment
from app.models.doctor import Doctor
from app.models.patient import Patient


def create_appointment(
    db: Session,
    appointment_data
):
    doctor = db.query(Doctor).filter(
        Doctor.id == appointment_data.doctor_id
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    patient = db.query(Patient).filter(
        Patient.id == appointment_data.patient_id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    overlapping = db.query(Appointment).filter(
        Appointment.doctor_id == appointment_data.doctor_id,
        Appointment.appointment_date == appointment_data.appointment_date,
        Appointment.appointment_time == appointment_data.appointment_time,
        Appointment.status != "cancelled"
    ).first()

    if overlapping:
        raise HTTPException(
            status_code=400,
            detail="Doctor already has appointment at this time"
        )

    appointment = Appointment(
        patient_id=appointment_data.patient_id,
        doctor_id=appointment_data.doctor_id,
        appointment_date=appointment_data.appointment_date,
        appointment_time=appointment_data.appointment_time,
        reason=appointment_data.reason,
        notes=appointment_data.notes
    )

    db.add(appointment)
    db.commit()
    db.refresh(appointment)

    return appointment

#List Function
def get_all_appointments(
    db: Session,
    user,
    page: int = 1,
    limit: int = 5
):
    query = db.query(Appointment)

    if user.role == "doctor":

        doctor = db.query(Doctor).filter(
            Doctor.email == user.email
        ).first()

        if doctor:
            query = query.filter(
                Appointment.doctor_id == doctor.id
            )

    elif user.role == "patient":

        patient = db.query(Patient).filter(
            Patient.email == user.email
        ).first()

        if patient:
            query = query.filter(
                Appointment.patient_id == patient.id
            )

    offset = (page - 1) * limit

    return query.offset(offset).limit(limit).all()

#GET by ID Fucntion
def get_appointment_by_id(
    db: Session,
    appointment_id: int,
    user
):
    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()

    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    if user.role == "doctor":

        doctor = db.query(Doctor).filter(
            Doctor.email == user.email
        ).first()

        if not doctor or (
            appointment.doctor_id != doctor.id
        ):
            raise HTTPException(
                status_code=403,
                detail="Access denied"
            )

    elif user.role == "patient":

        patient = db.query(Patient).filter(
            Patient.email == user.email
        ).first()

        if not patient or (
            appointment.patient_id != patient.id
        ):
            raise HTTPException(
                status_code=403,
                detail="Access denied"
            )

    return appointment



#Updating Appointments
def update_appointment(
    db: Session,
    appointment_id: int,
    appointment_data
):
    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()

    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    overlapping = db.query(Appointment).filter(
        Appointment.doctor_id == appointment.doctor_id,
        Appointment.appointment_date == appointment_data.appointment_date,
        Appointment.appointment_time == appointment_data.appointment_time,
        Appointment.id != appointment_id,
        Appointment.status != "cancelled"
    ).first()

    if overlapping:
        raise HTTPException(
            status_code=400,
            detail="Doctor already has appointment at this time"
        )

    appointment.appointment_date = (
        appointment_data.appointment_date
    )

    appointment.appointment_time = (
        appointment_data.appointment_time
    )

    appointment.reason = appointment_data.reason

    appointment.status = appointment_data.status

    appointment.notes = appointment_data.notes

    db.commit()
    db.refresh(appointment)

    return appointment


#Cancel Appointments
def cancel_appointment(
    db: Session,
    appointment_id: int
):
    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()

    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    appointment.status = "cancelled"

    db.commit()

    return {
        "message": "Appointment cancelled successfully"
    }