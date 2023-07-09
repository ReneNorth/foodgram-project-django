from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from ingredients.models import Ingredient
from tags.models import Tag

User = get_user_model()


class Recipe(models.Model):
    author = models.ForeignKey(User,
                               related_name='recipes',
                               verbose_name='Author',
                               on_delete=models.CASCADE,
                               help_text='Author of the recipe')
    name = models.CharField(max_length=80,
                            verbose_name='Name',
                            help_text='Name of the recipe')
    text = models.TextField(max_length=500,
                            verbose_name='Description')
    cooking_time = models.PositiveSmallIntegerField(
        validators=[
            MaxValueValidator(
                43200, 'Time of cooking cannot exceed one month'),
            MinValueValidator(
                1, 'The cooking tine cannot be less than 1 minute')],
        verbose_name='time for cooking in minutes')
    image = models.ImageField(
        upload_to='recipes/', default=None)
    tags = models.ManyToManyField(Tag, through='RecipeTag')
    ingredients = models.ManyToManyField(
        Ingredient, through='RecipeIngredient')
    pub_date = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return f'id {self.id}: {self.name[:10]}'


class RecipeTag(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE,
                            related_name='tags')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.tag} for the recipe {self.recipe}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['tag', 'recipe'],
                                    name='unique tag-recipe pair')
        ]


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient,
                                   on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField(
        verbose_name='quantity',
        default=1,
        validators=[MinValueValidator(1, 'the weight cannot be less than 1')])

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['ingredient', 'recipe'],
                                    name='unique ingredient per recipe')
        ]

    def __str__(self) -> str:
        return f'Ингредиент {self.ingredient} в рецепте {self.recipe}'


class FavoriteRecipe(models.Model):
    who_favorited = models.ForeignKey(User,
                                      related_name='who_favorited',
                                      on_delete=models.CASCADE)
    favorited_recipe = models.ForeignKey(Recipe,
                                         related_name='is_favorited',
                                         on_delete=models.CASCADE)

    def __str__(self) -> str:
        return (f'{self.who_favorited}'
                f'added to favorite a recipe {self.favorited_recipe}')
