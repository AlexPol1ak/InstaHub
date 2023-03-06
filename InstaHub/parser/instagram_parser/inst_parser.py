import time
from instagrapi import Client




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
        #add code
        return self.client

    def disconnect_inst(self):
        """Выход с учетной записи instagram."""
        if self.inst_connecting:
            self.client.logout()
            self.inst_connecting = False
        return self.inst_connecting



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
    """Аккумулирует все действия с профилем instagram."""
    def __init__(self):
        """Инициализация функционала внутреннего счетчика действий и функционала подключения к isntagram."""
        super().__init__() # <-_ActionsCounter , + _InstConnect

class InstagramParser(_InstagramActionsMixin):
    """Instagram parser."""
    def __init__(self, **kwargs):
        """Инициализация функционала действий парсера """
        super().__init__()
        self.kwargs = kwargs


    def __str__(self):
        return f'Object  {self.__class__}. Connecting {self.login}'


# from parser.instagram_parser import InstagramParser
# p = InstagramParser()
# p.value_counter
