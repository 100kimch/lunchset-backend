from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def get_meals():
    return {"meals": ["Meal 1", "Meal 2"]}
