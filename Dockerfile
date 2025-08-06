FROM python:3.12

# Установка poetry
RUN pip install poetry

# Установка рабочей директории
WORKDIR /app

# Копирование файлов poetry
COPY pyproject.toml poetry.lock* /app/

# Установка зависимостей
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Копирование проекта
COPY . /app

EXPOSE 8000


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]