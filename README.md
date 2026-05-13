# Hospital Backend System - FastAPI

## Overview

This project is a backend application built using FastAPI for managing doctors, patients, appointments, and prescriptions in a clinic workflow system.

The application includes JWT-based authentication, role-based authorization, appointment scheduling, prescription management, and workflow validations commonly used in real-world healthcare systems.

---

# Features

## Authentication & Authorization
- User registration and login
- JWT token generation and validation
- Protected APIs
- Role-based access control

Supported roles:
- Admin
- Doctor
- Patient

---

# Doctor Management
- Create doctor
- List doctors
- Get doctor details
- Update doctor
- Soft delete doctor

---

# Patient Management
- Create patient
- List patients
- Get patient details

---

# Appointment Management
- Book appointments
- View appointments
- Update appointments
- Cancel appointments
- Pagination support

Business validations:
- Past appointments are not allowed
- Doctors cannot have overlapping appointments
- Appointment status validation
- Cancelled appointments are excluded from overlap checks

---

# Prescription Management
- Create prescription
- List prescriptions
- Get prescription details

Business validations:
- Prescription can only be created for completed appointments
- Cancelled appointments cannot have prescriptions
- Duplicate prescriptions for same appointment are blocked

---

# Role-Based Access

## Admin
- View all doctors, patients, appointments, and prescriptions
- Manage doctors and patients

## Doctor
- View own appointments
- Create prescriptions
- View own prescriptions and patients

## Patient
- Book appointments
- View own appointments
- View own prescriptions

---

# Tech Stack

- Python 3.13
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- JWT Authentication
- Uvicorn

---

# Project Structure

```text
app/
│
├── core/
├── db/
├── dependencies/
├── models/
├── routers/
├── schemas/
├── services/
└── main.py
```

---

# API Modules

## Authentication APIs

| Method | Endpoint | Description |
|---|---|---|
| POST | /auth/register | Register user |
| POST | /auth/login | Login user |

---

## Doctor APIs

| Method | Endpoint | Description |
|---|---|---|
| POST | /doctors | Create doctor |
| GET | /doctors | List doctors |
| GET | /doctors/{id} | Get doctor details |
| PUT | /doctors/{id} | Update doctor |
| DELETE | /doctors/{id} | Soft delete doctor |

---

## Patient APIs

| Method | Endpoint | Description |
|---|---|---|
| POST | /patients | Create patient |
| GET | /patients | List patients |
| GET | /patients/{id} | Get patient details |

---

## Appointment APIs

| Method | Endpoint | Description |
|---|---|---|
| POST | /appointments | Book appointment |
| GET | /appointments | List appointments |
| GET | /appointments/{id} | Get appointment details |
| PUT | /appointments/{id} | Update appointment |
| DELETE | /appointments/{id} | Cancel appointment |

Pagination example:

```text
/appointments?page=1&limit=5
```

---

## Prescription APIs

| Method | Endpoint | Description |
|---|---|---|
| POST | /prescriptions | Create prescription |
| GET | /prescriptions | List prescriptions |
| GET | /prescriptions/{id} | Get prescription details |

---

# Setup Instructions

## 1. Clone Repository

```bash
git clone https://github.com/vinupraneeth/fastapi-hospital-management.git
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate virtual environment:

### Windows
```bash
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Create `.env` File

```env
DATABASE_URL=sqlite:///./hospital.db
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## 5. Run Application

```bash
uvicorn app.main:app --reload
```

---

# Swagger Documentation

Open:

```text
http://127.0.0.1:8000/docs
```

---

# Authentication Flow

1. Register user
2. Login using email and password
3. Receive JWT token
4. Authorize using Swagger Authorize button
5. Access protected APIs

---

# Validation Rules

- Unique email validation
- Age must be greater than 0
- Phone number must contain 10–15 digits
- Appointment date cannot be in the past
- Doctor overlap prevention for appointments
- Valid appointment status enforcement

---

# Soft Delete

Doctor deletion is implemented using soft delete:

```text
is_active = False
```

instead of permanently removing records from the database.

---

# Notes

- SQLite is used for local development
- JWT authentication is implemented using python-jose
- Password hashing is implemented using passlib and bcrypt
- Pagination support is implemented for appointments