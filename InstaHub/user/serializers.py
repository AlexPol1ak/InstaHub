from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from user.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователя."""

    class Meta:
        model = User
        fields = ('login', 'password', 'email', 'first_name', 'last_name', 'phone_number', 'date_birth',)


    def validate_password(self, value: str) -> str:

        return make_password(value)

class RetrieveUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'login', 'email', 'first_name', 'last_name', 'phone_number', 'date_birth', 'status',
                  'is_stuff', 'is_activ', 'date_joined')