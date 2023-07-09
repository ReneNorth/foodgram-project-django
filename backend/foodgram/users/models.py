from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER: str = 'user'
    ADMIN: str = 'admin'
    CHOICES = (
        (USER, 'user'),
        (ADMIN, 'admin'),
    )
    role = models.CharField(choices=CHOICES,
                            default='user',
                            max_length=128)

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    class Meta:
        ordering = ['id']
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        constraints = [
            models.UniqueConstraint(fields=['username', 'email'],
                                    name='unique_user')
        ]

    def __str__(self):
        return self.username
