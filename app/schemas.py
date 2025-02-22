from pydantic import BaseModel, EmailStr, constr
from enum import Enum


class UserRole(str, Enum):
    nutritionist = "nutritionist"
    kindergarten_teacher = "kindergarten_teacher"
    daycare_teacher = "daycare_teacher"


class UserCreate(BaseModel):
    email: EmailStr
    password: constr(min_length=8)
    role: UserRole


class UserResponse(BaseModel):
    id: str
    email: str
    role: UserRole
    created_at: str

    class Config:
        orm_mode = True
