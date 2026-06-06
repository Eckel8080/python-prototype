from fastapi import APIRouter

from my_project.users.api import router as users_router

api_router = APIRouter()
api_router.include_router(users_router, prefix="/v1/users", tags=["Users"])
