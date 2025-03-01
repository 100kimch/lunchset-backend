from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routes import auth, meals, orders
from app.database import engine, Base

# ✅ Lifespan 컨텍스트 매니저 추가
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Lifespan startup")  # ✅ 앱이 시작될 때 실행
    yield
    print("Lifespan shutdown")  # ✅ 앱이 종료될 때 실행

app = FastAPI(lifespan=lifespan)  # ✅ Lifespan 적용

# DB 테이블 생성
Base.metadata.create_all(bind=engine)

# 라우트 추가
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(meals.router, prefix="/meals", tags=["Meals"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"])


@app.get("/")
def root():
    return {"message": "Welcome to Kindergarten Meal API"}
