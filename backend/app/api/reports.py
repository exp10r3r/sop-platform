"""数据报表API"""

from fastapi import APIRouter, Depends, BackgroundTasks
from typing import Dict, Any
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.csm_client import CSMClient, get_csm_client
from app.services.sync_service import SyncService

router = APIRouter(prefix="/reports", tags=["数据报表"])


@router.get("/summary", summary="获取综合统计概览")
async def get_summary(
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """
    获取综合统计概览

    从本地数据库读取统计数据
    """
    sync_service = SyncService(db, None)
    stats = sync_service.get_dashboard_stats()

    return {
        "status": True,
        "data": {
            "assets": {
                "ip_count": stats.ip_count,
                "domain_count": stats.domain_count,
                "portserver_count": stats.portserver_count,
                "webapp_count": stats.webapp_count,
            },
            "risks": {
                "poc_count": stats.poc_count,
                "version_count": stats.version_count,
                "thirdvuln_count": stats.thirdvuln_count,
                "riskport_count": stats.riskport_count,
                "by_level": {
                    "critical": stats.critical_count,
                    "high": stats.high_count,
                    "medium": stats.medium_count,
                    "low": stats.low_count,
                },
                "by_status": {
                    "unhandled": stats.unhandled_count,
                    "fixed": stats.fixed_count,
                },
            },
            "intelligence": {
                "vulinfo_count": stats.vulinfo_count,
            },
            "updated_at": stats.updated_at.isoformat() if stats.updated_at else None,
        },
    }


@router.post("/sync", summary="手动同步数据")
async def sync_data(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    csm: CSMClient = Depends(get_csm_client),
) -> Dict[str, Any]:
    """
    手动触发数据同步

    从CSM平台同步数据到本地数据库
    """
    sync_service = SyncService(db, csm)
    stats = await sync_service.sync_dashboard_stats(source="manual")

    return {
        "status": True,
        "message": "数据同步成功",
        "data": {
            "updated_at": stats.updated_at.isoformat() if stats.updated_at else None,
        },
    }


@router.get("/trend", summary="获取历史趋势数据")
async def get_trend(
    days: int = 7,
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """
    获取历史趋势数据

    Args:
        days: 查询最近N天的数据，默认7天
    """
    sync_service = SyncService(db, None)
    trend_data = sync_service.get_trend_data(days=days)

    return {
        "status": True,
        "data": trend_data,
    }


@router.get("/assets", summary="获取资产报表")
async def get_assets_report(
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """获取资产报表数据"""
    sync_service = SyncService(db, None)
    stats = sync_service.get_dashboard_stats()

    return {
        "status": True,
        "data": {
            "ip": stats.ip_count,
            "domain": stats.domain_count,
            "portserver": stats.portserver_count,
            "webapp": stats.webapp_count,
        },
    }


@router.get("/risks", summary="获取风险报表")
async def get_risks_report(
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """获取风险报表数据"""
    sync_service = SyncService(db, None)
    stats = sync_service.get_dashboard_stats()

    return {
        "status": True,
        "data": {
            "total": {
                "poc": stats.poc_count,
                "version": stats.version_count,
                "thirdvuln": stats.thirdvuln_count,
                "riskport": stats.riskport_count,
            },
            "by_level": {
                "critical": stats.critical_count,
                "high": stats.high_count,
                "medium": stats.medium_count,
                "low": stats.low_count,
            },
            "by_status": {
                "unhandled": stats.unhandled_count,
                "fixed": stats.fixed_count,
            },
        },
    }


@router.get("/intelligence", summary="获取情报报表")
async def get_intelligence_report(
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    """获取情报报表数据"""
    sync_service = SyncService(db, None)
    stats = sync_service.get_dashboard_stats()

    return {
        "status": True,
        "data": {
            "vulinfo": stats.vulinfo_count,
        },
    }