from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Order, Meal, User
from app.schemas import OrderCreate, OrderResponse
from app.database import get_db
import uuid

router = APIRouter()


@router.post("/", response_model=OrderResponse)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == order.user_id).first()
    meal = db.query(Meal).filter(Meal.id == order.meal_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not meal:
        raise HTTPException(status_code=404, detail="Meal not found")

    new_order = Order(
        id=uuid.uuid4(),
        user_id=order.user_id,
        meal_id=order.meal_id,
        quantity=order.quantity,
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return new_order
