from ingredients.models import Ingredient
from tags.models import Tag
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

User = get_user_model()


class Recipe(models.Model):
    """
    Рецепты.
    """
    author = models.ForeignKey(User,
                               verbose_name=('Автор'),
                               on_delete=models.CASCADE)
    name = models.CharField(max_length=80,
                            verbose_name='Название')
    text = models.TextField(max_length=500,
                            verbose_name='Описание')
    is_in_shopping_cart = models.BooleanField(default=False,
                                              verbose_name='в списке покупок')
    cooking_time = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(43200,
                                      'Вы указали время приготовления больше'
                                      'чем один месяц, вы уверены в'
                                      'корректности введённых данных?'),
                    MinValueValidator(1,
                                      'Время приготовления не может'
                                      'быть меньше одной минуты')],
        verbose_name='Время на приготовление в минутах'
        )
    image = models.ImageField(
        upload_to='recipes/', null=True, blank=True)
    tags = models.ManyToManyField(Tag, through='RecipeTag')

    def __str__(self) -> str:
        return f'id {self.id}: {self.name[:10]}'


class RecipeTag(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.tag} к рецепту {self.recipe}'


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient,
                                   related_name='ingredients_in_recipe',
                                   on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe,
                               related_name='ingredients',
                               on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField(
        verbose_name='количество',
        default=1,
        blank=True,
        null=True,
        validators=[MinValueValidator(1,
                                      'вес не может быть меньше одной десятой'
                                      'от одной единицы измерения'), ])

    def __str__(self) -> str:
        return f'Ингредиент {self.ingredient} в рецепте {self.recipe}'


class FavoriteRecipe(models.Model):
    who_favorited = models.ForeignKey(User,
                                      related_name='who_favorited',
                                      on_delete=models.CASCADE)
    favorited_recipe = models.ForeignKey(Recipe,
                                         related_name='is_favorited',
                                         on_delete=models.CASCADE)
