FROM python:3.12-slim AS base

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- Production Stage ----
FROM base AS production

COPY . .
RUN mkdir -p /app/data
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# ---- Development Stage ----
FROM base AS development

# watchfiles 提供高效的文件变更检测，uvicorn --reload 会自动使用它
RUN pip install --no-cache-dir watchfiles

# 不 COPY 源码 — docker-compose.dev.yml 会用 volume 挂载
RUN mkdir -p /app/data

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
