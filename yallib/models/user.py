from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
    )


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Создаем и сохраняем Юзера с полученным емаил и парол
        """
        if not email:
            raise ValueError("User must have a email address")

        user = self.model(email=self.normalize_email(email),)

        user.set_password(password)

        user.save(using=self.db)

        return user

    def create_staffuser(self, email, password):
        """
        Создаем и сохраняем stuff user с полученным емаил и паролем
        """
        user = self.create_user(
            email,
            password=password,
            )
        user.staff = True

        user.save(using=self.db)
        return user

    def create_superuser(self, email, password):
        """
        Создаем и сохраняем супепользователя с получением емаил и пароль
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self.db)
        return user


class User(AbstractBaseUser):  # создаем таблицу пользователь в БД

    email = models.EmailField(
        verbose_name='email address',  max_length=100, unique=True
    )
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)  # admin User
    admin = models.BooleanField(default=False)  # super User
    ORDER_STATUS = (
        ("0", "BLOCKED"),
        ("1", "ACTIVE"),
        ("2", "DELETED"),
        ("3", "SUSPENDED"),
    )
    status = models.IntegerField(default=0, choices=ORDER_STATUS)

    objects = UserManager()
    # поле пароль встроено в settings стр 90-102
    USERNAME_FIELD = 'email'  # django заменяет встроенное поле имени
    # пользователя на емаил
    REQUIRED_FIELDS = []  # email & password по умолчанию

    def get_full_name(self):
        # авторизация пользователя идентифицируется по email
        return self.email

    def __str__(self):
        # возвращаем полученный email строкой
        return self.email

    def has_perm(self, perm, obj=None):
        # always True/Yes
        return True

    def has_module_perms(self, app_label):
        # имеет ли пользователь права на просмтр приложения
        return True

    @property  # декоратор для контроля за проавами доступа
    def is_staff(self):
        # проверяем является ли пользователь членом персонала
        return self.staff  # берем таблицу staff

    @property
    def is_admin(self):
        # проверяем является ли пользователь super User
        return self.admin  # берем таблицу admin

    @property
    def is_active(self):
        # является ли пользователь активированным
        return self.active  # берем таблицу active
