from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from user.models import User, User_instagram_account
from user.utils import CurrentUserId


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
                  'is_staff', 'is_activ', 'date_joined',)


class UserUpdateDataSerializer(serializers.ModelSerializer):
    """Сериализатор для обновления информации пользователя."""
    class Meta:
        model = User
        fields = ('login', 'email', 'first_name', 'last_name', 'phone_number', 'date_birth',)


class UserUpdatePasswordSerializer(serializers.ModelSerializer):
    """Сериализатор для изменения пароля."""

    new_password = serializers.CharField(max_length=20, min_length=5, required=True, write_only=True, )  # validators=[validate_password]
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('new_password', 'old_password', 'id')
        extra_kwargs = {
            'password': {'read_only': True},
            'old_password': {'read_only': True},
            'id': {'read_only': True},
        }

    def validate_old_password(self, value):

        user = self.context['request'].user
        if user.check_password(value):
            return value
        else:
            raise serializers.ValidationError({"old_password": "Old password is not correct"})

    def validate_new_password(self, value):

        user = self.context['request'].user
        if user.check_password(value):
            raise serializers.ValidationError({'error': 'The new password matches the old password.'})
        else:
            return value

    def update(self, instance, validated_data):

        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance


class ResetPasswordSerializer(serializers.Serializer):
    """Сериализатор для сброса пароля"""

    login = serializers.CharField(max_length=40, required=True, write_only=True)
    email = serializers.EmailField(max_length=40, required=True, write_only=True)
    response = serializers.CharField(read_only=True)


class GetAllUserSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения всех пользователей"""
    class Meta:
        model = User
        fields = ('id', 'login', 'email', 'phone_number', 'date_joined')


class DestroyOrDeactivateSerializer(serializers.Serializer):
    """
    Сериализатор для деактивации или удаления пользователя.
    Сериализует введенный пароль для выполнения действия.
    """
    password = serializers.CharField(write_only=True, required=True)



class UserInstagramAccountSerializer(serializers.ModelSerializer):
    """
    Серилизатор для добавления, изменения, удаления пользователем данных авторизации
    аккаунта instagram.
     """
    user_id = serializers.HiddenField(default=CurrentUserId())
    login_inst = serializers.CharField(max_length=40, required=True,)
    password_inst = serializers.CharField(max_length=40, required=True)

    class Meta:
        model = User_instagram_account
        fields = ('user_id', 'login_inst', 'password_inst', 'verification_code')




