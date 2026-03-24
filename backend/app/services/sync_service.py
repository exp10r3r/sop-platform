"""数据同步服务"""

from sqlalchemy.orm import Session
from app.models.dashboard import DashboardStats
from app.services.csm_client import CSMClient


class SyncService:
    """数据同步服务"""

    def __init__(self, db: Session, csm: CSMClient):
        self.db = db
        self.csm = csm

    async def sync_dashboard_stats(self) -> DashboardStats:
        """同步总览统计数据"""

        # 资产统计
        ip_result = await self.csm.get_ip_assets({"limit": 1, "attach": "count"})
        domain_result = await self.csm.get_domains({"limit": 1, "attach": "count"})
        portserver_result = await self.csm.get_portservers({"limit": 1, "attach": "count"})
        webapp_result = await self.csm.get_webapps({"limit": 1, "attach": "count"})

        # 风险统计
        poc_result = await self.csm.get_poc_vulns({"limit": 1, "attach": "count"})
        version_result = await self.csm.get_version_vulns({"limit": 1, "attach": "count"})
        thirdvuln_result = await self.csm.get_thirdvulns({"limit": 1, "attach": "count"})
        riskport_result = await self.csm.get_risk_ports({"limit": 1, "attach": "count"})

        # 情报统计
        vulinfo_result = await self.csm.get_vulinfo({"limit": 1, "attach": "count"})

        # 按风险等级统计
        poc_critical = await self.csm.get_poc_vulns({"limit": 1, "attach": "count", "risklevel": "3"})
        poc_high = await self.csm.get_poc_vulns({"limit": 1, "attach": "count", "risklevel": "2"})
        poc_medium = await self.csm.get_poc_vulns({"limit": 1, "attach": "count", "risklevel": "1"})
        poc_low = await self.csm.get_poc_vulns({"limit": 1, "attach": "count", "risklevel": "0"})

        # 按处置状态统计
        poc_unhandled = await self.csm.get_poc_vulns({"limit": 1, "attach": "count", "status": "0"})
        poc_fixed = await self.csm.get_poc_vulns({"limit": 1, "attach": "count", "status": "2"})

        # 获取或创建统计记录（只保留一条记录）
        stats = self.db.query(DashboardStats).first()
        if not stats:
            stats = DashboardStats()
            self.db.add(stats)

        # 更新数据
        stats.ip_count = ip_result.get("count", 0)
        stats.domain_count = domain_result.get("count", 0)
        stats.portserver_count = portserver_result.get("count", 0)
        stats.webapp_count = webapp_result.get("count", 0)

        stats.poc_count = poc_result.get("count", 0)
        stats.version_count = version_result.get("count", 0)
        stats.thirdvuln_count = thirdvuln_result.get("count", 0)
        stats.riskport_count = riskport_result.get("count", 0)

        stats.vulinfo_count = vulinfo_result.get("count", 0)

        stats.critical_count = poc_critical.get("count", 0)
        stats.high_count = poc_high.get("count", 0)
        stats.medium_count = poc_medium.get("count", 0)
        stats.low_count = poc_low.get("count", 0)

        stats.unhandled_count = poc_unhandled.get("count", 0)
        stats.fixed_count = poc_fixed.get("count", 0)

        self.db.commit()
        self.db.refresh(stats)

        return stats

    def get_dashboard_stats(self) -> DashboardStats:
        """获取总览统计数据"""
        stats = self.db.query(DashboardStats).first()
        if not stats:
            # 返回空数据
            stats = DashboardStats()
        return stats