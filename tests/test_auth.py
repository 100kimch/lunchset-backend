import pytest
import uuid
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    """ 회원가입 API 테스트 (항상 새로운 이메일 사용) """
    unique_email = f"test_{uuid.uuid4().hex}@example.com"  # ✅ 항상 새로운 이메일 생성
    response = await client.post("/auth/register", json={
        "email": unique_email,
        "password": "password123",
        "role": "kindergarten_teacher",
        "age": 30,
        "institution": "Test School"
    })
    assert response.status_code == 200, response.text
    assert response.json()["email"] == unique_email
    return unique_email  # ✅ 이후 테스트에서 사용하기 위해 이메일 반환

@pytest.mark.asyncio
async def test_login_user(client: AsyncClient):
    """ 로그인 API 테스트 (회원가입 후 실행) """
    email = await test_register_user(client)  # ✅ 회원가입 먼저 실행 후 해당 이메일로 로그인

    response = await client.post("/auth/login", data={
        "username": email,
        "password": "password123"
    })

    assert response.status_code == 200, response.text
    assert "access_token" in response.json()
    return response.json()["access_token"]  # ✅ 이후 테스트에서 사용하기 위해 토큰 반환

@pytest.mark.asyncio
async def test_get_user_details(client: AsyncClient):
    """ 유저 정보 조회 API 테스트 """
    token = await test_login_user(client)  # ✅ 로그인 먼저 실행하여 토큰 확보
    assert token is not None, "Login failed, token not found."

    response = await client.get("/auth/show-detail", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200, response.text

@pytest.mark.asyncio
async def test_update_user_details(client: AsyncClient):
    """ 유저 정보 업데이트 API 테스트 """
    token = await test_login_user(client)  # ✅ 로그인 먼저 실행하여 토큰 확보
    assert token is not None, "Login failed, token not found."

    response = await client.put("/auth/show-detail", headers={"Authorization": f"Bearer {token}"}, json={
        "age": 35,
        "institution": "Updated School"
    })
    assert response.status_code == 200
    assert response.json()["age"] == 35
    assert response.json()["institution"] == "Updated School"

@pytest.mark.asyncio
async def test_delete_user(client: AsyncClient):
    """ 계정 삭제 API 테스트 """
    token = await test_login_user(client)  # ✅ 로그인 먼저 실행하여 토큰 확보
    assert token is not None, "Login failed, token not found."

    response = await client.delete("/auth/delete", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["message"] == "User deleted successfully"
