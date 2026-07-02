from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Time,
    ForeignKey
)

from database import Base


class Visit(Base):
    __tablename__ = "visits"

    id = Column(
        Integer,
        primary_key=True
    )

    visitor_id = Column(
        Integer,
        ForeignKey("visitors.id")
    )

    host_name = Column(String)

    department = Column(String)

    visit_date = Column(Date)

    check_in = Column(Time)

    check_out = Column(Time)

    status = Column(
        String,
        default="Scheduled")
