from fastapi import FastAPI
from routes import auth
from routers import orders, meals

app = FastAPI()

app.include_router(orders.router, prefix="/orders", tags=["Orders"])
app.include_router(meals.router, prefix="/meals", tags=["Meals"])


@app.get("/")
def read_root():
    return {"message": "Welcome to Kindergarten Meal API"}
