INSTALLED_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
    'users',
]

AUTH_USER_MODEL = 'users.CustomUser'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'recruiter_db',
        'USER': 'recruiter_user',
        'PASSWORD': 'securepassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}