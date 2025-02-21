from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def get_orders():
    return {"orders": ["Order 1", "Order 2"]}
