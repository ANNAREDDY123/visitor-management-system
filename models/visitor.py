from sqlalchemy import (
    Column,
    Integer,
    String
)

from database import Base


class Visitor(Base):
    __tablename__ = "visitors"

    id = Column(
        Integer,
        primary_key=True
    )

    name = Column(String)

    phone = Column(String)

    email = Column(
        String,
        unique=True
    )

    company = Column(String)

    purpose_of_visit = Column(String)
