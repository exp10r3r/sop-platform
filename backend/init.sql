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

-- ==================== 用户和认证相关表 ====================

-- 用户表
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'user',  -- admin, user
    is_active BOOLEAN DEFAULT TRUE,
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 用户表索引
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- 审计日志表
CREATE TABLE IF NOT EXISTS audit_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    action VARCHAR(50) NOT NULL,      -- login, logout, create, update, delete, api_call
    resource VARCHAR(100),            -- 操作的资源类型
    resource_id INTEGER,              -- 资源ID
    details TEXT,                     -- JSON格式的操作详情
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 审计日志表索引
CREATE INDEX IF NOT EXISTS idx_audit_logs_user ON audit_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_action ON audit_logs(action);
CREATE INDEX IF NOT EXISTS idx_audit_logs_created ON audit_logs(created_at);

-- 用户表注释
COMMENT ON TABLE users IS '用户表';
COMMENT ON COLUMN users.username IS '用户名';
COMMENT ON COLUMN users.email IS '邮箱';
COMMENT ON COLUMN users.password_hash IS '密码哈希';
COMMENT ON COLUMN users.role IS '角色：admin(管理员), user(普通用户)';
COMMENT ON COLUMN users.is_active IS '是否激活';
COMMENT ON COLUMN users.last_login IS '最后登录时间';

-- 审计日志表注释
COMMENT ON TABLE audit_logs IS '审计日志表';
COMMENT ON COLUMN audit_logs.action IS '操作类型：login, logout, create, update, delete, api_call';
COMMENT ON COLUMN audit_logs.resource IS '资源类型';
COMMENT ON COLUMN audit_logs.resource_id IS '资源ID';
COMMENT ON COLUMN audit_logs.details IS '操作详情(JSON)';
COMMENT ON COLUMN audit_logs.ip_address IS 'IP地址';
COMMENT ON COLUMN audit_logs.user_agent IS '用户代理';

-- 创建默认管理员账户（密码: admin123，请在生产环境中修改）
-- 密码哈希使用bcrypt生成，对应密码: admin123
INSERT INTO users (username, email, password_hash, role)
VALUES ('admin', 'admin@example.com', '$2b$12$bVCgAn9fBCmjNJ9LENJgL.if/S1pFC.4FeDPFspgEK/dcqG4Cg1G2', 'admin')
ON CONFLICT (username) DO NOTHING;