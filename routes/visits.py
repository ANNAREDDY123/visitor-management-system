from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session
from datetime import date

from database import SessionLocal

from models.visit import Visit
from models.visitor import Visitor

from schemas.visit import VisitCreate

from services.visit_service import valid_visit_time

router = APIRouter(
    prefix="/visits",
    tags=["Visits"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/")
def create_visit(
    visit: VisitCreate,
    db: Session = Depends(get_db)
):

    visitor = db.query(Visitor).filter(
        Visitor.id == visit.visitor_id
    ).first()

    if not visitor:

        raise HTTPException(
            status_code=404,
            detail="Visitor not found"
        )

    if not valid_visit_time(
        visit.check_in,
        visit.check_out
    ):

        raise HTTPException(
            status_code=400,
            detail="Check-out must be greater than check-in"
        )

    active_visit = db.query(Visit).filter(
        Visit.visitor_id == visit.visitor_id,
        Visit.status.in_(["Scheduled", "Checked In"])
    ).first()

    if active_visit:

        raise HTTPException(
            status_code=400,
            detail="Visitor already has an active visit"
        )

    new_visit = Visit(
        visitor_id=visit.visitor_id,
        host_name=visit.host_name,
        department=visit.department,
        visit_date=visit.visit_date,
        check_in=visit.check_in,
        check_out=visit.check_out,
        status="Scheduled"
    )

    db.add(new_visit)

    db.commit()

    db.refresh(new_visit)

    return new_visit


@router.get("/")
def get_visits(
    visit_date: str = None,
    status: str = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):

    query = db.query(Visit)

    if visit_date:
        query = query.filter(
            Visit.visit_date == visit_date
        )

    if status:
        query = query.filter(
            Visit.status == status
        )

    total = query.count()

    visits = query.offset(
        (page - 1) * limit
    ).limit(limit).all()

    return {
        "total_records": total,
        "current_page": page,
        "limit": limit,
        "data": visits
    }


@router.get("/{visit_id}")
def get_visit(
    visit_id: int,
    db: Session = Depends(get_db)
):

    visit = db.query(Visit).filter(
        Visit.id == visit_id
    ).first()

    if not visit:

        raise HTTPException(
            status_code=404,
            detail="Visit not found"
        )

    return visit


@router.put("/{visit_id}")
def update_visit(
    visit_id: int,
    visit: VisitCreate,
    db: Session = Depends(get_db)
):

    db_visit = db.query(Visit).filter(
        Visit.id == visit_id
    ).first()

    if not db_visit:

        raise HTTPException(
            status_code=404,
            detail="Visit not found"
        )

    if not valid_visit_time(
        visit.check_in,
        visit.check_out
    ):

        raise HTTPException(
            status_code=400,
            detail="Invalid visit time"
        )

    db_visit.visitor_id = visit.visitor_id
    db_visit.host_name = visit.host_name
    db_visit.department = visit.department
    db_visit.visit_date = visit.visit_date
    db_visit.check_in = visit.check_in
    db_visit.check_out = visit.check_out

    db.commit()

    return {
        "message": "Visit updated"
    }


@router.get("/reports/today")
def today_visitors(
    db: Session = Depends(get_db)
):

    return db.query(Visit).filter(
        Visit.visit_date == date.today()
    ).all()
