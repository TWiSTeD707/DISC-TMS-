# DISC Test Management System

## 📚 Описание

Этот проект предназначен для управления тестами DISC в корпоративной среде. Он позволяет компаниям создавать команды, отправлять приглашения сотрудникам и анализировать результаты тестов через интеграцию с внешним API DeepSeek.

## 📦 Стек технологий
 • Backend: Python + Django + Django REST Framework

 • База данных: PostgreSQL
 
 • Асинхронные задачи: Celery + Redis/RabbitMQ
 
 • Аутентификация: JWT (djangorestframework-simplejwt)
 
 • Внешняя аналитика: DeepSeek API
 
 • Деплой: Nginx + Gunicorn

## ⚙️ Установка и настройка

### 1. Установка зависимостей

pip install django djangorestframework djangorestframework-simplejwt psycopg2-binary celery requests

### 2. Настройка базы данных

settings.py:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

### 3. Применение миграций

python manage.py migrate

### 4. Запуск сервера разработки

python manage.py runserver

### 5. Запуск Celery

celery -A project_name worker --loglevel=info

## 📑 Модели данных

### Пользователи и роли

from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = [("company", "Компания"), ("employee", "Сотрудник")]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    company = models.ForeignKey("Company", on_delete=models.CASCADE, null=True, blank=True)

### Компании и команды

class Company(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class Team(models.Model):
    name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    members = models.ManyToManyField(CustomUser, related_name="teams")

### Результаты тестов DISC

class DISCResult(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    d_score = models.IntegerField()
    i_score = models.IntegerField()
    s_score = models.IntegerField()
    c_score = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

### Инвайт-ссылки

class Invitation(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

## 🔐 Аутентификация и авторизация

### JWT-токены:
Добавьте настройки в settings.py:

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

## 🌐 API-эндпоинты

### Для компаний
 • POST /api/invite/ — генерация инвайт-ссылки
 
 • POST /api/teams/ — создание команды
 
 • GET /api/employees/ — список сотрудников с результатами тестов
 
 • GET /api/analytics/ — метрики от DeepSeek API

### Для сотрудников
 • GET /api/my-results/ — результаты своих тестов
 • GET /api/my-team/ — информация о команде

## ⚡ Интеграция с DeepSeek API

### Асинхронная обработка данных через Celery:

@shared_task
def analyze_team(team_id):
    team = Team.objects.get(id=team_id)
    data = {
        "members": [{"d": member.disc_result.d_score, "i": member.disc_result.i_score, ...} for member in team.members.all()]
    }
    response = requests.post("https://api.deepseek.com/analyze", json=data)
    # Сохранение результатов анализа в БД

## 🔗 Генерация инвайт-ссылок

### Пример создания ссылки:

class InviteView(APIView):
    def post(self, request):
        company = request.user.company
        token = uuid.uuid4()
        Invitation.objects.create(company=company, token=token, expires_at=timezone.now() + timedelta(days=3))
        return Response({"link": f"https://ваш-сайт.ru/join/{token}/"})

## 🛡️ Безопасность
 • HTTPS: рекомендуется для всех запросов

 • Валидация данных: сериализаторы Django REST Framework

 • Хеширование паролей: встроено в Django

 • Защита от CSRF и SQL-инъекций: ORM Django

## 🚀 Деплой
 1. Сервер: Nginx + Gunicorn
 2. Хостинг: Яндекс.
