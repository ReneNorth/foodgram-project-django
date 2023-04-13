from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from rest_framework import serializers
from rest_framework.validators import ValidationError
from django.shortcuts import get_object_or_404
from ingredients.models import Ingredient
from recipe.models import FavoriteRecipe, Recipe, RecipeIngredient
from tags.models import Tag
from subscription.models import Subscription
from shopping_cart.models import InShoppingCart
from users.serializers import CustomUserSerializer

import base64
import webcolors
from django.core.files.base import ContentFile


User = get_user_model()


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


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


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit']


class TagSerializer(serializers.ModelSerializer):
    color = Hex2NameColor()

    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug']


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

    # TODO оптимизация через related?
    def get_name(self, obj):
        return Ingredient.objects.get(id=obj.ingredient.id).name

    def get_measurement_unit(self, obj):
        return Ingredient.objects.get(id=obj.ingredient.id).measurement_unit


class RecipeRetreiveDelListSerializer(serializers.ModelSerializer):
    """ """
    author = CustomUserSerializer()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    # is_subscribed = serializers.SerializerMethodField()
    ingredients = RecipeIngredientSerializer(many=True)
    tags = TagSerializer(many=True)
    image = Base64ImageField(required=False, allow_null=True)

    # def get_is_subscribed(self, recipe):
    #     user = self.context.get('request').user
    #     if Subscription.objects.filter(author=recipe.author,
    #                                    user=user):
    #         return True
    #     return False

    def get_is_favorited(self, recipe):
        user = self.context.get('request').user
        if FavoriteRecipe.objects.filter(who_favorited=user,
                                         favorited_recipe=recipe).exists():
            return True
        return False

    def get_is_in_shopping_cart(self, recipe):
        user = self.context.get('request').user
        if InShoppingCart.objects.filter(user=user,
                                         recipe_in_cart=recipe).exists():
            return True
        return False

    class Meta:
        model = Recipe
        fields = ['id', 'tags', 'author', 'ingredients',
                  'is_favorited',
                #   'is_subscribed',
                  'is_in_shopping_cart',
                  'name', 'image', 'text',
                  'cooking_time', ]
        read_only_fields = ['id', 'tags', 'author', 'ingredients',
                            'is_favorited',
                            'is_in_shopping_cart', 'name', 'image', 'text',
                            'cooking_time', ]


class RecipeLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            'id', 'name', 'image',
            'cooking_time'
            ]


class RecipeCreatePatchSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all())
    ingredients = RecipeIngredientSerializer(many=True)
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Recipe
        fields = [
            'name', 'text', 'cooking_time', 'tags',
            'ingredients', 'image']

    def get_user(self, obj):
        if 'user' in self.context:
            return self.context['user']
        return None

    def create(self, validated_data):

        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        user = self.context['user']

        instance = Recipe.objects.create(author=user, **validated_data)
        instance.tags.set(tags)
        instance.save()
        for ingredient in ingredients:
            RecipeIngredient.objects.create(recipe=instance, **ingredient)
        return instance


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


class InShoppingCartSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    recipe_in_cart = serializers.SerializerMethodField()

    def get_user(self, obj):
        if "user" in self.context:
            return self.context["user"].id
        return None

    def get_recipe_in_cart(self, obj):
        if "recipe_in_cart" in self.context:
            return self.context["recipe_in_cart"].id
        return None

    class Meta:
        model = FavoriteRecipe
        fields = ['user', 'recipe_in_cart']

    def create(self, validated_data):
        user_id = self.context["user"].id
        recipe_id = self.context["recipe_in_cart"].id
        if InShoppingCart.objects.filter(user=user_id,
                                         recipe_in_cart_id=recipe_id):
            raise serializers.ValidationError('Нельзя добавить рецепт в '
                                              'избранные два раза')
        recipe_in_cart = InShoppingCart.objects.create(
            user_id=user_id,
            recipe_in_cart_id=recipe_id)
        recipe_in_cart.save()
        return recipe_in_cart


class SubscriptionCreateDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['user', 'author']
        read_only_fields = ['user', 'author']
        extra_kwargs = {
            'user': {'required': False},
            'author': {'required': False},
        }

    def create(self, validated_data):
        return Subscription.objects.create(**validated_data,
                                           user=self.context['user'],
                                           author=self.context['author'])

    def validate(self, data):
        if self.context['request'].method == 'POST':
            user = self.context['user'].id
            author = self.context['author'].id
            if author == user:
                raise ValidationError('Нельзя подписаться на себя!')
            if Subscription.objects.filter(user__id=user,
                                           author__id=author).exists():
                raise ValidationError('Нельзя подписаться два раза')
        return data


class SubscriptionListSerializer(serializers.ModelSerializer):
    """lists authors the user is subscribed to and their recipes"""
    recipes = RecipeLightSerializer(many=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'id', 'first_name', 'last_name', 'username',
                  'is_subscribed',
                  'recipes',
                  ]

    def get_is_subscribed(self, author):
        user = self.context.get('request').user
        if Subscription.objects.filter(author=author,
                                       user=user):
            return True
        return False
