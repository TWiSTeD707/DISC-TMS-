from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_company_creator = models.BooleanField(default=False)
    is_worker = models.BooleanField(default=False)

class Team(models.Model):
    name = models.CharField(max_length=100)
    creator = models.ForeignKey(User, related_name='teams_created', on_delete=models.CASCADE)
    employees = models.ManyToManyField(User, related_name='teams', blank=True)
