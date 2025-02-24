from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Meal
from app.schemas import MealCreate, MealResponse
from app.database import get_db
import uuid

router = APIRouter()


@router.post("/", response_model=MealResponse)
def create_meal(meal: MealCreate, db: Session = Depends(get_db)):
    new_meal = Meal(
        id=uuid.uuid4(),
        name=meal.name,
        description=meal.description,
        calories=meal.calories,
    )

    db.add(new_meal)
    db.commit()
    db.refresh(new_meal)

    return new_meal


@router.get("/{meal_id}", response_model=MealResponse)
def get_meal(meal_id: uuid.UUID, db: Session = Depends(get_db)):
    meal = db.query(Meal).filter(Meal.id == meal_id).first()
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")
    return meal
