import webcolors

from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from rest_framework import serializers

from ingredients.models import Ingredient
from recipe.models import FavoriteRecipe, Recipe, RecipeIngredient
from tags.models import Tag


User = get_user_model()


class CustomUserSerilizer(UserSerializer):
    class Meta:
        model = User
        fields = ['email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed']


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit']


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class RecipeIngredientSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    measurement_unit = serializers.SerializerMethodField()

    class Meta:
        model = RecipeIngredient
        fields = [
                  'ingredient',  # переименовать поле на id?
                  'name',
                  'measurement_unit',
                  'amount',
                  ]
        extra_kwargs = {
            'measurement_unit': {'read_only': True},
            'name': {'read_only': True},
        }

    def get_name(self, obj):
        return Ingredient.objects.get(id=obj.ingredient.id).name

    def get_measurement_unit(self, obj):
        return Ingredient.objects.get(id=obj.ingredient.id).measurement_unit


class RecipeRetreiveDelListSerializer(serializers.ModelSerializer):
    """ """
    author = CustomUserSerilizer()
    is_favorited = serializers.SerializerMethodField()
    ingredients = RecipeIngredientSerializer(many=True)
    tags = TagSerializer(many=True)

    def get_is_favorited(self, recipe):
        user = self.context.get("request").user
        # TODO оптимизировать запрос
        if FavoriteRecipe.objects.filter(who_favorited=user,
                                         favorited_recipe=recipe):
            return True
        return False

    class Meta:
        model = Recipe
        fields = ['id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time', ]

        extra_kwargs = {
            'is_favorited': {'read_only': True},
        }


class RecipeCreatePatchSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all())
    ingredients = RecipeIngredientSerializer(many=True)

    class Meta:
        fields = [
            'name', 'text', 'cooking_time', 'tags',
            'ingredients',
        ]
        model = Recipe

    def get_user(self, obj):
        if "user" in self.context:
            return self.context["user"]
        return None

    def create(self, validated_data):

        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        user = self.context["user"]

        instance = Recipe.objects.create(author=user, **validated_data)
        instance.tags.set(tags)
        instance.save()
        for ingredient in ingredients:
            print(ingredient)
            RecipeIngredient.objects.create(recipe=instance, **ingredient)
        return instance


class Hex2NameColor(serializers.Field):
    # При чтении данных ничего не меняем - просто возвращаем как есть
    def to_representation(self, value):
        return value
    # При записи код цвета конвертируется в его название
    def to_internal_value(self, data):
        # Доверяй, но проверяй
        try:
            # Если имя цвета существует, то конвертируем код в название
            data = webcolors.hex_to_name(data)
        except ValueError:
            # Иначе возвращаем ошибку
            raise serializers.ValidationError('Для этого цвета нет имени')
        # Возвращаем данные в новом формате
        return data


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
        user_id = self.context["who_favorited"].id
        recipe_id = self.context["favorited_recipe"].id
        if FavoriteRecipe.objects.filter(who_favorited_id=user_id,
                                         favorited_recipe_id=recipe_id):
            raise serializers.ValidationError('Нельзя добавить рецепт в '
                                              'избранные два раза')
        favorite_recipe = FavoriteRecipe.objects.create(
            who_favorited_id=user_id,
            favorited_recipe_id=recipe_id)
        favorite_recipe.save()
        return favorite_recipe
