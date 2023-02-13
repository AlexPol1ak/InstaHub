from django.core.mail import send_mail
from django.utils import timezone

from InstaHub.settings import EMAIL_HOST_USER
from user.models import User


class MessagesSender():
    """Содержит функционал для отправки сообщений пользователю."""

    def __init__(self, user: User):
        """Инициализация пользователя."""
        self.__user = user
        self.__signature = '\nInstaHub service'

    def send_email_reset_password(self, password: str):
        """Отправляет пользователю уведомление о смене пароля."""

        title = 'Сброс пароля'
        text = f'Поступил запрос на сброс пароля. Старый пароль сброшен.\nУстановлен новый пароль: {password}\n' \
               f'Не кому не сообщайте новый пароль. Вы можете изменить его в личном кабинете.'
        time = timezone.now().strftime('%d-%m-%Y %H:%M')
        message = text + '\n' + time + '\n' + self.__signature

        send_mail(
            title,
            message,
            recipient_list=[self.__user.email],
            from_email=EMAIL_HOST_USER,
            fail_silently=False,
            )
        return 'New password sent to your email.'
