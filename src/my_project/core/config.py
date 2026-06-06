from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """项目全局配置管理类。

    通过 pydantic_settings 自动从环境变量或 .env 文件中加载配置。
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # 基础配置
    PROJECT_NAME: str = Field(default="My Web Project API", description="项目名称")
    PROJECT_DESCRIPTION: str = Field(
        default="基于 FastAPI 的 Python Web 开发规范参考实现", description="项目描述"
    )
    PROJECT_VERSION: str = Field(default="1.0.0", description="项目版本")

    # 服务运行配置
    LOG_LEVEL: str = Field(default="INFO", description="全局日志级别")


# 全局配置单例
settings = Settings()
