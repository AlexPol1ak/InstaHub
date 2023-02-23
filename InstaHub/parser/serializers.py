from rest_framework import serializers

from parser.models import InstaHub_instagram_accounts


class ServiceInstagramAccountSerializer(serializers.ModelSerializer):
    """
    Сериализатор для добавления, изменения, удаления данных авторизации
    аккаунта instagram.
    """
    class Meta:
        model = InstaHub_instagram_accounts
        fields = ('id', 'login_inst', 'password_inst', 'email', 'email_password', 'date_update', 'date_joined', 'blocked')
        extra_kwargs = {
            'date_joined': {'read_only': True},
            'blocked': {'read_only': True},
        }

class ServiceInstagramAccountBlockedSerializer(serializers.ModelSerializer):
    """Сериализатор для установки флага блокировки/разблокирвоки на аккаунт instagram."""

    class Meta:
        model = InstaHub_instagram_accounts
        fields = ('id', 'blocked', 'date_update')
        extra_kwargs = {
            'id': {'read_only': True},
            'blocked': {'required': True},
            'date_update': {'read_only': True},
                        }