from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.dependencies.auth import require_admin

from app.schemas.patient import (
    PatientCreate,
    PatientResponse
)

from app.services import patient_service

router = APIRouter(
    prefix="/patients",
    tags=["Patients"]
)

@router.post(
    "",
    response_model=PatientResponse
)
def create_patient(
    request: PatientCreate,
    db: Session = Depends(get_db),
    user = Depends(require_admin)
):
    return patient_service.create_patient(db, request)

@router.get(
    "",
    response_model=list[PatientResponse]
)
def get_patients(
    db: Session = Depends(get_db)
):
    return patient_service.get_all_patients(db)

@router.get(
    "/{patient_id}",
    response_model=PatientResponse
)
def get_patient(
    patient_id: int,
    db: Session = Depends(get_db)
):
    return patient_service.get_patient_by_id(db, patient_id)

