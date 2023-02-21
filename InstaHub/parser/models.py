from django.db import models
from django.utils import timezone


class InstaHub_instagram_accounts(models.Model):
    """Модель хранит данные для авторизации в instagram аккаунтов принадлежавших сервису."""

    login_inst = models.CharField(max_length=40, unique=True, blank=False, verbose_name='Instagram логин')
    password_inst = models.CharField(max_length=40, blank=False, verbose_name='Instagram пароль')
    email = models.EmailField(max_length=40, unique=True, blank=True,  verbose_name= 'email')
    email_password = models.CharField(max_length=40, blank=True, verbose_name='Пароль email')
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='Дата регистрации')
    date_update = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    blocked = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.pk}. {self.login_inst} -blocked: {self.blocked}'
