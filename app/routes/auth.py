from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import Column
from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserCreate, UserResponse, UserLogin, UserUpdate
from app.database import get_db
import uuid

# JWT 설정
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# 비밀번호 해싱 설정
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 비밀번호 기반 로그인 방식 사용
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# FastAPI 라우터 생성
router = APIRouter()

# ✅ 비밀번호 해싱
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# ✅ 비밀번호 검증
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# ✅ JWT 토큰 생성
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# ✅ JWT 토큰 검증
def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

# ✅ 회원가입 API
@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")  # ✅ 중복된 이메일 예외 메시지 명확히 설정

    hashed_password = hash_password(user.password)

    new_user = User(
        id=uuid.uuid4(),
        email=user.email,
        password_hash=hashed_password,
        role=user.role,
        age=user.age,
        institution=user.institution
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# ✅ 로그인 API (JWT 토큰 반환)
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")  # ✅ 사용자 없을 때 메시지 변경

    if not verify_password(form_data.password, str(user.password_hash)):
        raise HTTPException(status_code=401, detail="Incorrect password")  # ✅ 비밀번호 오류 메시지 변경

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}

# ✅ 현재 사용자 정보 조회
@router.get("/show-detail", response_model=UserResponse)
def show_user_detail(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = verify_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.id == payload["sub"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

# ✅ 사용자 정보 업데이트 API
@router.put("/show-detail", response_model=UserResponse)
def update_user_detail(update_data: UserUpdate, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = verify_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.id == payload["sub"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # ✅ 필드 값이 None이 아닐 때만 업데이트
    if update_data.role is not None:
        setattr(user, "role", update_data.role)
    if update_data.age is not None:
        setattr(user, "age", update_data.age)
    if update_data.institution is not None:
        setattr(user, "institution", update_data.institution)

    try:
        db.commit()
        db.refresh(user)
    except Exception as e:
        db.rollback()  # ✅ 오류 발생 시 롤백
        raise HTTPException(status_code=500, detail=str(e))  # ✅ FastAPI에서 오류 메시지를 명확하게 반환

    return user

# ✅ 계정 삭제 API
@router.delete("/delete")
def delete_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = verify_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.id == payload["sub"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
