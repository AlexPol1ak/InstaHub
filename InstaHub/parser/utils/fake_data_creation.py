from random import random, randint

from django.utils import timezone
from mimesis import Person, Text
from mimesis.enums import Gender


class FakeInstagramProfile():
    """Класс представляет фальшивый профиль instagram"""

    def __init__(self,
                 i_d: int = 1,
                 user_name: str = 'Default_user_name',
                 name: str = 'Default_name',
                 profile_bio: str = 'Default_profile_bio',
                 number_publications: int = 2,
                 profile_link = 'https://www.django-rest-framework.org/',
                 followers=None,
                 following=None,
                 ):

        """Иницилизация данных пользователя"""
        if following is None:
            following = []
        if followers is None:
            followers = []
        self.id = int(i_d)
        self.user_name = str(user_name)
        self.name = str(name)
        self.profile_bio = str(profile_bio)
        self.number_publications = int(number_publications)
        self.profile_link = profile_link
        self.followers = list(followers)
        self.following = list(following)
        self.data_joined = timezone.now

    def __str__(self):
        return f'{self.id}. {self.user_name}'



class CreateFakeInstagramProfiles(FakeInstagramProfile):
    """Генерирует фальшивый профиль instagram c случайными данными"""

    def __init__(self, language: str = 'ru', gender :str = 'male',):
        """Инициализация случайного фальшивого профиля."""

        if gender != 'male' and gender != 'female':
            raise ValueError('Gender должен быть female или male.')

        self.person = Person(language)
        self.gender = gender
        super().__init__(
            i_d= randint(1, 100**2),
            user_name = self.person.username(),
            name = self.person.name(gender=Gender(self.gender)),
            profile_bio = Text().text(3),
            number_publications = randint(1, 1000)
        )
    @staticmethod
    def many(language: str = 'ru', gender :str = 'male', number: int =2) -> list:
        """Создает указанное количество фальшивых профилей"""

        if number <1:
            raise ValueError(f'Количество пользователей должно быть больше {number}')
        else:
            users_lst = []
            for i in range(1, number+1):
                users_lst.append(CreateFakeInstagramProfiles(language, gender))

        return users_lst
