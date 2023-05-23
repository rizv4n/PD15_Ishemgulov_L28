from django.db import models
from django.contrib.auth.models import AbstractUser


class UserRoles(models.TextChoices):
    MEMBER = 'member', 'Пользователь'
    ADMIN = 'admin', 'Администратор'
    MODERATOR = 'moderator', 'Модератор'


class User(AbstractUser):

    age = models.PositiveSmallIntegerField()
    role = models.CharField(max_length=9, choices=UserRoles.choices, default=UserRoles.MEMBER)
    birthday = models.DateField()
    email = models.EmailField(max_length=200, unique=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']

    def __str__(self):
        return self.username
