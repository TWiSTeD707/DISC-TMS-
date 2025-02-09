from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ("company", "Компания"),
        ("employee", "Сотрудник"),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    company = models.ForeignKey("Company", on_delete=models.CASCADE, null=True, blank=True)

class Company(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="teams")
    members = models.ManyToManyField(CustomUser, related_name="teams")

    def __str__(self):
        return f"{self.name} ({self.company.name})"

class DISCResult(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="disc_results")
    d_score = models.IntegerField()
    i_score = models.IntegerField()
    s_score = models.IntegerField()
    c_score = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"DISC Result for {self.user.email}"

class Invitation(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="invitations")
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"Invitation for {self.company.name}"