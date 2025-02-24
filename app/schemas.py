from enum import Enum  # ✅ Enum을 명확히 임포트
from pydantic import BaseModel, EmailStr, constr
from datetime import datetime
from uuid import UUID


# 식단 (Meal) 스키마
class MealCreate(BaseModel):
    name: str
    description: str | None = None
    calories: int | None = None


class MealResponse(MealCreate):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True


# 발주 (Order) 스키마
class OrderCreate(BaseModel):
    user_id: UUID
    meal_id: UUID
    quantity: int


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


class OrderResponse(OrderCreate):
    id: UUID
    order_date: datetime

    class Config:
        orm_mode = True
