from rest_framework import serializers
from recipe.models import Recipe, FavoriteRecipe
from ingredients.models import Ingredient
from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
# from users.models import User

User = get_user_model()


class CustomUserSerilizer(UserSerializer):
    class Meta:
        # add is_subscribed to fields  
        model = User
        fields = ['email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed']


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit']


class FavoriteSerializer(serializers.ModelSerializer):
    who_favorited = serializers.SerializerMethodField()
    favorited_recipe = serializers.SerializerMethodField()

    def get_who_favorited(self, obj):
        if "who_favorited" in self.context:
            return self.context["who_favorited"].id
        return None

    def get_favorited_recipe(self, obj):
        if "favorited_recipe" in self.context:
            return self.context["favorited_recipe"].id
        return None

    class Meta:
        model = FavoriteRecipe
        fields = ['who_favorited', 'favorited_recipe']

    def create(self, validated_data):
        favorite_recipe = FavoriteRecipe.objects.create(
            who_favorited_id=self.context["who_favorited"].id,
            favorited_recipe_id=self.context["favorited_recipe"].id)
        favorite_recipe.save()
        return favorite_recipe


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
    author = CustomUserSerilizer()
    is_favorited = serializers.SerializerMethodField()

    def get_is_favorited(self, recipe):
        user = self.context.get("request").user
        # TODO оптимизировать запрос
        if FavoriteRecipe.objects.filter(who_favorited=user,
                                         favorited_recipe=recipe):
            return True
        return False

    class Meta:
        model = Recipe
        fields = ['id', 'author', 'name', 'image',
                  'text', 'cooking_time', 'is_favorited']

        extra_kwargs = {
            'is_favorited': {'read_only': True},
        }
