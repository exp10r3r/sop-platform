"""FastAPI应用入口"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import sys

from app.config import get_settings
from app.database import engine, Base, SessionLocal
from app.models import DashboardStats
from app.models.user import User, AuditLog  # 导入用户模型
from app.api import assets, risks, intelligence, reports, auth  # 导入认证路由
from app.services.csm_client import get_csm_client

# 配置日志
logger.remove()
logger.add(sys.stderr, level="DEBUG")

settings = get_settings()

# 定时任务调度器
scheduler = AsyncIOScheduler()


async def sync_dashboard_data():
    """定时同步总览数据"""
    from app.services.sync_service import SyncService
    logger.info("开始同步总览数据...")
    try:
        db = SessionLocal()
        csm = get_csm_client()
        sync_service = SyncService(db, csm)
        await sync_service.sync_dashboard_stats()
        db.close()
        logger.info("总览数据同步完成")
    except Exception as e:
        logger.error(f"总览数据同步失败: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时创建表
    Base.metadata.create_all(bind=engine)
    logger.info("数据库表创建完成")

    # 启动时执行一次同步
    await sync_dashboard_data()

    # 启动定时任务（每小时同步一次）
    scheduler.add_job(sync_dashboard_data, 'interval', hours=1)
    scheduler.start()
    logger.info("定时同步任务已启动（每小时）")

    yield

    # 关闭时停止定时任务
    scheduler.shutdown()
    logger.info("应用已关闭")


# 创建FastAPI应用
app = FastAPI(
    title=settings.APP_NAME,
    description="SOP平台 - 对接CSM平台API，提供资产数据、安全风险、安全情报等功能",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
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
app.include_router(auth.router, prefix="/api")  # 认证路由
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
        port=8888,
        reload=settings.DEBUG,
    )