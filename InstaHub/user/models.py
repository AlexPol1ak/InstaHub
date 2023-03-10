from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models
from django.utils import timezone

from parser.instagram_parser import InstagramParser
from user.managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    """Модель личных данных пользователя."""

    login = models.CharField(max_length=40, unique=True, verbose_name='Логин')
    first_name = models.CharField(max_length=40, blank=True, verbose_name='Имя')
    last_name = models.CharField(max_length=40, blank=True, verbose_name='Фамилия')
    email = models.EmailField(max_length=40, unique=True, verbose_name= 'email')
    phone_number = PhoneNumberField(null=True, unique=True, verbose_name='Номер телефона')
    date_birth = models.DateField(null=True, verbose_name='Дата рождения')
    status = models.CharField(max_length=3, default='st', verbose_name='Тарифный план')
    is_staff = models.BooleanField(default=False)
    is_activ = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='Дата регистрации')

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользватель'
        verbose_name_plural = 'Пользователи'

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self

    def __str__(self):
        user = f"Login: {self.login}. email: {self.email}"
        return user

    parser = InstagramParser()



class User_instagram_account(models.Model):
    """Модель хранит данные пользователей для авторизации в instagram ."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, parent_link=True)
    login_inst = models.CharField(max_length=40, unique=True, blank=True, verbose_name='Instagram пользователя')
    password_inst = models.CharField(max_length=40, blank=True, verbose_name='Пароль пользователя')
    verification_code = models.CharField(max_length=40, blank=True, verbose_name='Код верификации')

    class Meta:
        verbose_name = 'Instagram аккаунт пользователя'
        verbose_name_plural = 'Instagram аккаунты пользователя'

    def __str__(self):
        return f'{self.user}: {self.login_inst}'

