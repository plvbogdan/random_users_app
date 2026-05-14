##  Random Users App




Приложение для загрузки и хранения случайных пользователей из внешнего API [randomdatatools.ru](https://randomdatatools.ru/developers/).

## Стек технологий

| Компонент | Технология | Обоснование |
|-----------|------------|-------------|
| Web фреймворк | FastAPI | Асинхронный, производительный, встроенная валидация, автоматическая документация |
| База данных | PostgreSQL | Надёжная реляционная БД, легко запускается в Docker |
| ORM | SQLAlchemy 2.0 (async) | Асинхронная работа с БД |
| HTTP клиент | HTTPX | Асинхронный, удобно тестировать |
| Шаблоны | Jinja2 | Гибкие HTML шаблоны |
| Контейнеризация | Docker Compose | Упрощает развёртывание |
| Тесты | pytest + respx | Моки внешнего API |

## Функциональность

- При первом запуске автоматически загружается 1000 пользователей из внешнего API
- Главная страница с таблицей пользователей (пагинация по 50 записей)
- Форма для ручной загрузки любого количества пользователей
- Страница конкретного пользователя: `/user/{id}`
- Страница случайного пользователя: `/random` (обновляется при каждом запросе)
- JSON API для пагинации: `/api/users?offset=0&limit=50`

## Запуск

```bash
git clone https://github.com/plvbogdan/random_users_app
cd random_users_app
docker compose up --build
```

После запуска:
- Главная страница: http://localhost:8000
- Документация API: http://localhost:8000/docs

## Тесты

```bash
docker compose exec app pytest tests/ -v
```


Результаты
```bash
tests/test_api_client.py::test_fetch_users_batch_with_mock PASSED        [14%]
tests/test_api_client.py::test_fetch_users_total_150_with_mock PASSED    [28%]
tests/test_main.py::test_home_page_returns_200 PASSED                    [42%]
tests/test_main.py::test_random_user_endpoint_returns_404_when_empty PASSED [57%]
tests/test_main.py::test_user_detail_nonexistent_returns_404 PASSED      [71%]
tests/test_services.py::test_save_user_to_db PASSED                      [85%]
tests/test_services.py::test_pagination_works PASSED                     [100%]
```


Тестируется

2 теста — клиент API (моки внешнего API, разбиение запросов по 100)

2 теста — сервисы (сохранение в БД, пагинация)

3 теста — эндпоинты (главная страница, случайный пользователь, 404)

## Переменные окружения

Создайте файл `.env`:

```
API_BASE_URL=https://api.randomdatatools.ru
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/random_users
```

## API Эндпоинты

| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/` | Главная страница |
| GET | `/api/users?offset=0&limit=50` | JSON список пользователей |
| POST | `/load` | Загрузить N пользователей |
| GET | `/user/{id}` | Страница пользователя |
| GET | `/random` | Случайный пользователь |
| GET | `/docs` | Swagger |

## Структура

```
random_users_app/
├── app/
│ ├── init.py
│ ├── main.py # FastAPI приложение, эндпоинты
│ ├── database.py # Подключение к PostgreSQL
│ ├── models.py # SQLAlchemy модель User
│ ├── schemas.py # Pydantic схемы
│ ├── api_client.py # Клиент для внешнего API
│ ├── services.py # Бизнес-логика
│ └── templates/ # HTML шаблоны
│ ├── index.html
│ └── user_detail.html
├── tests/
│ ├── init.py
│ ├── conftest.py # Фикстуры 
│ ├── test_api_client.py # Тесты клиента API 
│ ├── test_services.py # Тесты сервисов 
│ └── test_main.py # Тесты эндпоинтов
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── pytest.ini
└── README.md
```
---
