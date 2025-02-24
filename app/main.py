from fastapi import FastAPI
from app.routes import auth, meals, orders
from app.database import engine, Base

app = FastAPI()

# DB 테이블 생성
Base.metadata.create_all(bind=engine)

# 라우트 추가
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(meals.router, prefix="/meals", tags=["Meals"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"])


@app.get("/")
def root():
    return {"message": "Welcome to Kindergarten Meal API"}
