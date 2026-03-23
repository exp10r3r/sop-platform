"""资产管理API"""

from fastapi import APIRouter, Depends, Query
from typing import Optional
from app.services.csm_client import CSMClient, get_csm_client

router = APIRouter(prefix="/assets", tags=["资产管理"])


@router.get("/ip", summary="获取IP资产列表")
async def get_ip_assets(
    ip: Optional[str] = Query(None, description="IP地址（模糊搜索）"),
    port: Optional[int] = Query(None, description="端口号"),
    os: Optional[str] = Query(None, description="操作系统"),
    location: Optional[str] = Query(None, description="地理位置"),
    limit: int = Query(10, ge=1, le=1000, description="返回数量"),
    offset: int = Query(0, ge=0, description="偏移量"),
    ordering: Optional[str] = Query("-id", description="排序字段"),
    csm: CSMClient = Depends(get_csm_client),
):
    """
    获取IP资产列表

    支持的搜索字段：
    - ip: IP地址
    - port: 端口号
    - os: 操作系统
    - location: 地理位置
    """
    params = {"limit": limit, "offset": offset, "attach": "count"}
    if ip:
        params["ip"] = ip
    if port:
        params["port"] = port
    if os:
        params["os"] = os
    if location:
        params["location"] = location
    if ordering:
        params["ordering"] = ordering

    return await csm.get_ip_assets(params)


@router.get("/domain", summary="获取域名资产列表")
async def get_domains(
    domain: Optional[str] = Query(None, description="域名（模糊搜索）"),
    ip: Optional[str] = Query(None, description="关联IP"),
    limit: int = Query(10, ge=1, le=1000, description="返回数量"),
    offset: int = Query(0, ge=0, description="偏移量"),
    ordering: Optional[str] = Query("-id", description="排序字段"),
    csm: CSMClient = Depends(get_csm_client),
):
    """
    获取域名资产列表
    """
    params = {"limit": limit, "offset": offset, "attach": "count"}
    if domain:
        params["domain"] = domain
    if ip:
        params["ip"] = ip
    if ordering:
        params["ordering"] = ordering

    return await csm.get_domains(params)


@router.get("/portserver", summary="获取端口服务列表")
async def get_portservers(
    ip: Optional[str] = Query(None, description="IP地址"),
    port: Optional[int] = Query(None, description="端口号"),
    service: Optional[str] = Query(None, description="服务类型"),
    limit: int = Query(10, ge=1, le=1000, description="返回数量"),
    offset: int = Query(0, ge=0, description="偏移量"),
    ordering: Optional[str] = Query("-id", description="排序字段"),
    csm: CSMClient = Depends(get_csm_client),
):
    """
    获取端口服务列表
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

    return await csm.get_portservers(params)


@router.get("/webapp", summary="获取站点列表")
async def get_webapps(
    webapp: Optional[str] = Query(None, description="站点名称"),
    ip: Optional[str] = Query(None, description="IP地址"),
    limit: int = Query(10, ge=1, le=1000, description="返回数量"),
    offset: int = Query(0, ge=0, description="偏移量"),
    ordering: Optional[str] = Query("-id", description="排序字段"),
    csm: CSMClient = Depends(get_csm_client),
):
    """
    获取站点列表
    """
    params = {"limit": limit, "offset": offset, "attach": "count"}
    if webapp:
        params["webapp"] = webapp
    if ip:
        params["ip"] = ip
    if ordering:
        params["ordering"] = ordering

    return await csm.get_webapps(params)


@router.get("/url", summary="获取URL/API资产列表")
async def get_urls(
    url: Optional[str] = Query(None, description="URL地址"),
    webapp_id: Optional[int] = Query(None, description="站点ID"),
    limit: int = Query(10, ge=1, le=1000, description="返回数量"),
    offset: int = Query(0, ge=0, description="偏移量"),
    ordering: Optional[str] = Query("-id", description="排序字段"),
    csm: CSMClient = Depends(get_csm_client),
):
    """
    获取URL/API资产列表
    """
    params = {"limit": limit, "offset": offset, "attach": "count"}
    if url:
        params["url"] = url
    if webapp_id:
        params["webapp_id"] = webapp_id
    if ordering:
        params["ordering"] = ordering

    return await csm.get_urls(params)


@router.get("/ssl", summary="获取SSL证书列表")
async def get_ssl_certs(
    domain: Optional[str] = Query(None, description="域名"),
    issuer: Optional[str] = Query(None, description="颁发者"),
    limit: int = Query(10, ge=1, le=1000, description="返回数量"),
    offset: int = Query(0, ge=0, description="偏移量"),
    ordering: Optional[str] = Query("-id", description="排序字段"),
    csm: CSMClient = Depends(get_csm_client),
):
    """
    获取SSL证书列表
    """
    params = {"limit": limit, "offset": offset, "attach": "count"}
    if domain:
        params["domain"] = domain
    if issuer:
        params["issuer"] = issuer
    if ordering:
        params["ordering"] = ordering

    return await csm.get_ssl_certs(params)