from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from my_project.api.v1.users import router as users_router
from my_project.services.user import BusinessException

app = FastAPI(
    title="My Web Project API",
    description="基于 FastAPI 的 Python Web 开发规范参考实现",
    version="1.0.0",
)


# 全局业务异常拦截处理器
@app.exception_handler(BusinessException)
def business_exception_handler(
    request: Request, exc: BusinessException
) -> JSONResponse:
    """拦截并统一处理自定义的业务异常。"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.message,
            "error_code": exc.error_code,
        },
    )


# 挂载路由
app.include_router(users_router, prefix="/api/v1/users", tags=["Users"])


@app.get("/", tags=["Health Check"])
def health_check() -> dict[str, str]:
    """健康检查/根目录端点。"""
    return {"status": "healthy", "service": "user-api"}
