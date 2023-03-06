import random

from parser.models import InstaHubInstagramAccounts
from user.models import User_instagram_account, User


def user_inst_auth_data(user: User) -> User_instagram_account | None:
    """Возвращает объект для аутентификации от instagram пользователя"""
    try:
        inst_data = User_instagram_account.objects.get(user_id=user.pk)
        return inst_data
    except User_instagram_account.DoesNotExist:
        return None


def service_inst_auth_data(user: User) -> InstaHubInstagramAccounts | None:
    """
    Возвращает объект для аутентификации от случайного instagram аккаунта, принадлежащих сервису.
    """

    if user.status != 'st':
        inst_accounts = InstaHubInstagramAccounts.objects.filter(blocked=False)
        inst_data = random.choice(inst_accounts)
        return inst_data
    else:
        return None


def get_inst_auth_data(user: User) -> User_instagram_account | InstaHubInstagramAccounts |None:
    """Возвращает объект для аутентификации в instagram."""

    inst_data = user_inst_auth_data(user=user)
    if not inst_data:
        inst_data = service_inst_auth_data(user=user)

    return inst_data
