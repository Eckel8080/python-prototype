import pytest

from my_project.users.exceptions import (
    EmailAlreadyExistsError,
    UserNotFoundError,
)
from my_project.users.schemas import UserCreate, UserUpdate
from my_project.users.services import UserService


def make_user_create(
    username: str = "testuser",
    email: str = "test@example.com",
    password: str = "strongpassword",
) -> UserCreate:
    """测试数据工厂：生成创建用户输入模型实例。"""
    return UserCreate(username=username, email=email, password=password)


class TestUserService:
    """UserService 模块的单元测试类。"""

    def test_create_user_success(self) -> None:
        """测试成功创建用户。"""
        # Arrange
        service = UserService()
        user_in = make_user_create()

        # Act
        result = service.create_user(user_in)

        # Assert
        assert result["id"] == 1
        assert result["username"] == "testuser"
        assert result["email"] == "test@example.com"
        assert result["is_active"] is True

    def test_create_duplicate_email_raises_error(self) -> None:
        """测试使用已注册的邮箱创建用户时，抛出 EmailAlreadyExistsError 异常。"""
        # Arrange
        service = UserService()
        user_in1 = make_user_create(username="user1", email="same@example.com")
        user_in2 = make_user_create(username="user2", email="same@example.com")
        service.create_user(user_in1)

        # Act & Assert
        with pytest.raises(EmailAlreadyExistsError) as exc_info:
            service.create_user(user_in2)

        assert exc_info.value.status_code == 400
        assert "same@example.com" in exc_info.value.message

    def test_get_user_by_id_success(self) -> None:
        """测试成功根据 ID 获取用户详情。"""
        # Arrange
        service = UserService()
        user_in = make_user_create(username="getuser", email="get@example.com")
        created = service.create_user(user_in)
        user_id = created["id"]

        # Act
        result = service.get_user_by_id(user_id)

        # Assert
        assert result["id"] == user_id
        assert result["username"] == "getuser"
        assert result["email"] == "get@example.com"

    def test_get_user_not_found_raises_error(self) -> None:
        """测试获取不存在的用户时，抛出 UserNotFoundError 异常。"""
        # Arrange
        service = UserService()
        non_exist_id = 999

        # Act & Assert
        with pytest.raises(UserNotFoundError) as exc_info:
            service.get_user_by_id(non_exist_id)

        assert exc_info.value.status_code == 404
        assert f"ID 为 {non_exist_id} 的用户不存在" in exc_info.value.message

    def test_update_user_success(self) -> None:
        """测试成功更新用户信息。"""
        # Arrange
        service = UserService()
        created = service.create_user(make_user_create(email="old@example.com"))
        user_id = created["id"]
        update_in = UserUpdate(username="newname", email="new@example.com")

        # Act
        result = service.update_user(user_id, update_in)

        # Assert
        assert result["id"] == user_id
        assert result["username"] == "newname"
        assert result["email"] == "new@example.com"

    def test_update_user_duplicate_email_raises_error(self) -> None:
        """测试更新用户邮箱为已被占用的邮箱时，抛出 EmailAlreadyExistsError 异常。"""
        # Arrange
        service = UserService()
        service.create_user(
            make_user_create(username="user1", email="user1@example.com")
        )
        user2 = service.create_user(
            make_user_create(username="user2", email="user2@example.com")
        )
        update_in = UserUpdate(email="user1@example.com")

        # Act & Assert
        with pytest.raises(EmailAlreadyExistsError) as exc_info:
            service.update_user(user2["id"], update_in)

        assert exc_info.value.status_code == 400
        assert "user1@example.com" in exc_info.value.message
