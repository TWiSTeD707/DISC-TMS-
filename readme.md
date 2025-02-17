# DISC Test Management System

## 📚 Описание

**DISC Test Management System** — это система, предназначенная для управления тестами DISC в корпоративной среде. С помощью этой платформы компании могут организовывать и управлять тестированием своих сотрудников, создавать команды, анализировать результаты тестов с использованием нейросетей через интеграцию с **DeepSeek API** и улучшать процессы подбора и оценки персонала.

Проект предоставляет:
- Возможность регистрации компаний и сотрудников.
- Интеграцию с внешним API для аналитики результатов тестов.
- Простую и удобную систему для создания и управления командами сотрудников.

## 📦 Стек технологий

Проект использует следующий стек технологий:

- **Backend**: Python + Django + Django REST Framework  
- **База данных**: PostgreSQL   
- **Аутентификация**: JWT (djangorestframework-simplejwt)  
- **Внешняя аналитика**: DeepSeek API  
- **Деплой**: Nginx + Gunicorn

## ⚙️ Установка и настройка

### 1. Установка зависимостей

Для установки всех необходимых зависимостей используйте следующую команду:

```bash
pip install django djangorestframework djangorestframework-simplejwt psycopg2-binary celery requests
```

### 2. Настройка базы данных

В файле `settings.py` настроить подключение к базе данных PostgreSQL:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',  # Замените на имя вашей базы данных
        'USER': 'your_db_user',  # Замените на вашего пользователя базы данных
        'PASSWORD': 'your_db_password',  # Замените на ваш пароль
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 3. Применение миграций

Для применения миграций и создания всех необходимых таблиц в базе данных выполните команду:

```bash
python manage.py migrate
```

### 4. Запуск сервера разработки

Запустите сервер разработки, используя команду:

```bash
python manage.py runserver
```

Теперь ваш сервер доступен по адресу `http://localhost:8000`.

### 5. Запуск Celery

Для запуска задач Celery, выполните команду:

```bash
celery -A project_name worker --loglevel=info
```

Замените `project_name` на имя вашего проекта.

## 📑 Модели данных

### Пользователи и роли

Модель для пользователей, включающая роль сотрудника или компании:

```python
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = [("company", "Компания"), ("employee", "Сотрудник")]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    company = models.ForeignKey("Company", on_delete=models.CASCADE, null=True, blank=True)
```

### Компании и команды

Модели для создания компаний и команд:

```python
class Company(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class Team(models.Model):
    name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    members = models.ManyToManyField(CustomUser, related_name="teams")
```

### Результаты тестов DISC

Модель для хранения результатов тестов DISC для каждого сотрудника:

```python
class DISCResult(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    d_score = models.IntegerField()
    i_score = models.IntegerField()
    s_score = models.IntegerField()
    c_score = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
```

### Инвайт-ссылки

Модель для генерации инвайт-ссылок для сотрудников:

```python
class Invitation(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
```

## 🔐 Аутентификация и авторизация

Для аутентификации используется JWT-токены с использованием библиотеки **djangorestframework-simplejwt**. Чтобы настроить аутентификацию, добавьте следующие настройки в файл `settings.py`:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}
```

## 🌐 API-эндпоинты

### Для компаний

- **POST** /api/invite/ — Генерация инвайт-ссылки для приглашения сотрудников.
- **POST** /api/teams/ — Создание новой команды в компании.
- **GET** /api/employees/ — Получение списка сотрудников с результатами тестов.
- **GET** /api/analytics/ — Получение метрик и аналитики от DeepSeek API для оценки команды.

### Для сотрудников

- **GET** /api/my-results/ — Получение результатов своих тестов.
- **GET** /api/my-team/ — Информация о команде, к которой принадлежит сотрудник.

## ⚡ Интеграция с DeepSeek API

Для анализа данных о сотрудниках используется **DeepSeek API**, который обрабатывает данные и предоставляет аналитические выводы. Асинхронная обработка данных выполняется через Celery.

### Асинхронная обработка данных через Celery:

```python
from celery import shared_task
import requests

@shared_task
def analyze_team(team_id):
    team = Team.objects.get(id=team_id)
    data = {
        "members": [{"d": member.disc_result.d_score, "i": member.disc_result.i_score, ...} for member in team.members.all()]
    }
    response = requests.post("https://api.deepseek.com/analyze", json=data)
    # Сохранение результатов анализа в БД
```

## 🔗 Генерация инвайт-ссылок

Для создания уникальных инвайт-ссылок для сотрудников компании используется следующий код:

```python
class InviteView(APIView):
    def post(self, request):
        company = request.user.company
        token = uuid.uuid4()
        Invitation.objects.create(company=company, token=token, expires_at=timezone.now() + timedelta(days=3))
        return Response({"link": f"https://ваш-сайт.ru/join/{token}/"})
```

Каждый инвайт-ссылочный токен генерируется уникально и имеет срок действия 3 дня.

## 🛡️ Безопасность

- **HTTPS**: Рекомендуется для всех запросов, чтобы обеспечить безопасность данных.
- **Валидация данных**: Все данные, которые проходят через API, валидаируются с использованием сериализаторов Django REST Framework.
- **Хеширование паролей**: Django встроенно использует безопасное хеширование паролей.
- **Защита от CSRF и SQL-инъекций**: Django ORM автоматически защищает от SQL-инъекций и CSRF-атак.

## 🚀 Деплой

Для деплоя проекта рекомендуется использовать **Nginx** и **Gunicorn**:

1. **Gunicorn** — WSGI сервер для запуска приложения.
2. **Nginx** — веб-сервер для маршрутизации запросов и работы с фронтендом.

Пример конфигурации для **Gunicorn**:

```bash
gunicorn project_name.wsgi:application --bind 0.0.0.0:8000
```

Пример конфигурации для **Nginx**:

```nginx
server {
    listen 80;
    server_name example.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```