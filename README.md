# Hospital Backend System - FastAPI

## Overview

This project is a backend application built using FastAPI for managing doctors and patients with JWT-based authentication and role-based authorization.

The system supports:
- User authentication
- Admin and Doctor roles
- Doctor management
- Patient management
- Doctor-patient assignment
- Protected APIs using JWT

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

# Features

## Authentication
- Register API
- Login API
- JWT token generation
- Protected routes

## Authorization
- Admin-only APIs
- Doctors can only view their own patients

## Doctor Management
- Create doctor
- List doctors
- Get doctor details
- Update doctor
- Soft delete doctor

## Patient Management
- Create patient
- List patients
- Get patient details

## Doctor-Patient Assignment
- Assign patient to doctor
- Fetch doctor patients

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

## 4. Run Application

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

# Environment Variables

Create `.env` file:

```env
DATABASE_URL=sqlite:///./hospital.db
SECRET_KEY=secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

# Authentication Flow

1. Register user
2. Login using credentials
3. Receive JWT token
4. Authorize using token in Swagger
5. Access protected APIs

---

# Roles

## Admin
- Manage doctors
- Manage patients
- Assign patients

## Doctor
- View only their assigned patients

---

# Validation Rules

- Unique email validation
- Age must be greater than 0
- Phone number must contain 10-15 digits

---

# Soft Delete

Doctor deletion is implemented using soft delete:
```text
is_active = False
```

instead of removing records from the database.
