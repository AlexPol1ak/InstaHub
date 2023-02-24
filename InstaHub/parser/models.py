from django.db import models
from django.utils import timezone

# Установить связи между таблицами. Провести миграции. Определить декодер json !!!

class InstaHub_instagram_accounts(models.Model):
    """Модель хранит данные для авторизации в instagram аккаунтов принадлежавших сервису."""

    login_inst = models.CharField(max_length=40, unique=True, blank=False, verbose_name='Instagram логин')
    password_inst = models.CharField(max_length=40, blank=False, verbose_name='Instagram пароль')
    email = models.EmailField(max_length=40, blank=True, verbose_name='email')
    email_password = models.CharField(max_length=40, blank=True, verbose_name='Пароль email')
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='Дата регистрации')
    date_update = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    blocked = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Аккаунты instagram'
        verbose_name_plural = 'Аккаунты instagram'

    def __str__(self):
        return f'{self.pk}. {self.login_inst} -blocked: {self.blocked}'


class Tracked_users(models.Model):
    """Модель отслеживаемых пользователей."""

    id_instagram = models.PositiveBigIntegerField(unique=True, blank=False, verbose_name='id аккаунта instagram')
    user_name = models.CharField(max_length=40, unique=True, blank=False, verbose_name='Уникальное имя в instagram')
    profile_link = models.URLField(verbose_name='Ссылка на профиль')
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Отслеживаемые профили'
        verbose_name_plural = 'Отслеживаемые профили'

    def __str__(self):
        return f'id_inst:{self.id_instagram} -user_name:{self.user_name}'



class Screenshot_profile(models.Model):
    """Модель хранения состояний отслеживаемого аккаунта instagram."""

    name = models.CharField(max_length=40, blank=True,verbose_name='Собственно имя')  # Не уникальное, Собственное имя пользователя
    profile_bio = models.CharField(max_length=100, verbose_name='Биография в профиле')
    number_publications = models.IntegerField(verbose_name='Количество публикаций')
    followers = models.JSONField(verbose_name='Подписчики')
    following = models.JSONField(verbose_name='Подписки')
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='Дата фиксации состояния ')

    class Meta:
        verbose_name = 'Состояние профиля instagram'
        verbose_name_plural = 'Состояния профилей instagram'
