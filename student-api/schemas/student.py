from pydantic import BaseModel, ConfigDict


class StudentCreate(BaseModel):
    id: int
    name: str
    email: str
    password: str


class StudentUpdate(BaseModel):
    name: str
    email: str


class StudentOut(BaseModel):
    """Response model — never exposes the password hash."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
