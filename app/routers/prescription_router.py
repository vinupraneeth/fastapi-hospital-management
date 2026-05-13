from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.dependencies.auth import (
    get_current_user
)

from app.schemas.prescription import (
    PrescriptionCreate,
    PrescriptionResponse
)

from app.services import prescription_service


#Create Router
router = APIRouter(
    prefix="/prescriptions",
    tags=["Prescriptions"]
)

#Prescription API
@router.post(
    "",
    response_model=PrescriptionResponse
)
def create_prescription(
    request: PrescriptionCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    if user.role != "doctor":
        raise HTTPException(
            status_code=403,
            detail="Only doctors can create prescriptions"
        )

    return prescription_service.create_prescription(
        db,
        request
    )

#Listing API
@router.get(
    "",
    response_model=list[PrescriptionResponse]
)
def get_prescriptions(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return prescription_service.get_all_prescriptions(
        db,
        user
    )

#Get by ID API
@router.get(
    "/{prescription_id}",
    response_model=PrescriptionResponse
)
def get_prescription(
    prescription_id: int,
    db: Session = Depends(get_db)
):
    return prescription_service.get_prescription_by_id(
        db,
        prescription_id
    )