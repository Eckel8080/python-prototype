import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from my_project.api import api_router
from my_project.core.config import settings
from my_project.users.exceptions import BusinessError

# 配置全局日志
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION,
)


class HealthCheckResponse(BaseModel):
    """健康检查响应数据模型。"""

    status: str = Field(..., description="服务状态，通常为 'healthy'")
    service: str = Field(..., description="服务名称标识")


# 全局业务异常拦截处理器
@app.exception_handler(BusinessError)
def business_exception_handler(_request: Request, exc: BusinessError) -> JSONResponse:
    """拦截并统一处理自定义的业务异常。"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.message,
            "error_code": exc.error_code,
        },
    )


# 全局系统级未预料异常拦截处理器
@app.exception_handler(Exception)
def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """拦截并统一处理系统级未预料异常。"""
    logger.error(
        f"Unhandled Exception occurred: {exc} on path: {request.url.path}",
        exc_info=True,
    )
    return JSONResponse(
        status_code=500,
        content={
            "detail": "系统内部错误，请稍后重试",
            "error_code": "INTERNAL_SERVER_ERROR",
        },
    )


# 挂载路由聚合
app.include_router(api_router, prefix="/api")


@app.get(
    "/",
    response_model=HealthCheckResponse,
    status_code=200,
    tags=["Health Check"],
)
def health_check() -> dict[str, str]:
    """健康检查/根目录端点。"""
    return {"status": "healthy", "service": "user-api"}
