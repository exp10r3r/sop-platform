"""配置管理模块"""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """应用配置"""

    # CSM平台配置
    CSM_BASE_URL: str = "https://localhost:38201"
    CSM_ACCESS_KEY: str = ""
    CSM_SECRET_KEY: str = ""

    # 数据库配置
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/sop_platform"

    # 应用配置
    APP_NAME: str = "SOP Platform"
    DEBUG: bool = True

    # JWT配置
    SECRET_KEY: str = "sop-platform-secret-key-change-in-production"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """获取配置实例（缓存）"""
    return Settings()