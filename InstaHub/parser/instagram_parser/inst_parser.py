import random
import time

from instagrapi import Client

from parser.models import InstaHubInstagramAccounts
from user.models import User, User_instagram_account


class _InstConnect():
    """Подключение к instagram."""

    def __init__(self):
        """Инициализация данных авторизации в instagram"""
        # login: str = None, password: str = None, *, proxy: str | list = None, verification_code: str = None

        self.login = ''
        self.__password = ''
        self.verification_code = ''
        self.proxy = ''
        # флаг авторизации в instagram
        self.inst_connecting = False
        # предоставляет API для парсинга instagram
        self.client = Client()

    def connect_inst(self, pk: int):
        """Соединение с Instagram."""
        if not self.inst_connecting:
            if self._install_inst_auth_data(pk=pk):
                self.client.login(self.login, self.__password)

                self.inst_connecting = True
        return self.client

    def disconnect_inst(self):
        """Выход с учетной записи instagram."""
        if self.inst_connecting:
            self.client.logout()
            self.inst_connecting = False
        return self.inst_connecting

    def _install_inst_auth_data(self, pk):
        """Установка данных авторизации для подключения к instagram."""
        if self._install_user_inst_auth_data(pk):
            return True
        elif self._install_service_inst_auth_data(pk):
            return True

    def _install_user_inst_auth_data(self, pk: int):
        """Получает логин и пароль для instagram от пользователя."""

        try:
            # Получаем логин и пароль от instagram от пользователя, если пользователь их указал.
            # Устанавливаем в качестве данных для подключения к instagram
            user_inst = User_instagram_account.get(user_id=pk)
            self.login = user_inst.login_inst
            self.__password = user_inst.password_inst
            # Возвращаем флаг для подключения
            return True
        # Если пользователь не сохранил логин или пароль-вернуть False в функцию подключения.
        except User_instagram_account.DoesNotExist:
            raise FileNotFoundError('Пользователь не указал данные от instagram')

    def _install_service_inst_auth_data(self, pk):
        """
        Получает случайный логин и пароль для instagram из БД принадлежащих сервису InstaHub.
        """
        # Если статус пользователя выше чем стандарт
        if User.objects.get(pk=pk).status == 'st':
            raise PermissionError('Недостаточный статус для использования аккаунтов сервиса InstaHub')

        else:
            users = InstaHubInstagramAccounts.objects.filter(blocked=False)
            if len(users) == 0:
                raise FileNotFoundError('Отсутствуют не заблокированные аккаунты')

            user_inst = random.choice(users)
            self.login = user_inst.login_inst
            self.__password = user_inst.password_inst

        return True

class _ActionsCounter(_InstConnect):
    """Счетчик действий."""

    def __init__(self):
        super().__init__() # <- _InstConnect

        self.value_counter = 0

    def _check_counter(self, max_value: int = 250):
        """Проверяет значение счетчика"""
        if self.value_counter > max_value:
            raise ConnectionError(f'Превышено максимальное число действий {max_value}.')

    def add_counter_action(self, max_value=250):
        """
        Проверяет достижение счетчиком максимального значения, и увеличивает счетчик на 1 шаг.
        Максимальное значение по умолчанию 250.
        """
        self._check_counter(max_value=max_value)
        self.value_counter += 1
        return self.value_counter

    def reset_counter(self):
        """Сбрасывает значение счетчика"""
        self.value_counter = 0

class _GetUserInfo():
    """Предоставляет данные о пользователе instagram."""

    def get_user_info(self, user_name:str):
        """Предоставляет данные о пользователе instagram."""
        time.sleep(2)
        data = self.client.user_info_by_username(user_name)
        return data


class _GetFollowers():
    """Получить всех подписчиков."""

    def get_followers(self, inst_user: str|int):
        """Получает id по user_name, получает всех подписчиков"""
        time.sleep(2)
        if isinstance(inst_user, str):
            user_id = self.client.user_id_from_username(inst_user)
            data = self.client.user_followers(user_id)
        elif isinstance(inst_user, int):
            data = self.client.user_followers(inst_user)
        else:
            raise TypeError('Аргумент должен быть строкой-именем пользователя или целым числом id.')
        return data

class _GetFollowing():
    """Получить всех подписчиков."""

    def get_following(self, inst_user: str|int):
        """Получает id по user_name, получает всех подписчиков"""
        time.sleep(2)
        if isinstance(inst_user, str):
            user_id = self.client.user_id_from_username(inst_user)
            data = self.client.user_following(user_id)
        elif isinstance(inst_user, int):
            data = self.client.user_following(inst_user)
        else:
            raise TypeError('Аргумент должен быть строкой-именем пользователя или целым числом id.')
        return data


class _InstagramActionsMixin(_ActionsCounter, _GetUserInfo, _GetFollowers, _GetFollowing):
    """Аккумулируeт все действия с профилем instagram."""
    def __init__(self):
        """Инициализация функционала внутреннего счетчика действий и функционала подключения к isntagram."""
        super().__init__() # <-_ActionsCounter , + _InstConnect

class InstagramParser(_InstagramActionsMixin):
    """Instagram parser."""
    def __init__(self):
        """Инициализация функционала действий парсера """
        super().__init__()

    def __str__(self):
        return f'Object  {self.__class__}. Connecting {self.login}'


# from parser.instagram_parser import InstagramParser
# p = InstagramParser()
# p.value_counter
