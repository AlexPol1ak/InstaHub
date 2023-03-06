from django.contrib.auth.base_user import BaseUserManager
from django.db import transaction


class UserManager(BaseUserManager):
    """Менеджер для создания пользователей."""

    def create_user(self, login, password, first_name, last_name, email, phone_number, date_birth, alias=None):

        with transaction.atomic():
            user = self.model(
                login=login,
                first_name=first_name,
                last_name=last_name,
                email = self.normalize_email(email),
                phone_number=phone_number,
                date_birth=date_birth
            )
            user.set_password(password)
            user.save()
            return user

    def create_superuser(self, login, password, first_name, last_name, email, phone_number, date_birth):

        user = self.create_user(login, password, first_name, last_name, email, phone_number, date_birth)
        user.is_stuff = True
        user.status = 'PRO'
        user.is_superuser = True
        user.save()

        return user




