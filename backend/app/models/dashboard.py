"""数据库模型 - 总览统计数据"""

from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.sql import func
from app.database import Base


class DashboardStats(Base):
    """总览统计数据表 - 当前最新快照"""

    __tablename__ = "dashboard_stats"

    id = Column(Integer, primary_key=True, index=True)

    # 资产统计
    ip_count = Column(Integer, default=0)
    domain_count = Column(Integer, default=0)
    portserver_count = Column(Integer, default=0)
    webapp_count = Column(Integer, default=0)

    # 风险统计
    poc_count = Column(Integer, default=0)
    version_count = Column(Integer, default=0)
    thirdvuln_count = Column(Integer, default=0)
    riskport_count = Column(Integer, default=0)

    # 情报统计
    vulinfo_count = Column(Integer, default=0)

    # 风险等级分布
    critical_count = Column(Integer, default=0)
    high_count = Column(Integer, default=0)
    medium_count = Column(Integer, default=0)
    low_count = Column(Integer, default=0)

    # 处置状态分布
    unhandled_count = Column(Integer, default=0)
    fixed_count = Column(Integer, default=0)

    # 更新时间
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class DashboardStatsHistory(Base):
    """总览统计数据历史表 - 用于趋势分析"""

    __tablename__ = "dashboard_stats_history"

    id = Column(Integer, primary_key=True, index=True)

    # 资产统计
    ip_count = Column(Integer, default=0)
    domain_count = Column(Integer, default=0)
    portserver_count = Column(Integer, default=0)
    webapp_count = Column(Integer, default=0)

    # 风险统计
    poc_count = Column(Integer, default=0)
    version_count = Column(Integer, default=0)
    thirdvuln_count = Column(Integer, default=0)
    riskport_count = Column(Integer, default=0)

    # 情报统计
    vulinfo_count = Column(Integer, default=0)

    # 风险等级分布
    critical_count = Column(Integer, default=0)
    high_count = Column(Integer, default=0)
    medium_count = Column(Integer, default=0)
    low_count = Column(Integer, default=0)

    # 处置状态分布
    unhandled_count = Column(Integer, default=0)
    fixed_count = Column(Integer, default=0)

    # 快照时间（用于趋势分析）
    snapshot_at = Column(DateTime, server_default=func.now(), index=True)

    # 数据来源：auto(定时同步) / manual(手动同步)
    source = Column(String(20), default='auto')