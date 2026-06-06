from fastapi import APIRouter, Depends

from my_project.users.schemas import UserCreate, UserResponse, UserUpdate
from my_project.users.services import UserService

router = APIRouter()


def get_user_service() -> UserService:
    """依赖注入：获取 UserService 实例。

    Returns:
        UserService 实例。
    """
    return UserService()


@router.post("/", response_model=UserResponse, status_code=201)
def create_user(
    user_in: UserCreate,
    service: UserService = Depends(get_user_service),
) -> dict:
    """创建新用户接口。"""
    return service.create_user(user_in)


@router.get("/{user_id}", response_model=UserResponse, status_code=200)
def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
) -> dict:
    """获取指定用户详情接口。"""
    return service.get_user_by_id(user_id)


@router.put("/{user_id}", response_model=UserResponse, status_code=200)
def update_user(
    user_id: int,
    user_in: UserUpdate,
    service: UserService = Depends(get_user_service),
) -> dict:
    """更新用户信息接口。"""
    return service.update_user(user_id, user_in)
