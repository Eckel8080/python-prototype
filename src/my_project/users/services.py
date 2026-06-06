from my_project.users.exceptions import EmailAlreadyExistsError, UserNotFoundError
from my_project.users.schemas import UserCreate, UserUpdate

# 模拟一个内存数据库
USERS_DB: dict[int, dict] = {}
_id_counter = 0


class UserService:
    """用户业务逻辑服务层。"""

    def create_user(self, user_in: UserCreate) -> dict:
        """创建新用户。

        Args:
            user_in: 创建用户输入数据。

        Returns:
            创建成功的用户字典数据。

        Raises:
            EmailAlreadyExistsError: 当邮箱已被注册时抛出。
        """
        global _id_counter
        # 检查邮箱冲突
        for user in USERS_DB.values():
            if user["email"] == user_in.email:
                raise EmailAlreadyExistsError(user_in.email)

        _id_counter += 1
        new_user = {
            "id": _id_counter,
            "username": user_in.username,
            "email": user_in.email,
            "is_active": True,
        }
        USERS_DB[_id_counter] = new_user
        return new_user

    def get_user_by_id(self, user_id: int) -> dict:
        """根据用户ID获取用户详情。

        Args:
            user_id: 用户唯一ID。

        Returns:
            用户字典数据。

        Raises:
            UserNotFoundError: 当用户不存在时抛出。
        """
        user = USERS_DB.get(user_id)
        if not user:
            raise UserNotFoundError(user_id)
        return user

    def update_user(self, user_id: int, user_in: UserUpdate) -> dict:
        """更新用户信息。

        Args:
            user_id: 用户唯一ID。
            user_in: 更新的数据。

        Returns:
            更新后的用户字典数据。

        Raises:
            UserNotFoundError: 当用户不存在时抛出.
            EmailAlreadyExistsError: 当新邮箱已被其他用户注册时抛出。
        """
        user = self.get_user_by_id(user_id)

        # 检查新邮箱是否与其他用户冲突
        if user_in.email and user_in.email != user["email"]:
            for other_id, other_user in USERS_DB.items():
                if other_id != user_id and other_user["email"] == user_in.email:
                    raise EmailAlreadyExistsError(user_in.email)

        # 增量更新字段
        update_data = user_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            user[key] = value

        USERS_DB[user_id] = user
        return user
