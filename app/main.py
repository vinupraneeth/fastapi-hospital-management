from fastapi import FastAPI
from app.db.session import engine
from app.db.base import Base
from app.models import user
from app.models import doctor
from app.routers import doctor_router
from app.models import patient
from app.models import association

# import model so SQLAlchemy knows it exists
from app.models import test  

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Backend is running"}

from fastapi import Depends
from sqlalchemy.orm import Session
from app.dependencies.db import get_db

@app.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    return {"status": "DB working"}

from app.routers import auth_router

app.include_router(auth_router.router)

from fastapi import Depends
from app.dependencies.auth import get_current_user

@app.get("/protected")
def protected_route(user = Depends(get_current_user)):
    return {
        "message": "Authenticated user",
        "email": user.email,
        "role": user.role
    }

from app.dependencies.auth import require_admin

@app.get("/admin-only")
def admin_route(user = Depends(require_admin)):
    return {
        "message": "Welcome Admin",
        "email": user.email
    }

app.include_router(doctor_router.router)

from app.routers import patient_router

app.include_router(patient_router.router)