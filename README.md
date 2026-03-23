# SOP Platform

内部SOP平台，对接CSM（外部攻击面管理）平台API，提供资产数据、安全风险、安全情报等功能。

## 技术栈

- **后端**: FastAPI + Python 3.8.9
- **前端**: Vue 3 + Element Plus + ECharts
- **数据库**: PostgreSQL

## 项目结构

```
sop-platform/
├── backend/                # FastAPI 后端
│   ├── app/
│   │   ├── api/           # API路由
│   │   ├── services/      # 业务服务
│   │   ├── models/        # 数据模型
│   │   └── main.py        # 应用入口
│   ├── requirements.txt
│   └── .env
└── frontend/              # Vue 3 前端
    ├── src/
    │   ├── views/         # 页面组件
    │   ├── api/           # API调用
    │   └── router/        # 路由配置
    └── package.json
```

## 快速开始

### 后端启动

```bash
# 进入后端目录
cd backend

# 安装依赖
pip3 install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，配置CSM平台地址和密钥

# 启动服务
python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
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

- 前端: http://localhost:3000
- 后端API文档: http://localhost:8000/docs

## 功能模块

### 资产管理
- IP资产
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

### 数据报表
- 综合统计概览
- 资产统计报表
- 风险统计报表
- 情报统计报表

## 配置说明

### 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| CSM_BASE_URL | CSM平台地址 | https://localhost:38201 |
| CSM_ACCESS_KEY | CSM平台AccessKey | - |
| CSM_SECRET_KEY | CSM平台SecretKey | - |
| DATABASE_URL | 数据库连接地址 | postgresql://... |
| DEBUG | 调试模式 | true |

## API文档

启动后端服务后，访问 http://localhost:8000/docs 查看Swagger API文档。