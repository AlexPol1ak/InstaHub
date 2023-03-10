from rest_framework import serializers

from parser.models import InstaHubInstagramAccounts, TrackedUsers


class ServiceInstagramAccountSerializer(serializers.ModelSerializer):
    """
    Сериализатор для добавления, изменения, удаления данных авторизации
    аккаунта instagram.
    """
    class Meta:
        model = InstaHubInstagramAccounts
        fields = ('id', 'login_inst', 'password_inst','verification_code',
                  'email', 'email_password', 'date_update', 'date_joined', 'blocked', )
        extra_kwargs = {
            'date_joined': {'read_only': True},
            'blocked': {'read_only': True},
        }

class ServiceInstagramAccountBlockedSerializer(serializers.ModelSerializer):
    """Сериализатор для установки флага блокировки/разблокирвоки на аккаунт instagram."""

    class Meta:
        model = InstaHubInstagramAccounts
        fields = ('id', 'blocked', 'date_update')
        extra_kwargs = {
            'id': {'read_only': True},
            'blocked': {'required': True},
            'date_update': {'read_only': True},
                        }


class AddTrackedUserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для добавления пользователя instagram в список отслеживаемых или получения списка всех отслеживаемых
    """

    class Meta:
        model = TrackedUsers
        fields = ('id','user', 'user_name', 'profile_link', 'id_instagram')
        read_only_fields = ('id', 'user', 'profile_link', 'id_instagram')
