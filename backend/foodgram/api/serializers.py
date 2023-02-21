from rest_framework import serializers
from recipe.models import Recipe



class RecipeSerializer(serializers.ModelSerializer):
    """
    http://localhost/api/docs/redoc.html#tag/Recepty/operation/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA%20%D1%80%D0%B5%D1%86%D0%B5%D0%BF%D1%82%D0%BE%D0%B2
    Страница доступна всем пользователям. Доступна фильтрация по избранному, автору, списку покупок и тегам.

    QUERY PARAMETERS
    page	
    integer
    Номер страницы.

    limit	
    integer
    Количество объектов на странице.

    is_favorited	
    integer
    Enum: 0 1
    Показывать только рецепты, находящиеся в списке избранного.

    is_in_shopping_cart	
    integer
    Enum: 0 1
    Показывать только рецепты, находящиеся в списке покупок.

    author	
    integer
    Показывать рецепты только автора с указанным id.

    tags	
    Array of strings
    Example: tags=lunch&tags=breakfast
    Показывать рецепты только с указанными тегами (по slug)
    """
    class Meta:
        model = Recipe
        fields = ['id', 'author', 'name', 'text']