class BusinessError(Exception):
    """自定义业务异常基类。"""

    def __init__(self, message: str, error_code: str, status_code: int = 400):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.status_code = status_code


class UserNotFoundError(BusinessError):
    """用户未找到异常。"""

    def __init__(self, user_id: int):
        super().__init__(
            message=f"ID 为 {user_id} 的用户不存在",
            error_code="USER_NOT_FOUND",
            status_code=404,
        )


class EmailAlreadyExistsError(BusinessError):
    """邮箱已被占用异常。"""

    def __init__(self, email: str):
        super().__init__(
            message=f"邮箱 {email} 已被注册",
            error_code="EMAIL_ALREADY_EXISTS",
            status_code=400,
        )
