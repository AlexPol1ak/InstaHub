import secrets
import string
import random

class PasswordGeneration():
    """Класс для генерации паролей."""

    @staticmethod
    def get_random_password(max_length :int = 7) -> str:
        """Генерирует пароль из букв верхнего регистра, нижнего регистра, цифр."""

        raw_password = []
        for i in range(0, max_length):
            raw_password.append(secrets.choice(string.ascii_letters + string.digits))
        random.shuffle(raw_password)
        password = ''.join(raw_password)

        return password

tup = (10,20,30)
a, *b, c = tup 
print(b)