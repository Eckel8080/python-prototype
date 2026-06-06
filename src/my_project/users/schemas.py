from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    """用户基础数据模型。"""

    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    email: EmailStr = Field(..., description="邮箱地址")


class UserCreate(UserBase):
    """创建用户时的请求输入模型。"""

    password: str = Field(..., min_length=6, max_length=100, description="密码")


class UserUpdate(BaseModel):
    """更新用户时的请求输入模型（所有字段可选）。"""

    username: str | None = Field(
        default=None, min_length=3, max_length=50, description="用户名"
    )
    email: EmailStr | None = Field(default=None, description="邮箱地址")


class UserResponse(UserBase):
    """向客户端返回的用户响应模型。"""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="用户唯一ID")
    is_active: bool = Field(..., description="用户是否处于激活状态")
