import secrets
import string
import random

from rest_framework import serializers


class PasswordGeneration():
    """Класс для генерации паролей."""

    @staticmethod
    def get_random_password(max_length :int = 7) -> str:
        """Генерирует пароль из букв верхнего регистра, нижнего регистра, цифр."""

        raw_password = []
        for i in range(0, max_length):
            raw_password.append(secrets.choice(string.ascii_letters + string.digits))
        random.shuffle(raw_password)
        password = ''.join(raw_password)

        return password


class CurrentUserId(serializers.CurrentUserDefault):
    """Возвращает id текущего пользователя."""

    requires_context = True
    def __call__(self, serializer_field):
        return super().__call__(serializer_field).pk