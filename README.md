# DuckDuckGo API

一个基于 DuckDuckGo 搜索引擎的 RESTful API 服务，支持文本搜索、问答、图片和视频搜索。

## 功能特点

- 基于 FastAPI 构建的高性能异步 API
- 支持多种搜索类型：文本、问答、图片、视频
- 自动提取和清洗搜索结果
- 完整的错误处理和日志记录
- Docker 容器化部署支持
- 可配置的代理支持

## API 接口

### 1. 文本搜索
```http
GET/POST /search?q=马思唯是谁&max_results=2
```

参数：
- `q`: 搜索关键词（必需）
- `max_results`: 最大返回结果数（可选，默认值：10）

示例响应：
```json
{
    "results": [
        {
            "title": "搜索结果标题",
            "body": "搜索结果摘要...",
            "href": "https://example.com",
            "full_content": "完整的网页内容..."
        }
    ]
}
```

### 2. 问答搜索
```http
GET/POST /searchAnswers?q=马思唯是谁&max_results=1
```

### 3. 图片搜索
```http
GET/POST /searchImages?q=马思唯&max_results=2
```

### 4. 视频搜索
```http
GET/POST /searchVideos?q=马思唯&max_results=2
```

## 部署说明

### 使用 Docker Compose（推荐）

1. 克隆仓库并进入项目目录
```bash
git clone 
cd duckduckgo-api
```

2. 配置环境变量（可选）
创建 `.env` 文件并设置以下变量：
```
FASTAPI_CONFIG=production
# 如需使用代理，取消注释下面的配置
# HTTP_PROXY=http://your-proxy:port
# HTTPS_PROXY=http://your-proxy:port
```

3. 启动服务
```bash
docker-compose up -d
```

服务将在 http://localhost:8000 启动，可通过 http://localhost:8000/docs 访问 API 文档。

### 手动部署

1. 安装依赖
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. 运行服务
```bash
# 开发环境
python run.py

# 生产环境
uvicorn run:app --host 0.0.0.0 --port 8000 --workers 4 --log-level info
```

## 配置项

配置文件位于 `config.py`，主要配置项包括：

- `FASTAPI_CONFIG`: 运行环境（development/production/testing）
- `MAX_WORKERS`: 工作线程数
- `DEFAULT_MAX_RESULTS`: 默认最大返回结果数
- `LOG_LEVEL`: 日志级别
- `PROXY_CONFIG`: 代理服务器配置

## 日志

- 日志文件保存在 `logs` 目录
- 按日期自动轮转
- 包含请求信息、错误追踪等

## 许可证

MIT License