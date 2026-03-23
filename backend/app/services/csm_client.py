"""CSM平台API客户端"""

import httpx
from typing import Optional, Dict, Any
from loguru import logger
from app.config import get_settings


class CSMClient:
    """CSM平台API客户端"""

    def __init__(self):
        settings = get_settings()
        self.base_url = settings.CSM_BASE_URL.rstrip("/")
        self.headers = {
            "Accept": "application/json",
            "Content-type": "application/json",
            "ACCESSKEY": settings.CSM_ACCESS_KEY,
            "SECRETKEY": settings.CSM_SECRET_KEY,
        }

    async def _request(
        self, endpoint: str, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        发送请求到CSM平台

        Args:
            endpoint: API端点，如 /api/v1/ip
            params: 请求参数

        Returns:
            API响应数据
        """
        url = f"{self.base_url}{endpoint}"

        try:
            async with httpx.AsyncClient(verify=False, timeout=30.0) as client:
                response = await client.get(url, headers=self.headers, params=params)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            logger.error(f"CSM API请求失败: {endpoint}, 错误: {e}")
            return {"status": False, "info": [], "error": str(e)}

    # ==================== 资产数据API ====================

    async def get_ip_assets(self, params: Optional[Dict] = None) -> Dict:
        """获取IP资产列表"""
        return await self._request("/api/v1/ip", params)

    async def get_domains(self, params: Optional[Dict] = None) -> Dict:
        """获取域名资产列表"""
        return await self._request("/api/v1/domain", params)

    async def get_portservers(self, params: Optional[Dict] = None) -> Dict:
        """获取端口服务列表"""
        return await self._request("/api/v1/portserver", params)

    async def get_webapps(self, params: Optional[Dict] = None) -> Dict:
        """获取站点列表"""
        return await self._request("/api/v1/webapp", params)

    async def get_urls(self, params: Optional[Dict] = None) -> Dict:
        """获取URL/API资产列表"""
        return await self._request("/api/v1/url", params)

    async def get_ssl_certs(self, params: Optional[Dict] = None) -> Dict:
        """获取SSL证书列表"""
        return await self._request("/api/v1/ssl_cert", params)

    # ==================== 安全风险API ====================

    async def get_poc_vulns(self, params: Optional[Dict] = None) -> Dict:
        """获取PoC漏洞列表"""
        return await self._request("/api/v1/poc", params)

    async def get_version_vulns(self, params: Optional[Dict] = None) -> Dict:
        """获取版本型漏洞列表"""
        return await self._request("/api/v1/version", params)

    async def get_thirdvulns(self, params: Optional[Dict] = None) -> Dict:
        """获取第三方漏洞列表"""
        return await self._request("/api/v1/thirdvuln", params)

    async def get_risk_ports(self, params: Optional[Dict] = None) -> Dict:
        """获取高危端口列表"""
        return await self._request("/api/v1/riskport", params)

    async def get_abnormal_ports(self, params: Optional[Dict] = None) -> Dict:
        """获取非常规端口列表"""
        return await self._request("/api/v1/abnormal_port", params)

    # ==================== 安全情报API ====================

    async def get_vulinfo(self, params: Optional[Dict] = None) -> Dict:
        """获取漏洞情报列表"""
        return await self._request("/api/v1/vulinfo", params)

    async def get_darkweb(self, params: Optional[Dict] = None) -> Dict:
        """获取暗网监控数据"""
        return await self._request("/api/v1/darkweb", params)

    async def get_git_monitor(self, params: Optional[Dict] = None) -> Dict:
        """获取开源社区监控数据"""
        return await self._request("/api/v1/git", params)

    async def get_shadow_assets(self, params: Optional[Dict] = None) -> Dict:
        """获取影子资产监控数据"""
        return await self._request("/api/v1/shadow", params)

    async def get_im_monitor(self, params: Optional[Dict] = None) -> Dict:
        """获取IM监控数据"""
        return await self._request("/api/v1/im", params)

    async def get_mail_monitor(self, params: Optional[Dict] = None) -> Dict:
        """获取企业邮箱监控数据"""
        return await self._request("/api/v1/mails", params)

    async def get_doc_monitor(self, params: Optional[Dict] = None) -> Dict:
        """获取文档监控数据"""
        return await self._request("/api/v1/doc", params)

    async def get_pan_monitor(self, params: Optional[Dict] = None) -> Dict:
        """获取网盘监控数据"""
        return await self._request("/api/v1/pan", params)

    # ==================== 其他API ====================

    async def get_plugins(self, params: Optional[Dict] = None) -> Dict:
        """获取插件列表"""
        return await self._request("/api/v1/plugin", params)

    async def get_users(self, params: Optional[Dict] = None) -> Dict:
        """获取用户列表"""
        return await self._request("/api/v1/user", params)


# 创建全局客户端实例
csm_client = CSMClient()


def get_csm_client() -> CSMClient:
    """获取CSM客户端实例"""
    return csm_client