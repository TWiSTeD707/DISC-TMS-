from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Company

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    company_name = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['email', 'password', 'role', 'company_name']

    def create(self, validated_data):
        company_name = validated_data.pop('company_name', None)
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role']
        )

        if user.role == "company" and company_name:
            company = Company.objects.create(name=company_name)
            user.company = company
            user.save()

        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()