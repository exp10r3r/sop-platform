"""安全风险API"""

from fastapi import APIRouter, Depends, Query
from typing import Optional, List
from app.services.csm_client import CSMClient, get_csm_client

router = APIRouter(prefix="/risks", tags=["安全风险"])


@router.get("/poc", summary="获取PoC漏洞列表")
async def get_poc_vulns(
    vul_title: Optional[str] = Query(None, description="漏洞名称"),
    risklevel: Optional[str] = Query(None, description="漏洞等级: 0-低危, 1-中危, 2-高危, 3-严重"),
    target: Optional[str] = Query(None, description="漏洞地址"),
    ip: Optional[str] = Query(None, description="IP地址"),
    port: Optional[int] = Query(None, description="端口"),
    status: Optional[str] = Query(None, description="处置状态: 0-未处理, 1-已确认, 2-已修复, 3-误报, 4-待修复, 5-修复失败, 6-已验证, 7-忽略"),
    cve: Optional[str] = Query(None, description="CVE编号"),
    limit: int = Query(10, ge=1, le=1000, description="返回数量"),
    offset: int = Query(0, ge=0, description="偏移量"),
    ordering: Optional[str] = Query("-id", description="排序字段"),
    csm: CSMClient = Depends(get_csm_client),
):
    """
    获取PoC漏洞列表

    漏洞等级:
    - 0: 低危
    - 1: 中危
    - 2: 高危
    - 3: 严重

    处置状态:
    - 0: 未处理
    - 1: 已确认
    - 2: 已修复
    - 3: 误报
    - 4: 待修复
    - 5: 修复失败
    - 6: 已验证
    - 7: 忽略
    """
    params = {"limit": limit, "offset": offset, "attach": "count"}
    if vul_title:
        params["vul_title"] = vul_title
    if risklevel:
        params["risklevel"] = risklevel
    if target:
        params["target"] = target
    if ip:
        params["ip"] = ip
    if port:
        params["port"] = port
    if status:
        params["status"] = status
    if cve:
        params["cve"] = cve
    if ordering:
        params["ordering"] = ordering

    return await csm.get_poc_vulns(params)


@router.get("/version", summary="获取版本型漏洞列表")
async def get_version_vulns(
    vul_title: Optional[str] = Query(None, description="漏洞名称"),
    risklevel: Optional[str] = Query(None, description="漏洞等级"),
    target: Optional[str] = Query(None, description="漏洞地址"),
    ip: Optional[str] = Query(None, description="IP地址"),
    status: Optional[str] = Query(None, description="处置状态"),
    limit: int = Query(10, ge=1, le=1000, description="返回数量"),
    offset: int = Query(0, ge=0, description="偏移量"),
    ordering: Optional[str] = Query("-id", description="排序字段"),
    csm: CSMClient = Depends(get_csm_client),
):
    """
    获取版本型漏洞列表
    """
    params = {"limit": limit, "offset": offset, "attach": "count"}
    if vul_title:
        params["vul_title"] = vul_title
    if risklevel:
        params["risklevel"] = risklevel
    if target:
        params["target"] = target
    if ip:
        params["ip"] = ip
    if status:
        params["status"] = status
    if ordering:
        params["ordering"] = ordering

    return await csm.get_version_vulns(params)


@router.get("/thirdvuln", summary="获取第三方漏洞列表")
async def get_thirdvulns(
    vul_title: Optional[str] = Query(None, description="漏洞名称"),
    risklevel: Optional[str] = Query(None, description="漏洞等级"),
    target: Optional[str] = Query(None, description="漏洞地址"),
    status: Optional[str] = Query(None, description="处置状态"),
    limit: int = Query(10, ge=1, le=1000, description="返回数量"),
    offset: int = Query(0, ge=0, description="偏移量"),
    ordering: Optional[str] = Query("-id", description="排序字段"),
    csm: CSMClient = Depends(get_csm_client),
):
    """
    获取第三方漏洞列表
    """
    params = {"limit": limit, "offset": offset, "attach": "count"}
    if vul_title:
        params["vul_title"] = vul_title
    if risklevel:
        params["risklevel"] = risklevel
    if target:
        params["target"] = target
    if status:
        params["status"] = status
    if ordering:
        params["ordering"] = ordering

    return await csm.get_thirdvulns(params)


@router.get("/riskport", summary="获取高危端口列表")
async def get_risk_ports(
    ip: Optional[str] = Query(None, description="IP地址"),
    port: Optional[int] = Query(None, description="端口号"),
    service: Optional[str] = Query(None, description="服务类型"),
    limit: int = Query(10, ge=1, le=1000, description="返回数量"),
    offset: int = Query(0, ge=0, description="偏移量"),
    ordering: Optional[str] = Query("-id", description="排序字段"),
    csm: CSMClient = Depends(get_csm_client),
):
    """
    获取高危端口列表
    """
    params = {"limit": limit, "offset": offset, "attach": "count"}
    if ip:
        params["ip"] = ip
    if port:
        params["port"] = port
    if service:
        params["service"] = service
    if ordering:
        params["ordering"] = ordering

    return await csm.get_risk_ports(params)


@router.get("/abnormal-port", summary="获取非常规端口列表")
async def get_abnormal_ports(
    ip: Optional[str] = Query(None, description="IP地址"),
    port: Optional[int] = Query(None, description="端口号"),
    limit: int = Query(10, ge=1, le=1000, description="返回数量"),
    offset: int = Query(0, ge=0, description="偏移量"),
    ordering: Optional[str] = Query("-id", description="排序字段"),
    csm: CSMClient = Depends(get_csm_client),
):
    """
    获取非常规端口列表
    """
    params = {"limit": limit, "offset": offset, "attach": "count"}
    if ip:
        params["ip"] = ip
    if port:
        params["port"] = port
    if ordering:
        params["ordering"] = ordering

    return await csm.get_abnormal_ports(params)