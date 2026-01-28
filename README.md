# Helpdesk Backend Service

Backend сервис внутреннего helpdesk приложения на Django + DRF.

## Технологии

- Python 3.11+
- Django 4.2+
- Django REST Framework
- PostgreSQL 15
- Docker + docker-compose
- JWT аутентификация (djangorestframework-simplejwt)
- django-filter для фильтрации
- drf-spectacular для Swagger документации

## Быстрый старт

### Запуск через Docker

```bash
docker-compose up --build
```

Сервис будет доступен на http://localhost:8000

### Swagger документация

http://localhost:8000/api/docs/

## Переменные окружения

| Переменная | Описание | По умолчанию |
|------------|----------|--------------|
| `DEBUG` | Режим отладки | `False` |
| `SECRET_KEY` | Секретный ключ Django | - |
| `POSTGRES_DB` | Имя базы данных | `helpdesk` |
| `POSTGRES_USER` | Пользователь БД | `helpdesk` |
| `POSTGRES_PASSWORD` | Пароль БД | `helpdesk` |
| `ALLOWED_HOSTS` | Разрешённые хосты (production) | - |

## Тестовые пользователи

При запуске автоматически создаются тестовые пользователи:

| Email | Пароль | Роль |
|-------|--------|------|
| `applicant@test.com` | `testpass123` | Заявитель |
| `operator@test.com` | `testpass123` | Оператор |
| `executor@test.com` | `testpass123` | Исполнитель |

## API Endpoints

### Аутентификация

#### Регистрация
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepass123",
    "password_confirm": "securepass123",
    "first_name": "Имя",
    "last_name": "Фамилия",
    "role": "applicant"
  }'
```

#### Авторизация (получение JWT)
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "applicant@test.com",
    "password": "testpass123"
  }'
```

Ответ:
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

#### Обновление токена
```bash
curl -X POST http://localhost:8000/api/auth/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }'
```

### Заявки (Tickets)

#### Создать заявку (Заявитель)
```bash
curl -X POST http://localhost:8000/api/tickets/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -d '{
    "title": "Не работает принтер",
    "description": "Принтер на 3 этаже не печатает документы",
    "priority": "high"
  }'
```

#### Мои заявки (Заявитель)
```bash
curl -X GET http://localhost:8000/api/tickets/my/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

С фильтрацией:
```bash
curl -X GET "http://localhost:8000/api/tickets/my/?status=new&priority=high" \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

#### Все заявки (Оператор)
```bash
curl -X GET http://localhost:8000/api/tickets/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

С фильтрацией:
```bash
curl -X GET "http://localhost:8000/api/tickets/?status=new&priority=medium" \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

#### Назначить исполнителя (Оператор)
```bash
curl -X PATCH http://localhost:8000/api/tickets/<TICKET_UUID>/assign/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -d '{
    "assigned_to": 3
  }'
```

#### Назначенные мне заявки (Исполнитель)
```bash
curl -X GET http://localhost:8000/api/tickets/assigned/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

#### Завершить заявку (Исполнитель)
```bash
curl -X PATCH http://localhost:8000/api/tickets/<TICKET_UUID>/complete/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

#### Отклонить заявку (Исполнитель)
```bash
curl -X PATCH http://localhost:8000/api/tickets/<TICKET_UUID>/reject/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

## Роли и права доступа

| Роль | Права |
|------|-------|
| **Заявитель** (applicant) | Создаёт заявки, видит только свои |
| **Оператор** (operator) | Видит все заявки, назначает исполнителей |
| **Исполнитель** (executor) | Видит только назначенные ему, может завершить/отклонить |

## Статусы заявок

- `new` - Новая
- `in_progress` - В работе
- `completed` - Выполнена
- `rejected` - Отклонена

## Приоритеты

- `low` - Низкий
- `medium` - Средний
- `high` - Высокий

## Структура проекта

```
src/
├── config/             # Настройки Django
│   └── settings/       # base, development, production
├── core/               # Общие компоненты
│   └── exceptions.py   # Кастомные исключения
└── apps/
    ├── users/          # Пользователи и аутентификация
    │   ├── models.py
    │   ├── serializers.py
    │   ├── views.py
    │   ├── services.py
    │   ├── selectors.py
    │   └── permissions.py
    └── tickets/        # Заявки
        ├── models.py
        ├── serializers.py
        ├── views.py
        ├── services.py
        ├── selectors.py
        ├── permissions.py
        └── filters.py
```

## Архитектурные принципы

- **Тонкие views** - только обработка HTTP
- **services.py** - бизнес-логика
- **selectors.py** - запросы к БД с оптимизацией (select_related)
- **Разные serializers** - для разных действий (Create, List, Detail)
- **Кастомные permissions** - для каждой роли
