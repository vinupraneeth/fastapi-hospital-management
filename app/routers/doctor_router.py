from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.dependencies.auth import require_admin, get_current_user

from app.schemas.doctor import (
    DoctorCreate,
    DoctorUpdate,
    DoctorResponse
)
from app.schemas.patient import PatientResponse

from app.services import doctor_service

from app.models.doctor import Doctor

router = APIRouter(
    prefix="/doctors",
    tags=["Doctors"]
)


@router.post(
    "",
    response_model=DoctorResponse
)
def create_doctor(
    request: DoctorCreate,
    db: Session = Depends(get_db),
    user=Depends(require_admin)
):
    return doctor_service.create_doctor(db, request)


@router.get(
    "",
    response_model=list[DoctorResponse]
)
def get_doctors(
    db: Session = Depends(get_db)
):
    return doctor_service.get_all_doctors(db)


@router.get(
    "/{doctor_id}",
    response_model=DoctorResponse
)
def get_doctor(
    doctor_id: int,
    db: Session = Depends(get_db)
):
    return doctor_service.get_doctor_by_id(db, doctor_id)


@router.post(
    "/{doctor_id}/patients/{patient_id}"
)
def assign_patient(
    doctor_id: int,
    patient_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_admin)
):
    return doctor_service.assign_patient_to_doctor(
        db,
        doctor_id,
        patient_id
    )


@router.get(
    "/{doctor_id}/patients",
    response_model=list[PatientResponse]
)
def get_doctor_patients(
    doctor_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    if user.role == "doctor":

        doctor = db.query(Doctor).filter(
            Doctor.email == user.email
        ).first()

        if not doctor:
            raise HTTPException(
                status_code=404,
                detail="Doctor profile not found"
            )

        if doctor.id != doctor_id:
            raise HTTPException(
                status_code=403,
                detail="Access denied"
            )

    return doctor_service.get_doctor_patients(
        db,
        doctor_id
    )

@router.put(
    "/{doctor_id}",
    response_model=DoctorResponse
)
def update_doctor(
    doctor_id: int,
    request: DoctorUpdate,
    db: Session = Depends(get_db),
    user = Depends(require_admin)
):
    return doctor_service.update_doctor(
        db,
        doctor_id,
        request
    )

@router.delete(
    "/{doctor_id}"
)
def delete_doctor(
    doctor_id: int,
    db: Session = Depends(get_db),
    user = Depends(require_admin)
):
    return doctor_service.soft_delete_doctor(
        db,
        doctor_id
    )