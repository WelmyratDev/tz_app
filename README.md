# 📝 Task Management System

Простое веб-приложение для управления задачами, построенное на FastAPI, PostgreSQL и Docker.

## 🚀 Стек технологий

- FastAPI
- SQLAlchemy (async)
- PostgreSQL
- Alembic
- Docker + Docker Compose
- Poetry
- Pytest

## ⚙️ Установка и запуск

### 1. Клонируй репозиторий и перейди в папку проекта

```bash
git clone https://github.com/WelmyratDev/tz_app.git
cd your-repo-name

python -m venv env
source env/bin/activate  # Windows: env\Scripts\activate

pip install poetry

poetry install

docker compose run --rm web alembic upgrade head

docker compose up --build

http://127.0.0.1:8000/docs

## Для Теста 
docker compose run --rm web pytest -v


