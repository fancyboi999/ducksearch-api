# 使用官方 Python 3.9 镜像作为基础镜像
FROM cjie.eu.org/python:3.9

# 将工作目录切换到 /app
WORKDIR /app

# 复制项目依赖列表并安装
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 将应用程序代码复制到容器中
COPY . .

# 暴露端口号 8000
EXPOSE 8000

# 设置环境变量
ENV FASTAPI_CONFIG=run.py
ENV FASTAPI_CONFIG=production

# 在容器中运行 FastAPI 服务器
CMD ["uvicorn", "run:app", "--host", "0.0.0.0", "--port", "8000"]
