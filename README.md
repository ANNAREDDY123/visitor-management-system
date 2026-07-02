# visitor-management-system
FastAPI Visitor Management System with JWT Authentication, Visitor Management, Visit Scheduling, Reports, Search, SQLAlchemy ORM, Pagination, and Docker Support.
# Visitor Management System

## Features

- JWT Authentication
- Visitor Management
- Visit Scheduling
- Reports & Search
- Filtering & Pagination
- SQLAlchemy ORM
- SQLite Database
- Docker Support

## Setup Instructions

1. Install dependencies

```bash
pip install -r requirements.txt
```

2. Run the application

```bash
uvicorn main:app --reload
```

## Environment Variables

```
SECRET_KEY=visitor_secret_key
ALGORITHM=HS256
```

## Authentication Flow

- Register using `/auth/register`
- Login using `/auth/login`
- JWT token is returned after successful login.

## API Flow Overview

1. Register/Login
2. Create Visitors
3. Schedule Visits
4. View Visits
5. Update Visits
6. View Today's Visitors

## Assumptions Made

- One visitor can have multiple visits.
- Duplicate active visits are not allowed.
- Check-out time must always be greater than check-in time.
- Visitor email must be unique.
