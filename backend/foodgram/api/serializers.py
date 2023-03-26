import webcolors

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.serializers import UserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator, ValidationError

from ingredients.models import Ingredient
from recipe.models import FavoriteRecipe, Recipe, RecipeIngredient
from tags.models import Tag
from subscription.models import Subscription

import base64  
from django.core.files.base import ContentFile


User = get_user_model()


class CustomUserSerilizer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['email', 'id', 'username', 'first_name',
                  'last_name',
                  'is_subscribed'
                  ]
    
    def get_is_subscribed(self, author):
        user = self.context.get('request').user
        # TODO оптимизировать запрос
        # if 1 == 1:
        # if get_object_or_404(Subscription, author=author, user=user):
        if Subscription.objects.filter(author=author,
                                       user=user):
            return True
        return False


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        # Если полученный объект строка, и эта строка 
        # начинается с 'data:image'...
        if isinstance(data, str) and data.startswith('data:image'):
            # ...начинаем декодировать изображение из base64.
            # Сначала нужно разделить строку на части.
            format, imgstr = data.split(';base64,')  
            # И извлечь расширение файла.
            ext = format.split('/')[-1]  
            # Затем декодировать сами данные и поместить результат в файл,
            # которому дать название по шаблону.
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


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

    # TODO оптимизация через related?
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
    image = Base64ImageField(required=False, allow_null=True)

    def get_is_favorited(self, recipe):
        user = self.context.get('request').user
        # TODO оптимизировать запрос get_object_or_404
        if FavoriteRecipe.objects.filter(who_favorited=user,
                                         favorited_recipe=recipe):
            return True
        return False

    class Meta:
        model = Recipe
        fields = ['id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time', ]
        # read_only_fields = 
        extra_kwargs = {
            'is_favorited': {'read_only': True},
        }


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

    class Meta:
        model = Recipe
        fields = [
            'name', 'text', 'cooking_time', 'tags',
            'ingredients', ]

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


class SubscriptionListRecipeSerializer(serializers.ModelSerializer): # надо переприумать для соответстия ТЗ
    # for del after tests
    pass
    # recipes = RecipeLightSerializer(many=True)
    # is_subscribed = serializers.SerializerMethodField()

    # class Meta:
    #     model = User
    #     fields = ['email', 'id', 'first_name', 'last_name', 'username',
    #               'recipes',
    #               'is_subscribed', # сейчас не заработает
    #               ]
    
    # def get_is_subscribed(self, author):
    #     user = self.context.get('request').user
        # TODO оптимизировать запрос
        # if 1 == 1:
        # if get_object_or_404(Subscription, author=author, user=user):
        # if Subscription.objects.filter(author=author,
        #                                user=user):
        #     return True
        # return False