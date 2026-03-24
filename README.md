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
│   │   │   └── reports.py     # 数据报表API
│   │   ├── services/          # 业务服务
│   │   │   ├── csm_client.py  # CSM API客户端
│   │   │   └── sync_service.py # 数据同步服务
│   │   ├── models/            # 数据模型
│   │   │   └── dashboard.py   # 总览统计模型
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
│   │   │   └── Reports.vue    # 报表页面
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

## 功能模块

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

## 配置说明

### 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| CSM_BASE_URL | CSM平台地址 | https://localhost:38201 |
| CSM_ACCESS_KEY | CSM平台AccessKey | - |
| CSM_SECRET_KEY | CSM平台SecretKey | - |
| DATABASE_URL | 数据库连接地址 | postgresql://postgres:postgres@localhost:5432/sop_platform |
| DEBUG | 调试模式 | true |

## API接口

### 数据报表

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/reports/summary | 获取综合统计概览（从本地数据库读取） |
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