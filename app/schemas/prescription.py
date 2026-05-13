from pydantic import BaseModel
from datetime import datetime


class PrescriptionCreate(BaseModel):
    appointment_id: int
    doctor_id: int
    patient_id: int
    diagnosis: str
    medicines: str
    dosage_instructions: str
    remarks: str | None = None


class PrescriptionResponse(BaseModel):
    id: int
    appointment_id: int
    doctor_id: int
    patient_id: int
    diagnosis: str
    medicines: str
    dosage_instructions: str
    remarks: str | None
    created_at: datetime

    class Config:
        from_attributes = True