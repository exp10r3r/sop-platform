"""安全情报API"""

from fastapi import APIRouter, Depends, Query
from typing import Optional
from app.services.csm_client import CSMClient, get_csm_client

router = APIRouter(prefix="/intel", tags=["安全情报"])


@router.get("/vulinfo", summary="获取漏洞情报列表")
async def get_vulinfo(
    title: Optional[str] = Query(None, description="情报标题"),
    risk_level: Optional[str] = Query(None, description="风险等级"),
    limit: int = Query(10, ge=1, le=1000, description="返回数量"),
    offset: int = Query(0, ge=0, description="偏移量"),
    ordering: Optional[str] = Query("-id", description="排序字段"),
    csm: CSMClient = Depends(get_csm_client),
):
    """
    获取漏洞情报列表
    """
    params = {"limit": limit, "offset": offset, "attach": "count"}
    if title:
        params["title"] = title
    if risk_level:
        params["risk_level"] = risk_level
    if ordering:
        params["ordering"] = ordering

    return await csm.get_vulinfo(params)


@router.get("/darkweb", summary="获取暗网监控数据")
async def get_darkweb(
    keyword: Optional[str] = Query(None, description="关键字"),
    limit: int = Query(10, ge=1, le=1000, description="返回数量"),
    offset: int = Query(0, ge=0, description="偏移量"),
    ordering: Optional[str] = Query("-id", description="排序字段"),
    csm: CSMClient = Depends(get_csm_client),
):
    """
    获取暗网监控数据
    """
    params = {"limit": limit, "offset": offset, "attach": "count"}
    if keyword:
        params["keyword"] = keyword
    if ordering:
        params["ordering"] = ordering

    return await csm.get_darkweb(params)


@router.get("/git", summary="获取开源社区监控数据")
async def get_git_monitor(
    keyword: Optional[str] = Query(None, description="关键字"),
    repo: Optional[str] = Query(None, description="仓库名称"),
    limit: int = Query(10, ge=1, le=1000, description="返回数量"),
    offset: int = Query(0, ge=0, description="偏移量"),
    ordering: Optional[str] = Query("-id", description="排序字段"),
    csm: CSMClient = Depends(get_csm_client),
):
    """
    获取开源社区监控数据（GitHub、GitLab等）
    """
    params = {"limit": limit, "offset": offset, "attach": "count"}
    if keyword:
        params["keyword"] = keyword
    if repo:
        params["repo"] = repo
    if ordering:
        params["ordering"] = ordering

    return await csm.get_git_monitor(params)


@router.get("/shadow", summary="获取影子资产监控数据")
async def get_shadow_assets(
    keyword: Optional[str] = Query(None, description="关键字"),
    asset_type: Optional[str] = Query(None, description="资产类型"),
    limit: int = Query(10, ge=1, le=1000, description="返回数量"),
    offset: int = Query(0, ge=0, description="偏移量"),
    ordering: Optional[str] = Query("-id", description="排序字段"),
    csm: CSMClient = Depends(get_csm_client),
):
    """
    获取影子资产监控数据
    """
    params = {"limit": limit, "offset": offset, "attach": "count"}
    if keyword:
        params["keyword"] = keyword
    if asset_type:
        params["asset_type"] = asset_type
    if ordering:
        params["ordering"] = ordering

    return await csm.get_shadow_assets(params)


@router.get("/im", summary="获取IM监控数据")
async def get_im_monitor(
    keyword: Optional[str] = Query(None, description="关键字"),
    limit: int = Query(10, ge=1, le=1000, description="返回数量"),
    offset: int = Query(0, ge=0, description="偏移量"),
    ordering: Optional[str] = Query("-id", description="排序字段"),
    csm: CSMClient = Depends(get_csm_client),
):
    """
    获取IM监控数据（Telegram、Discord等）
    """
    params = {"limit": limit, "offset": offset, "attach": "count"}
    if keyword:
        params["keyword"] = keyword
    if ordering:
        params["ordering"] = ordering

    return await csm.get_im_monitor(params)


@router.get("/mails", summary="获取企业邮箱监控数据")
async def get_mail_monitor(
    email: Optional[str] = Query(None, description="邮箱地址"),
    limit: int = Query(10, ge=1, le=1000, description="返回数量"),
    offset: int = Query(0, ge=0, description="偏移量"),
    ordering: Optional[str] = Query("-id", description="排序字段"),
    csm: CSMClient = Depends(get_csm_client),
):
    """
    获取企业邮箱监控数据
    """
    params = {"limit": limit, "offset": offset, "attach": "count"}
    if email:
        params["email"] = email
    if ordering:
        params["ordering"] = ordering

    return await csm.get_mail_monitor(params)


@router.get("/doc", summary="获取文档监控数据")
async def get_doc_monitor(
    keyword: Optional[str] = Query(None, description="关键字"),
    limit: int = Query(10, ge=1, le=1000, description="返回数量"),
    offset: int = Query(0, ge=0, description="偏移量"),
    ordering: Optional[str] = Query("-id", description="排序字段"),
    csm: CSMClient = Depends(get_csm_client),
):
    """
    获取文档监控数据
    """
    params = {"limit": limit, "offset": offset, "attach": "count"}
    if keyword:
        params["keyword"] = keyword
    if ordering:
        params["ordering"] = ordering

    return await csm.get_doc_monitor(params)


@router.get("/pan", summary="获取网盘监控数据")
async def get_pan_monitor(
    keyword: Optional[str] = Query(None, description="关键字"),
    limit: int = Query(10, ge=1, le=1000, description="返回数量"),
    offset: int = Query(0, ge=0, description="偏移量"),
    ordering: Optional[str] = Query("-id", description="排序字段"),
    csm: CSMClient = Depends(get_csm_client),
):
    """
    获取网盘监控数据
    """
    params = {"limit": limit, "offset": offset, "attach": "count"}
    if keyword:
        params["keyword"] = keyword
    if ordering:
        params["ordering"] = ordering

    return await csm.get_pan_monitor(params)