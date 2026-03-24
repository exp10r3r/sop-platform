-- SOP平台数据库初始化脚本
-- 创建数据库: CREATE DATABASE sop_platform;

-- 总览统计数据表
CREATE TABLE IF NOT EXISTS dashboard_stats (
    id SERIAL PRIMARY KEY,
    -- 资产统计
    ip_count INTEGER DEFAULT 0,
    domain_count INTEGER DEFAULT 0,
    portserver_count INTEGER DEFAULT 0,
    webapp_count INTEGER DEFAULT 0,
    -- 风险统计
    poc_count INTEGER DEFAULT 0,
    version_count INTEGER DEFAULT 0,
    thirdvuln_count INTEGER DEFAULT 0,
    riskport_count INTEGER DEFAULT 0,
    -- 情报统计
    vulinfo_count INTEGER DEFAULT 0,
    -- 风险等级分布
    critical_count INTEGER DEFAULT 0,
    high_count INTEGER DEFAULT 0,
    medium_count INTEGER DEFAULT 0,
    low_count INTEGER DEFAULT 0,
    -- 处置状态分布
    unhandled_count INTEGER DEFAULT 0,
    fixed_count INTEGER DEFAULT 0,
    -- 更新时间
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 插入初始数据（一条空记录）
INSERT INTO dashboard_stats (id) VALUES (1) ON CONFLICT DO NOTHING;

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_dashboard_stats_updated ON dashboard_stats(updated_at);

-- 总览统计数据历史表（用于趋势分析）
CREATE TABLE IF NOT EXISTS dashboard_stats_history (
    id SERIAL PRIMARY KEY,
    -- 资产统计
    ip_count INTEGER DEFAULT 0,
    domain_count INTEGER DEFAULT 0,
    portserver_count INTEGER DEFAULT 0,
    webapp_count INTEGER DEFAULT 0,
    -- 风险统计
    poc_count INTEGER DEFAULT 0,
    version_count INTEGER DEFAULT 0,
    thirdvuln_count INTEGER DEFAULT 0,
    riskport_count INTEGER DEFAULT 0,
    -- 情报统计
    vulinfo_count INTEGER DEFAULT 0,
    -- 风险等级分布
    critical_count INTEGER DEFAULT 0,
    high_count INTEGER DEFAULT 0,
    medium_count INTEGER DEFAULT 0,
    low_count INTEGER DEFAULT 0,
    -- 处置状态分布
    unhandled_count INTEGER DEFAULT 0,
    fixed_count INTEGER DEFAULT 0,
    -- 快照时间（用于趋势分析）
    snapshot_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    -- 数据来源：auto(定时同步) / manual(手动同步)
    source VARCHAR(20) DEFAULT 'auto'
);

-- 创建历史表索引
CREATE INDEX IF NOT EXISTS idx_stats_history_snapshot ON dashboard_stats_history(snapshot_at);

-- 注释
COMMENT ON TABLE dashboard_stats IS '总览统计数据表 - 当前最新快照';
COMMENT ON COLUMN dashboard_stats.ip_count IS 'IP资产数量';
COMMENT ON COLUMN dashboard_stats.domain_count IS '域名数量';
COMMENT ON COLUMN dashboard_stats.portserver_count IS '端口服务数量';
COMMENT ON COLUMN dashboard_stats.webapp_count IS '站点数量';
COMMENT ON COLUMN dashboard_stats.poc_count IS 'PoC漏洞数量';
COMMENT ON COLUMN dashboard_stats.version_count IS '版本漏洞数量';
COMMENT ON COLUMN dashboard_stats.thirdvuln_count IS '第三方漏洞数量';
COMMENT ON COLUMN dashboard_stats.riskport_count IS '高危端口数量';
COMMENT ON COLUMN dashboard_stats.vulinfo_count IS '漏洞情报数量';
COMMENT ON COLUMN dashboard_stats.critical_count IS '严重漏洞数量';
COMMENT ON COLUMN dashboard_stats.high_count IS '高危漏洞数量';
COMMENT ON COLUMN dashboard_stats.medium_count IS '中危漏洞数量';
COMMENT ON COLUMN dashboard_stats.low_count IS '低危漏洞数量';
COMMENT ON COLUMN dashboard_stats.unhandled_count IS '未处理数量';
COMMENT ON COLUMN dashboard_stats.fixed_count IS '已修复数量';
COMMENT ON COLUMN dashboard_stats.updated_at IS '数据更新时间';

COMMENT ON TABLE dashboard_stats_history IS '总览统计数据历史表 - 用于趋势分析';
COMMENT ON COLUMN dashboard_stats_history.snapshot_at IS '快照时间';
COMMENT ON COLUMN dashboard_stats_history.source IS '数据来源：auto(定时同步) / manual(手动同步)';