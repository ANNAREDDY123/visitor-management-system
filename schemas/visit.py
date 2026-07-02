from pydantic import BaseModel
from datetime import date, time


class VisitCreate(BaseModel):

    visitor_id: int

    host_name: str

    department: str

    visit_date: date

    check_in: time

    check_out: time
