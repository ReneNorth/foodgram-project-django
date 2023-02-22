from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Recipe(models.Model):
    """
    Рецепт должен описываться такими полями:
    Автор публикации (пользователь).
    Название.
    Картинка.
    Текстовое описание.
    Ингредиенты: продукты для приготовления блюда по рецепту. Множественное поле, выбор из предустановленного списка, с указанием количества и единицы измерения.
    Тег (можно установить несколько тегов на один рецепт, выбор из предустановленных).
    Время приготовления в минутах.
    """
    author = models.ForeignKey(User,
                               verbose_name=('Автор'),
                               on_delete=models.CASCADE)
    name = models.CharField(max_length=80,
                             verbose_name='Название')
    text = models.TextField(max_length=500,
                                   verbose_name='Описание')
    cooking_time = models.SmallIntegerField(
        verbose_name='Время на приготовление в минутах')
    image = models.ImageField(
        upload_to='recipes/', null=True, blank=True)
    # ingredients = 
    # tags = 
    # is_favorited
    # is_in_shopping_cart
    
    
    