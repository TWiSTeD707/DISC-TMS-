# urls.py
from .views import RegistrationView, LoginView
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/register/', RegistrationView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('admin/', admin.site.urls),
    path('api/', include('users.urls'))
]