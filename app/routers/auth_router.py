from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.auth import RegisterRequest, LoginRequest
from app.dependencies.db import get_db
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    return auth_service.register_user(db, request.email, request.password, request.role)

@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    return auth_service.login_user(db, request.email, request.password)