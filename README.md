# Проект для тренировки в области NLP.

Написан на FastAPI, SQLAlchemy, Alembic, Pydantic, NLTK и spaCy.
Производит поиск в тексте ключевых и стоп слов. Ключевые и стоп слова можно добавить через эндпоинты.

## Установка
- Клонировать репозиторий и перейти в него в командной строке:

    ```bash
    git clone https://github.com/corbuncul/word_analitic.git
    ```

    ```bash
    cd word_analitic
    ```

- Cоздать и активировать виртуальное окружение:

    При разработке использовалась версия python 3.11.9

    ```bash
    python3 -m venv venv
    ```

    * Если у вас Linux/macOS

        ```bash
        source venv/bin/activate
        ```

    * Если у вас windows

        ```bash
        source venv/scripts/activate
        ```

- Установить зависимости из файла requirements.txt:

    ```bash
    python3 -m pip install --upgrade pip
    ```

    ```bash
    pip install -r requirements.txt
    ```
- Создать файл ".env" и прописать константы:

    ```ini
    AP_TITLE=Ваше название приложения
    AP_DESCRIPTION=Ваше краткое описание приложения
    AP_SECRET=Ваш секртный ключ (любая случайная строка)
    DB_DATABASE_URL=Ваше подключение к базе данных (например: sqlite+aiosqlite:///./fastapi.db)
    SU_SUPERUSER_EMAIL=Ваш email для первого суперпользователя. Если указан, при первом запуске будет создан суперпользователь.
    SU_SUPERUSER_PASSWORD=Ваш пароль суперпользователя
    ```
- Применить миграции:

    ```bash
    alembic upgrade head
    ```
## Запуск проекта:

```bash
uvicorn app.main:app
```

Проект будет доступен по адресу http://localhost:8000/
Подергать ручки http://localhost:8000/docs/