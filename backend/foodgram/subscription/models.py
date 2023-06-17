from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber'
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribed'
    )

    class Meta:
        models.UniqueConstraint(
            fields=['user', 'author'], name='already_following'
        )

    def __str__(self) -> str:
        return f'{self.user} subscribed to {self.author}'
