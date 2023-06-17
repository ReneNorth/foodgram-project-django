from django.contrib.auth import get_user_model
from django.db import models

from recipe.models import Recipe

User = get_user_model()


class InShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopper'
    )

    recipe_in_cart = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='is_in_cart'
    )

    class Meta:
        models.UniqueConstraint(
            fields=['user', 'is_in_cart'], name='already_in_cart'
        )

    def __str__(self) -> str:
        return f'{self.user} added to {self.recipe_in_cart} to cart'
