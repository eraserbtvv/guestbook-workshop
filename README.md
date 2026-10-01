# 📒 guestbook

Небольшая **гостевая книга** на FastAPI: можно оставить сообщение и посмотреть все оставленные. Данные хранятся в PostgreSQL.

## Что умеет

- `GET /` — приветствие
- `GET /health` — проверка «жив ли сервис»
- `GET /messages` — список сообщений (новые сверху)
- `POST /messages` — добавить сообщение: тело `{"author": "...", "text": "..."}`

## Запуск

Нужен только Docker с Compose.

```bash
cp .env.example .env      # и замените POSTGRES_PASSWORD на свой
docker compose up -d --build
```

Приложение будет доступно на <http://localhost:8000> (порт меняется через `APP_PORT`), документация API — на `/docs`.

База наружу не проброшена: она доступна только приложению внутри сети Compose. Данные лежат в именованном томе `db_data` и переживают `docker compose down` / `up`. Полностью удалить их можно через `docker compose down -v`.

## Настройки

Все настройки читаются в одном месте — [config.py](config.py) (pydantic-settings) — из переменных окружения или файла `.env`. Список переменных с примерами — в [.env.example](.env.example).

| Переменная          | Назначение                         | По умолчанию |
|---------------------|------------------------------------|--------------|
| `POSTGRES_USER`     | пользователь базы                  | —            |
| `POSTGRES_PASSWORD` | пароль базы                        | —            |
| `POSTGRES_DB`       | имя базы                           | —            |
| `DB_HOST`           | адрес базы (в Compose — `db`)      | `localhost`  |
| `DB_PORT`           | порт базы                          | `5432`       |
| `GREETING`          | текст приветствия на `/`           | см. конфиг   |
| `APP_PORT`          | порт приложения на хосте (Compose) | `8000`       |

Файл `.env` с реальными значениями в репозиторий не попадает (он в `.gitignore` и `.dockerignore`).

## Проверка

```bash
curl http://localhost:8000/health
curl -X POST http://localhost:8000/messages \
  -H "Content-Type: application/json" \
  -d '{"author": "Аня", "text": "Привет!"}'
curl http://localhost:8000/messages

docker compose down && docker compose up -d
curl http://localhost:8000/messages   # сообщение на месте
```

## Локальная разработка без Docker

Зависимости управляются через [uv](https://docs.astral.sh/uv/), версия Python закреплена в `.python-version`.

```bash
uv sync
uv run uvicorn main:app --reload
```

Для этого нужен доступный PostgreSQL с параметрами из `.env`.
