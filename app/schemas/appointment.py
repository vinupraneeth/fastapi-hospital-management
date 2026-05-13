from pydantic import BaseModel, field_validator
from datetime import date, time, datetime


VALID_STATUSES = [
    "scheduled",
    "completed",
    "cancelled"
]


class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_date: date
    appointment_time: time
    reason: str
    notes: str | None = None

    @field_validator("appointment_date")
    @classmethod
    def validate_date(cls, value):

        if value < date.today():
            raise ValueError(
                "Appointment date cannot be in the past"
            )

        return value


class AppointmentUpdate(BaseModel):
    appointment_date: date
    appointment_time: time
    reason: str
    status: str
    notes: str | None = None

    @field_validator("status")
    @classmethod
    def validate_status(cls, value):

        if value not in VALID_STATUSES:
            raise ValueError(
                "Invalid appointment status"
            )

        return value


class AppointmentResponse(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    appointment_date: date
    appointment_time: time
    reason: str
    status: str
    notes: str | None
    created_at: datetime

    class Config:
        from_attributes = True