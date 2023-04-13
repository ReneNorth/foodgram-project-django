from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    USER: str = 'user'
    MODERATOR: str = 'moderator'
    ADMIN: str = 'admin'

    CHOICES = (
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    )
    
    username = models.CharField(max_length=150, unique=True)
    role = models.CharField(choices=CHOICES,
                            default='user',
                            max_length=128)


    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(fields=['username', 'email'],
                                    name='unique_user')
        ]

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    def __str__(self):
        return self.username
