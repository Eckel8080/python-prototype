from fastapi.testclient import TestClient
from pytest_mock import MockerFixture

from my_project.app import app


def make_user_create_payload(
    username: str = "testuser",
    email: str = "test@example.com",
    password: str = "strongpassword",
) -> dict[str, str]:
    """测试数据工厂：生成创建用户的请求 Payload 字典。"""
    return {
        "username": username,
        "email": email,
        "password": password,
    }


class TestUsersAPI:
    """用户 API 端点的集成测试类。"""

    def test_create_user_success(self) -> None:
        """测试成功创建用户。"""
        # Arrange
        client = TestClient(app)
        payload = make_user_create_payload()

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

    def test_create_user_invalid_data(self) -> None:
        """测试创建用户时输入非法数据（触发 Pydantic 校验失败）。"""
        # Arrange: 邮箱格式错误，密码太短，用户名太短
        client = TestClient(app)
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
        assert len(errors) >= 3

    def test_create_duplicate_email(self) -> None:
        """测试使用已注册的邮箱创建用户（触发业务异常拦截）。"""
        # Arrange
        client = TestClient(app)
        payload1 = make_user_create_payload(username="user1", email="same@example.com")
        payload2 = make_user_create_payload(username="user2", email="same@example.com")
        client.post("/api/v1/users/", json=payload1)

        # Act
        response = client.post("/api/v1/users/", json=payload2)

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert data["error_code"] == "EMAIL_ALREADY_EXISTS"
        assert "same@example.com" in data["detail"]

    def test_get_user_not_found(self) -> None:
        """测试获取不存在的用户（触发 404 业务异常拦截）。"""
        # Arrange
        client = TestClient(app)

        # Act
        response = client.get("/api/v1/users/999")

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert data["error_code"] == "USER_NOT_FOUND"

    def test_get_user_success(self) -> None:
        """测试成功获取用户详情。"""
        # Arrange
        client = TestClient(app)
        payload = make_user_create_payload(username="getuser", email="get@example.com")
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

    def test_update_user_success(self) -> None:
        """测试成功更新用户信息。"""
        # Arrange
        client = TestClient(app)
        payload = make_user_create_payload(
            username="updateuser", email="old@example.com"
        )
        create_res = client.post("/api/v1/users/", json=payload)
        user_id = create_res.json()["id"]
        update_payload = {
            "username": "newusername",
            "email": "new@example.com",
        }

        # Act
        response = client.put(f"/api/v1/users/{user_id}", json=update_payload)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == user_id
        assert data["username"] == "newusername"
        assert data["email"] == "new@example.com"

    def test_unhandled_system_exception(self, mocker: MockerFixture) -> None:
        """测试系统发生未预料异常时，全局拦截处理器能够捕获并安全返回 500。"""
        # Arrange
        local_client = TestClient(app, raise_server_exceptions=False)
        mocker.patch(
            "my_project.users.api.UserService.get_user_by_id",
            side_effect=RuntimeError("Database crash"),
        )

        # Act
        response = local_client.get("/api/v1/users/1")

        # Assert
        assert response.status_code == 500
        data = response.json()
        assert data["error_code"] == "INTERNAL_SERVER_ERROR"
        assert data["detail"] == "系统内部错误，请稍后重试"
