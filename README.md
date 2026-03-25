# SOP Platform

内部SOP平台，对接CSM（外部攻击面管理）平台API，提供资产数据、安全风险、安全情报等功能。

## 技术栈

- **后端**: FastAPI + Python 3.8.9
- **前端**: Vue 3 + Element Plus + ECharts
- **数据库**: PostgreSQL
- **定时任务**: APScheduler

## 项目结构

```
sop-platform/
├── backend/                    # FastAPI 后端
│   ├── app/
│   │   ├── api/               # API路由
│   │   │   ├── assets.py      # 资产管理API
│   │   │   ├── risks.py       # 安全风险API
│   │   │   ├── intelligence.py # 安全情报API
│   │   │   ├── reports.py     # 数据报表API
│   │   │   └── auth.py        # 用户认证API
│   │   ├── services/          # 业务服务
│   │   │   ├── csm_client.py  # CSM API客户端
│   │   │   ├── sync_service.py # 数据同步服务
│   │   │   └── auth_service.py # 认证服务（JWT、密码验证）
│   │   ├── models/            # 数据模型
│   │   │   ├── dashboard.py   # 总览统计模型
│   │   │   └── user.py        # 用户和审计日志模型
│   │   ├── utils/             # 工具函数
│   │   │   └── auth.py        # 认证依赖注入
│   │   ├── config.py          # 配置管理
│   │   ├── database.py        # 数据库连接
│   │   └── main.py            # 应用入口
│   ├── requirements.txt
│   └── .env
├── frontend/                  # Vue 3 前端
│   ├── src/
│   │   ├── views/             # 页面组件
│   │   │   ├── assets/        # 资产管理页面
│   │   │   ├── risks/         # 安全风险页面
│   │   │   ├── intelligence/  # 安全情报页面
│   │   │   ├── Dashboard.vue  # 总览页面
│   │   │   ├── Reports.vue    # 报表页面
│   │   │   └── Login.vue      # 登录页面
│   │   ├── stores/            # 状态管理
│   │   │   └── user.js        # 用户状态管理
│   │   ├── api/               # API调用
│   │   └── router/            # 路由配置
│   └── package.json
└── README.md
```

## 快速开始

### 1. 数据库初始化

```bash
# 创建数据库
psql -U postgres -c "CREATE DATABASE sop_platform;"

# 执行初始化脚本（可选，应用启动时会自动创建表）
psql -U postgres -d sop_platform -f backend/init.sql
```

> 注：应用启动时会自动创建所需表结构，手动执行SQL脚本为可选操作。

### 2. 后端启动

```bash
# 进入后端目录
cd backend

# 安装依赖
pip3 install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，配置CSM平台地址和密钥、数据库连接

# 启动服务
python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8888
```

### 前端启动

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

### 访问

- 前端: http://localhost:3001
- 后端API文档: http://localhost:8888/docs
- **默认管理员账户**: `admin` / `admin123`（请在生产环境中修改密码）

## 功能模块

### 用户认证
- **JWT认证**: 基于JWT Token的无状态认证
- **用户管理**: 仅管理员可创建/删除用户
- **角色权限**: admin（管理员）、user（普通用户）
- **审计日志**: 记录登录/登出、数据操作、API调用
- **路由守卫**: 未登录自动跳转登录页

### 总览页面
- **本地数据存储**: 统计数据存储在本地PostgreSQL数据库
- **定时同步**: 每小时自动从CSM平台同步数据
- **手动同步**: 提供"数据同步"按钮，支持手动触发同步
- **统计卡片**: IP资产、域名资产、PoC漏洞、漏洞情报数量展示
- **图表展示**: 漏洞风险等级分布、处置状态分布

### 资产管理
- IP资产（ip、port、service、os、secstate、createtime、uptime、location、isp）
- 域名资产
- 端口服务
- 站点列表
- SSL证书

### 安全风险
- PoC漏洞
- 版本型漏洞
- 第三方漏洞
- 高危端口

### 安全情报
- 漏洞情报
- 暗网监控
- 开源社区监控
- 影子资产监控

## 数据库设计

### dashboard_stats 表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | SERIAL | 主键 |
| ip_count | INTEGER | IP资产数量 |
| domain_count | INTEGER | 域名数量 |
| portserver_count | INTEGER | 端口服务数量 |
| webapp_count | INTEGER | 站点数量 |
| poc_count | INTEGER | PoC漏洞数量 |
| version_count | INTEGER | 版本漏洞数量 |
| thirdvuln_count | INTEGER | 第三方漏洞数量 |
| riskport_count | INTEGER | 高危端口数量 |
| vulinfo_count | INTEGER | 漏洞情报数量 |
| critical_count | INTEGER | 严重漏洞数量 |
| high_count | INTEGER | 高危漏洞数量 |
| medium_count | INTEGER | 中危漏洞数量 |
| low_count | INTEGER | 低危漏洞数量 |
| unhandled_count | INTEGER | 未处理数量 |
| fixed_count | INTEGER | 已修复数量 |
| updated_at | TIMESTAMP | 更新时间 |

### dashboard_stats_history 表（历史趋势）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | SERIAL | 主键 |
| ... | ... | 与 dashboard_stats 相同字段 |
| snapshot_at | TIMESTAMP | 快照时间 |
| source | VARCHAR(20) | 数据来源：auto/manual |

### users 表（用户）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | SERIAL | 主键 |
| username | VARCHAR(50) | 用户名（唯一） |
| email | VARCHAR(100) | 邮箱（唯一） |
| password_hash | VARCHAR(255) | 密码哈希（bcrypt） |
| role | VARCHAR(20) | 角色：admin/user |
| is_active | BOOLEAN | 是否激活 |
| last_login | TIMESTAMP | 最后登录时间 |
| created_at | TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | 更新时间 |

### audit_logs 表（审计日志）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | SERIAL | 主键 |
| user_id | INTEGER | 用户ID（外键） |
| action | VARCHAR(50) | 操作类型：login/logout/create/update/delete |
| resource | VARCHAR(100) | 资源类型 |
| resource_id | INTEGER | 资源ID |
| details | TEXT | 操作详情（JSON） |
| ip_address | VARCHAR(45) | IP地址 |
| user_agent | TEXT | 用户代理 |
| created_at | TIMESTAMP | 创建时间 |

## 配置说明

### 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| CSM_BASE_URL | CSM平台地址 | https://localhost:38201 |
| CSM_ACCESS_KEY | CSM平台AccessKey | - |
| CSM_SECRET_KEY | CSM平台SecretKey | - |
| DATABASE_URL | 数据库连接地址 | postgresql://postgres:postgres@localhost:5432/sop_platform |
| SECRET_KEY | JWT密钥（生产环境请修改） | your-secret-key-change-in-production |
| DEBUG | 调试模式 | true |

## API接口

### 用户认证

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/auth/login | 用户登录 |
| POST | /api/auth/logout | 用户登出 |
| GET | /api/auth/me | 获取当前用户信息 |
| PUT | /api/auth/password | 修改密码 |
| POST | /api/auth/register | 创建用户（仅管理员） |
| GET | /api/auth/users | 用户列表（仅管理员） |
| DELETE | /api/auth/users/{id} | 删除用户（仅管理员） |
| GET | /api/auth/audit-logs | 审计日志列表（仅管理员） |

### 数据报表

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/reports/summary | 获取综合统计概览（从本地数据库读取） |
| GET | /api/reports/trend?days=7 | 获取历史趋势数据（最近N天） |
| POST | /api/reports/sync | 手动触发数据同步 |
| GET | /api/reports/assets | 获取资产报表 |
| GET | /api/reports/risks | 获取风险报表 |
| GET | /api/reports/intelligence | 获取情报报表 |

### 资产管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/assets/ip | 获取IP资产列表 |
| GET | /api/assets/domain | 获取域名资产列表 |
| GET | /api/assets/portserver | 获取端口服务列表 |
| GET | /api/assets/webapp | 获取站点列表 |
| GET | /api/assets/ssl | 获取SSL证书列表 |

### 安全风险

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/risks/poc | 获取PoC漏洞列表 |
| GET | /api/risks/version | 获取版本型漏洞列表 |
| GET | /api/risks/thirdvuln | 获取第三方漏洞列表 |
| GET | /api/risks/riskport | 获取高危端口列表 |

启动后端服务后，访问 http://localhost:8888/docs 查看完整Swagger API文档。