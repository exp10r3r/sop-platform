"""FastAPI应用入口"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import sys

from app.config import get_settings
from app.api import assets, risks, intelligence, reports

# 配置日志
logger.remove()
logger.add(sys.stderr, level="DEBUG")

settings = get_settings()

# 创建FastAPI应用
app = FastAPI(
    title=settings.APP_NAME,
    description="SOP平台 - 对接CSM平台API，提供资产数据、安全风险、安全情报等功能",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境请配置具体的前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(assets.router, prefix="/api")
app.include_router(risks.router, prefix="/api")
app.include_router(intelligence.router, prefix="/api")
app.include_router(reports.router, prefix="/api")


@app.get("/", tags=["根路径"])
async def root():
    """根路径"""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "docs": "/docs",
        "version": "1.0.0",
    }


@app.get("/health", tags=["健康检查"])
async def health_check():
    """健康检查接口"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
    )