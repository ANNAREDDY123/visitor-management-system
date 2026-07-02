from pydantic import (
    BaseModel,
    EmailStr
)


class VisitorCreate(BaseModel):

    name: str

    phone: str

    email: EmailStr

    company: str

    purpose_of_visit: str
