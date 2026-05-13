from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.dependencies.auth import get_current_user

from app.schemas.appointment import (
    AppointmentCreate,
    AppointmentUpdate,
    AppointmentResponse
)

from app.services import appointment_service

#Creating Router
router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"]
)

#Appointment Booking API
@router.post(
    "",
    response_model=AppointmentResponse
)
def create_appointment(
    request: AppointmentCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return appointment_service.create_appointment(
        db,
        request
    )

#Appointments List API
@router.get(
    "",
    response_model=list[AppointmentResponse]
)
def get_appointments(
    page: int = 1,
    limit: int = 5,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return appointment_service.get_all_appointments(
        db,
        user,
        page,
        limit
    )

#GET Appoinmtent API
@router.get(
    "/{appointment_id}",
    response_model=AppointmentResponse
)
def get_appointment(
    appointment_id: int,
    db: Session = Depends(get_db)
):
    return appointment_service.get_appointment_by_id(
        db,
        appointment_id
    )

#Update Appoinment API
@router.put(
    "/{appointment_id}",
    response_model=AppointmentResponse
)
def update_appointment(
    appointment_id: int,
    request: AppointmentUpdate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return appointment_service.update_appointment(
        db,
        appointment_id,
        request
    )

#Delete Appointment API
@router.delete(
    "/{appointment_id}"
)
def cancel_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return appointment_service.cancel_appointment(
        db,
        appointment_id
    )