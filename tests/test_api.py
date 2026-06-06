import pytest
from fastapi.testclient import TestClient

from my_project.main import app
from my_project.services.user import USERS_DB


@pytest.fixture(autouse=True)
def clean_db():
    """每次测试前清空模拟内存数据库，并重置计数器。"""
    USERS_DB.clear()
    import my_project.services.user as user_module

    user_module._id_counter = 0
    yield


client = TestClient(app)


def test_health_check():
    """测试健康检查端点。"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "user-api"}


def test_create_user_success():
    """测试成功创建用户。"""
    # Arrange
    payload = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "strongpassword",
    }

    # Act
    response = client.post("/api/v1/users/", json=payload)

    # Assert
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "password" not in data  # 确保返回模型中过滤掉了密码
    assert data["is_active"] is True


def test_create_user_invalid_data():
    """测试创建用户时输入非法数据（触发 Pydantic 校验失败）。"""
    # Arrange: 邮箱格式错误，密码太短，用户名太短
    payload = {
        "username": "tu",
        "email": "invalid-email",
        "password": "123",
    }

    # Act
    response = client.post("/api/v1/users/", json=payload)

    # Assert
    assert response.status_code == 422  # Unprocessable Entity
    errors = response.json()["detail"]
    assert len(errors) >= 3  # username 长度不足, email 不合法, password 长度不足


def test_create_duplicate_email():
    """测试使用已注册的邮箱创建用户（触发业务异常）。"""
    # Arrange
    payload1 = {
        "username": "user1",
        "email": "same@example.com",
        "password": "password123",
    }
    payload2 = {
        "username": "user2",
        "email": "same@example.com",
        "password": "password456",
    }
    client.post("/api/v1/users/", json=payload1)

    # Act
    response = client.post("/api/v1/users/", json=payload2)

    # Assert
    assert response.status_code == 400
    data = response.json()
    assert data["error_code"] == "EMAIL_ALREADY_EXISTS"
    assert "same@example.com" in data["detail"]


def test_get_user_not_found():
    """测试获取不存在的用户（触发 404 业务异常）。"""
    # Act
    response = client.get("/api/v1/users/999")

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert data["error_code"] == "USER_NOT_FOUND"


def test_get_user_success():
    """测试成功获取用户详情。"""
    # Arrange
    payload = {
        "username": "getuser",
        "email": "get@example.com",
        "password": "password123",
    }
    create_res = client.post("/api/v1/users/", json=payload)
    user_id = create_res.json()["id"]

    # Act
    response = client.get(f"/api/v1/users/{user_id}")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["username"] == "getuser"
    assert data["email"] == "get@example.com"


def test_update_user_success():
    """测试更新用户信息。"""
    # Arrange
    payload = {
        "username": "updateuser",
        "email": "old@example.com",
        "password": "password123",
    }
    create_res = client.post("/api/v1/users/", json=payload)
    user_id = create_res.json()["id"]

    # Act
    update_payload = {
        "username": "newusername",
        "email": "new@example.com",
    }
    response = client.put(f"/api/v1/users/{user_id}", json=update_payload)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["username"] == "newusername"
    assert data["email"] == "new@example.com"
