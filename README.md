# A2UI Web

AI-powered user interface with dynamic UI generation capabilities. A standalone web application that connects to an LLM backend and Odoo MCP server to provide intelligent chat interactions with dynamic UI rendering.

## Quick Start

```bash
# Copy environment file and configure
cp .env.example .env
# Edit .env with your LLM API key and Odoo MCP URL

# Start all services
docker-compose up -d
```

The application will be available at `http://localhost`.

## Architecture

- **Frontend**: Vue 3 + Naive UI + Tailwind CSS + Pinia + Vue Router
- **Backend**: FastAPI + SQLAlchemy 2.0 async + aiosqlite
- **Proxy**: Nginx (reverse proxy + static file serving)

## Default Admin

After startup, register a user and manually set `is_admin=true` in the database.

## Development

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Frontend
cd frontend
npm install
npm run dev
```
