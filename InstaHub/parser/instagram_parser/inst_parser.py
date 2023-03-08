import time
from instagrapi import Client


class _InstConnect():
    """Подключение к instagram."""

    def __init__(self, login: str = None, password: str = None, *, proxy: str | list = None,
                 verification_code: str = None):
        """Инициализация данных авторизации в instagram"""

        self.login = login
        self.__password = password
        self.verification_code = verification_code
        self.proxy = proxy
        # флаг авторизации в instagram
        self.inst_connecting = False
        # предоставляет API для парсинга instagram
        self.client = Client()

    def connect_inst(self, pk: int):
        """Соединение с Instagram."""

        if not self.login and not self.__password:
            raise ConnectionError('Отсутствует логин и пароль для подключения')
        elif not self.inst_connecting:
            flag = self.client.login(username=self.login, password=self.__password,
                                     verification_code=self.verification_code if self.verification_code else "")
            if not flag:
                return ConnectionAbortedError('Соединение отменено instagram')

        self.inst_connecting = True
        return self.client

    def disconnect_inst(self):
        """Выход с учетной записи instagram."""
        if self.inst_connecting:
            self.client.logout()
            self.inst_connecting = False
        return self.inst_connecting


class _ActionsCounter(_InstConnect):
    """Счетчик действий."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # <- _InstConnect

        self.value_counter = 0
        self.max_value = 250

    def _check_counter(self):
        """Проверяет значение счетчика"""
        if self.value_counter > self.max_value:
            raise ConnectionError(f'Превышено максимальное число действий {self.max_value}.')

    def add_counter_action(self):
        """
        Проверяет достижение счетчиком максимального значения, и увеличивает счетчик на 1 шаг.
        Максимальное значение по умолчанию 250.
        """
        self._check_counter()
        self.value_counter += 1
        return self.value_counter

    def reset_counter(self):
        """Сбрасывает значение счетчика"""
        self.value_counter = 0


class _GetUserInfo():
    """Предоставляет данные о пользователе instagram."""

    def get_user_info(self, user_name: str):
        """Предоставляет данные о пользователе instagram."""
        # self.add_counter_action()

        time.sleep(2)
        data = self.client.user_info_by_username(user_name)
        return data


class _GetFollowers():
    """Получить всех подписчиков."""

    def get_followers(self, inst_user: str | int):
        """Получает id по user_name, получает всех подписчиков"""
        # self.add_counter_action()

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

    def get_following(self, inst_user: str | int):
        """Получает id по user_name, получает всех подписчиков"""
        # self.add_counter_action()

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

    def __init__(self, *args, **kwargs):
        """Инициализация функционала внутреннего счетчика действий и функционала подключения к isntagram."""
        super().__init__(*args, **kwargs)


class InstagramParser(_InstagramActionsMixin):
    """Instagram parser."""

    def __init__(self, login: str = None, password: str = None, *, proxy: str | list = None,
                 verification_code: str = None):
        """Инициализация функционала действий парсера """
        super().__init__(login=login, password=password, proxy=proxy, verification_code=verification_code)
        # MRO
        # (<class 'parser.instagram_parser.inst_parser.InstagramParser'>,
        # <class 'parser.instagram_parser.inst_parser._InstagramActionsMixin'>,
        # <class 'parser.instagram_parser.inst_parser._ActionsCounter'>,
        # <class 'parser.instagram_parser.inst_parser._InstConnect'>,
        # <class 'parser.instagram_parser.inst_parser._GetUserInfo'>,
        # <class 'parser.instagram_parser.inst_parser._GetFollowers'>,
        # <class 'parser.instagram_parser.inst_parser._GetFollowing'>,
        # <class 'object'>)

    def __str__(self):
        return f'Object  {self.__class__}. Connecting {self.login}'

# from parser.instagram_parser import InstagramParser
# p = InstagramParser()
# p.value_counter
