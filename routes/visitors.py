from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from database import SessionLocal

from models.visitor import Visitor

from schemas.visitor import VisitorCreate

from services.visit_service import valid_phone

router = APIRouter(
    prefix="/visitors",
    tags=["Visitors"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/")
def create_visitor(
    visitor: VisitorCreate,
    db: Session = Depends(get_db)
):

    existing = db.query(Visitor).filter(
        Visitor.email == visitor.email
    ).first()

    if existing:

        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    if not valid_phone(visitor.phone):

        raise HTTPException(
            status_code=400,
            detail="Invalid phone number"
        )

    new_visitor = Visitor(
        name=visitor.name,
        phone=visitor.phone,
        email=visitor.email,
        company=visitor.company,
        purpose_of_visit=visitor.purpose_of_visit
    )

    db.add(new_visitor)

    db.commit()

    db.refresh(new_visitor)

    return new_visitor


@router.get("/")
def get_visitors(
    name: str = None,
    phone: str = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):

    query = db.query(Visitor)

    if name:
        query = query.filter(
            Visitor.name.contains(name)
        )

    if phone:
        query = query.filter(
            Visitor.phone.contains(phone)
        )

    total = query.count()

    visitors = query.offset(
        (page - 1) * limit
    ).limit(limit).all()

    return {
        "total_records": total,
        "current_page": page,
        "limit": limit,
        "data": visitors
    }


@router.get("/{visitor_id}")
def get_visitor(
    visitor_id: int,
    db: Session = Depends(get_db)
):

    visitor = db.query(Visitor).filter(
        Visitor.id == visitor_id
    ).first()

    if not visitor:

        raise HTTPException(
            status_code=404,
            detail="Visitor not found"
        )

    return visitor


@router.put("/{visitor_id}")
def update_visitor(
    visitor_id: int,
    visitor: VisitorCreate,
    db: Session = Depends(get_db)
):

    db_visitor = db.query(Visitor).filter(
        Visitor.id == visitor_id
    ).first()

    if not db_visitor:

        raise HTTPException(
            status_code=404,
            detail="Visitor not found"
        )

    db_visitor.name = visitor.name
    db_visitor.phone = visitor.phone
    db_visitor.email = visitor.email
    db_visitor.company = visitor.company
    db_visitor.purpose_of_visit = visitor.purpose_of_visit

    db.commit()

    return {
        "message": "Visitor updated"
    }


@router.delete("/{visitor_id}")
def delete_visitor(
    visitor_id: int,
    db: Session = Depends(get_db)
):

    visitor = db.query(Visitor).filter(
        Visitor.id == visitor_id
    ).first()

    if not visitor:

        raise HTTPException(
            status_code=404,
            detail="Visitor not found"
        )

    db.delete(visitor)

    db.commit()

    return {
        "message": "Visitor deleted" }
