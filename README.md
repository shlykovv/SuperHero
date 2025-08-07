# SuperHero API (тестовое задание)

Проект на Django + DRF, который взаимодействует с внешним API [superheroapi.com](https://superheroapi.com/) для создания и фильтрации супергероев.  
Реализованы два метода на одном эндпоинте `/hero/`:

- `GET` — фильтрация супергероев по имени и характеристикам.
- `POST` — добавление нового героя по имени через внешний API.

---

## Функциональность

- Получение списка героев с фильтрами:
  - по имени (`name`)
  - по характеристикам (`intelligence`, `strength`, `speed`, `power`)  
    Примеры фильтров: `intelligence=90`, `strength=>=80`, `power=<=70`

- Добавление героя:
  - если герой уже есть — возвращается сообщение.
  - если не найден во внешнем API — 404.
  - если найден — сохраняется в БД и возвращается сериализованный объект.

---

## Установка и запуск

### 1. Клонировать проект

```bash
git clone https://github.com/shlykovv/SuperHero.git
cd SuperHero
```

### 2. Заполнить `.env`

Создайте `.env` файл на корневом уровне:

```env
# Django
SECRET_KEY=your_django_secret_key

# superhero API
SECRET_API_TOKEN=your_token
API_URL=https://www.superheroapi.com/api/

# Postgres
DATABASE_NAME=heroes_db
DATABASE_USER=user
DATABASE_PASSWORD=password
DATABASE_HOST=db
DATABASE_PORT=5432
```

### 3. Собрать и запустить через Docker Compose

```bash
docker-compose up --build
```

### 4. Применить миграции и создать суперпользователя

```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

---

## Тестирование

Тесты написаны на `pytest`.

Для запуска:

```bash
docker-compose exec web pytest
```

---

## Примеры запросов

### GET `/hero/`

```http
GET /hero/?name=Batman&intelligence=>=80
```

### POST `/hero/`

```http
POST /hero/
Content-Type: application/json

{
  "name": "Batman"
}
```

---

## Используемые технологии

- Django + Django REST Framework
- PostgreSQL
- Docker + Docker Compose
- Pytest
- `.env` для конфигурации

---

## Внешнее API

В проекте используется [SuperHero API](https://www.superheroapi.com/)  
Пример запроса:  
`https://www.superheroapi.com/api/YOUR_TOKEN/search/Batman`

---

## Структура проекта

```
SuperHero/
├── heroes/               # Приложение heroes
│   ├── models.py         # Модель HeroModel
│   ├── views.py          # APIView с GET и POST
│   ├── serializers.py
│   └── tests/
│       └── test_hero_api.py
├── SuperHero/            # Конфигурация Django
├── manage.py
├── Dockerfile
├── docker-compose.yml
└── .env
```

---

## Автор

Тестовое задание выполнено кандидатом: [shlykovv](https://github.com/shlykovv)

---

## Примечания

- Код отформатирован и покрыт базовыми тестами.
- Обработка ошибок внешнего API реализована.
- При необходимости можно расширить фильтры и покрытие тестами.