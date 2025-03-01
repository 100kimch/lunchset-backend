from enum import Enum
from typing import Annotated  # ✅ Enum을 명확히 임포트
from pydantic import BaseModel, ConfigDict, EmailStr, constr
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
    model_config = ConfigDict(from_attributes=True)


# 발주 (Order) 스키마
class OrderCreate(BaseModel):
    user_id: UUID
    meal_id: UUID
    quantity: int


class OrderResponse(OrderCreate):
    id: UUID
    order_date: datetime
    model_config = ConfigDict(from_attributes=True)


# 사용자 역할 Enum
class UserRole(str, Enum):
    nutritionist = "nutritionist"
    kindergarten_teacher = "kindergarten_teacher"
    daycare_teacher = "daycare_teacher"


# 회원가입 요청 스키마
class UserCreate(BaseModel):
    email: EmailStr
    password: Annotated[str, ...]
    role: UserRole
    age: int | None = None  # ✅ 연령 추가
    institution: str | None = None  # ✅ 유치원(학교) 추가


# 로그인 요청 스키마
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# 유저 상세 조회 및 수정 스키마
class UserUpdate(BaseModel):
    role: UserRole | None = None
    age: int | None = None
    institution: str | None = None


# 유저 응답 스키마
class UserResponse(BaseModel):
    id: UUID
    email: str
    role: UserRole
    age: int | None = None
    institution: str | None = None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)