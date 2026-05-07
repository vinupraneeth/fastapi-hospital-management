from pydantic import BaseModel, field_validator
import re


class PatientCreate(BaseModel):
    name: str
    age: int
    phone: str

    @field_validator("age")
    @classmethod
    def validate_age(cls, value):
        if value <= 0:
            raise ValueError("Age must be greater than 0")
        return value

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):
        if not re.fullmatch(r"^[0-9]{10,15}$", value):
            raise ValueError("Phone number must be 10-15 digits")
        return value


class PatientResponse(BaseModel):
    id: int
    name: str
    age: int
    phone: str

    class Config:
        from_attributes = True