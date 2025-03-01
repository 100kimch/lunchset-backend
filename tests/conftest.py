import pytest
import asyncio
from httpx import AsyncClient
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """ 테스트 전 DB 초기화 및 테이블 생성 """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def event_loop():
    """ module 스코프의 asyncio 이벤트 루프 설정 (pytest-asyncio 0.25 버전 스타일) """
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="module")
def test_client():
    """ FastAPI TestClient를 생성하여 Lifespan을 자동 실행 """
    with TestClient(app) as client:
        yield client

@pytest.fixture(scope="module")
async def client(test_client):
    """ 비동기 HTTP 요청을 위한 AsyncClient 반환 """
    async with AsyncClient(base_url="http://localhost:8000") as ac:
        yield ac
