"""数据报表API"""

from fastapi import APIRouter, Depends
from typing import Dict, Any
from app.services.csm_client import CSMClient, get_csm_client

router = APIRouter(prefix="/reports", tags=["数据报表"])


@router.get("/summary", summary="获取综合统计概览")
async def get_summary(
    csm: CSMClient = Depends(get_csm_client),
) -> Dict[str, Any]:
    """
    获取综合统计概览

    返回资产、风险、情报的统计数据
    """
    # 并行获取各项统计数据
    ip_result = await csm.get_ip_assets({"limit": 1, "attach": "count"})
    domain_result = await csm.get_domains({"limit": 1, "attach": "count"})
    portserver_result = await csm.get_portservers({"limit": 1, "attach": "count"})
    webapp_result = await csm.get_webapps({"limit": 1, "attach": "count"})

    poc_result = await csm.get_poc_vulns({"limit": 1, "attach": "count"})
    version_result = await csm.get_version_vulns({"limit": 1, "attach": "count"})
    thirdvuln_result = await csm.get_thirdvulns({"limit": 1, "attach": "count"})
    riskport_result = await csm.get_risk_ports({"limit": 1, "attach": "count"})

    vulinfo_result = await csm.get_vulinfo({"limit": 1, "attach": "count"})

    # 按风险等级统计漏洞
    poc_critical = await csm.get_poc_vulns({"limit": 1, "attach": "count", "risklevel": "3"})
    poc_high = await csm.get_poc_vulns({"limit": 1, "attach": "count", "risklevel": "2"})
    poc_medium = await csm.get_poc_vulns({"limit": 1, "attach": "count", "risklevel": "1"})
    poc_low = await csm.get_poc_vulns({"limit": 1, "attach": "count", "risklevel": "0"})

    # 按处置状态统计
    poc_unhandled = await csm.get_poc_vulns({"limit": 1, "attach": "count", "status": "0"})
    poc_fixed = await csm.get_poc_vulns({"limit": 1, "attach": "count", "status": "2"})

    return {
        "status": True,
        "data": {
            "assets": {
                "ip_count": ip_result.get("count", 0),
                "domain_count": domain_result.get("count", 0),
                "portserver_count": portserver_result.get("count", 0),
                "webapp_count": webapp_result.get("count", 0),
            },
            "risks": {
                "poc_count": poc_result.get("count", 0),
                "version_count": version_result.get("count", 0),
                "thirdvuln_count": thirdvuln_result.get("count", 0),
                "riskport_count": riskport_result.get("count", 0),
                "by_level": {
                    "critical": poc_critical.get("count", 0),
                    "high": poc_high.get("count", 0),
                    "medium": poc_medium.get("count", 0),
                    "low": poc_low.get("count", 0),
                },
                "by_status": {
                    "unhandled": poc_unhandled.get("count", 0),
                    "fixed": poc_fixed.get("count", 0),
                },
            },
            "intelligence": {
                "vulinfo_count": vulinfo_result.get("count", 0),
            },
        },
    }


@router.get("/assets", summary="获取资产报表")
async def get_assets_report(
    csm: CSMClient = Depends(get_csm_client),
) -> Dict[str, Any]:
    """
    获取资产报表数据

    包含各类资产的数量统计
    """
    ip_result = await csm.get_ip_assets({"limit": 1, "attach": "count"})
    domain_result = await csm.get_domains({"limit": 1, "attach": "count"})
    portserver_result = await csm.get_portservers({"limit": 1, "attach": "count"})
    webapp_result = await csm.get_webapps({"limit": 1, "attach": "count"})
    url_result = await csm.get_urls({"limit": 1, "attach": "count"})
    ssl_result = await csm.get_ssl_certs({"limit": 1, "attach": "count"})

    return {
        "status": True,
        "data": {
            "ip": ip_result.get("count", 0),
            "domain": domain_result.get("count", 0),
            "portserver": portserver_result.get("count", 0),
            "webapp": webapp_result.get("count", 0),
            "url": url_result.get("count", 0),
            "ssl_cert": ssl_result.get("count", 0),
        },
    }


@router.get("/risks", summary="获取风险报表")
async def get_risks_report(
    csm: CSMClient = Depends(get_csm_client),
) -> Dict[str, Any]:
    """
    获取风险报表数据

    包含各类风险的数量统计
    """
    poc_result = await csm.get_poc_vulns({"limit": 1, "attach": "count"})
    version_result = await csm.get_version_vulns({"limit": 1, "attach": "count"})
    thirdvuln_result = await csm.get_thirdvulns({"limit": 1, "attach": "count"})
    riskport_result = await csm.get_risk_ports({"limit": 1, "attach": "count"})

    # 按风险等级统计
    level_stats = {}
    for level, name in [(0, "low"), (1, "medium"), (2, "high"), (3, "critical")]:
        result = await csm.get_poc_vulns({"limit": 1, "attach": "count", "risklevel": str(level)})
        level_stats[name] = result.get("count", 0)

    # 按处置状态统计
    status_stats = {}
    for status, name in [
        (0, "unhandled"),
        (1, "confirmed"),
        (2, "fixed"),
        (3, "false_positive"),
        (4, "pending"),
        (5, "fix_failed"),
        (6, "verified"),
        (7, "ignored"),
    ]:
        result = await csm.get_poc_vulns({"limit": 1, "attach": "count", "status": str(status)})
        status_stats[name] = result.get("count", 0)

    return {
        "status": True,
        "data": {
            "total": {
                "poc": poc_result.get("count", 0),
                "version": version_result.get("count", 0),
                "thirdvuln": thirdvuln_result.get("count", 0),
                "riskport": riskport_result.get("count", 0),
            },
            "by_level": level_stats,
            "by_status": status_stats,
        },
    }


@router.get("/intelligence", summary="获取情报报表")
async def get_intelligence_report(
    csm: CSMClient = Depends(get_csm_client),
) -> Dict[str, Any]:
    """
    获取情报报表数据

    包含各类情报的数量统计
    """
    vulinfo_result = await csm.get_vulinfo({"limit": 1, "attach": "count"})
    darkweb_result = await csm.get_darkweb({"limit": 1, "attach": "count"})
    git_result = await csm.get_git_monitor({"limit": 1, "attach": "count"})
    shadow_result = await csm.get_shadow_assets({"limit": 1, "attach": "count"})
    im_result = await csm.get_im_monitor({"limit": 1, "attach": "count"})
    mail_result = await csm.get_mail_monitor({"limit": 1, "attach": "count"})
    doc_result = await csm.get_doc_monitor({"limit": 1, "attach": "count"})
    pan_result = await csm.get_pan_monitor({"limit": 1, "attach": "count"})

    return {
        "status": True,
        "data": {
            "vulinfo": vulinfo_result.get("count", 0),
            "darkweb": darkweb_result.get("count", 0),
            "git": git_result.get("count", 0),
            "shadow": shadow_result.get("count", 0),
            "im": im_result.get("count", 0),
            "mail": mail_result.get("count", 0),
            "doc": doc_result.get("count", 0),
            "pan": pan_result.get("count", 0),
        },
    }