import base64
import logging

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from ingredients.models import Ingredient
from recipe.models import FavoriteRecipe, Recipe, RecipeIngredient
from rest_framework import serializers
from rest_framework.validators import ValidationError
from shopping_cart.models import InShoppingCart
from subscription.models import Subscription
from tags.models import Tag
from users.serializers import CustomUserSerializer

User = get_user_model()
log = logging.getLogger(__name__)


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit']


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug']


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredient
        fields = ['id', 'name', 'amount',
                  'measurement_unit', ]


class RecipeSerializer(serializers.ModelSerializer):
    is_in_shopping_cart = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()

    author = CustomUserSerializer(read_only=True)
    tags = TagSerializer(many=True,
                         read_only=True)
    ingredients = RecipeIngredientSerializer(many=True, read_only=True,
                                             source='recipeingredient_set')
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ['id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time', ]
        read_only_fields = ['id', 'author', ]

    def get_is_favorited(self, recipe) -> bool:
        user = self.context.get('user')
        return (
            user
            and FavoriteRecipe.objects.filter(
                who_favorited__id=user.id, favorited_recipe=recipe).exists()
        )

    def get_is_in_shopping_cart(self, recipe) -> bool:
        user = self.context.get('user')
        return (
            not user.is_anonymous
            and InShoppingCart.objects.filter(
                user=user, recipe_in_cart=recipe).exists()
        )

    def get_author(self, obj):
        if 'user' in self.context:
            return self.context['user']
        return None

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = self.initial_data.get('tags')
        user = self.context['user']
        if user.is_authenticated:
            instance = Recipe.objects.create(author=user, **validated_data)
            instance.tags.set(tags)
            instance.save()
            batch = []
            for ingredient in ingredients:
                batch.append(RecipeIngredient(
                    ingredient_id=ingredient['id'],
                    recipe_id=instance.id,
                    amount=ingredient['amount']))
            RecipeIngredient.objects.bulk_create(batch)
            return instance

    def update(self, instance, validated_data):
        instance.tags.clear()
        tags = self.initial_data.get('tags')
        instance.tags.set(tags)
        RecipeIngredient.objects.filter(recipe=instance).all().delete()
        ingredients = validated_data.get('ingredients')
        batch = []
        for ingredient in ingredients:
            batch.append(RecipeIngredient(
                ingredient_id=ingredient['id'],
                recipe_id=instance.id,
                amount=ingredient['amount']))
        RecipeIngredient.objects.bulk_create(batch)
        validated_data.pop('ingredients')
        super().update(instance, validated_data)
        return instance

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        if not ingredients:
            raise serializers.ValidationError(
                {'ingredients': 'you need at least one ingredient'
                                'for the recipe'})
        ingredient_list = set()
        for ingredient_item in ingredients:
            ingredient = get_object_or_404(Ingredient,
                                           id=ingredient_item['id'])
            if ingredient in ingredient_list:
                raise serializers.ValidationError(
                    'Ingredients should be unique')
            ingredient_list.add(ingredient)
            if int(ingredient_item['amount']) < 0:
                raise serializers.ValidationError({
                    'ingredients': ('Make sure that the value of the '
                                    'ingredient quantity is greater than 0')
                })
        data['ingredients'] = ingredients
        return data


class RecipeLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            'id', 'name', 'image',
            'cooking_time'
        ]


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
            raise serializers.ValidationError('You cannot add the recipe'
                                              'to favorites twice')
        favorite_recipe = FavoriteRecipe.objects.create(
            who_favorited_id=user_id,
            favorited_recipe_id=recipe_id)
        favorite_recipe.save()
        return favorite_recipe


class InShoppingCartSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    recipe_in_cart = serializers.SerializerMethodField()

    class Meta:
        model = FavoriteRecipe
        fields = ['user', 'recipe_in_cart']

    def create(self, validated_data):
        user_id = self.context["user"].id
        recipe_id = self.context["recipe_in_cart"].id
        if InShoppingCart.objects.filter(user=user_id,
                                         recipe_in_cart_id=recipe_id):
            raise serializers.ValidationError('You cannot add the recipe to '
                                              'the cart twice')
        recipe_in_cart = InShoppingCart.objects.create(
            user_id=user_id,
            recipe_in_cart_id=recipe_id)
        recipe_in_cart.save()
        return recipe_in_cart

    def get_user(self, obj):
        if 'user' in self.context:
            return self.context['user'].id
        return None

    def get_recipe_in_cart(self, obj):
        if 'recipe_in_cart' in self.context:
            return self.context['recipe_in_cart'].id
        return None


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
                raise ValidationError(
                    'You cannot subscribe to yourself!')
            if Subscription.objects.filter(user__id=user,
                                           author__id=author).exists():
                raise ValidationError(
                    'You cannot subscribe twice to the same user')
        return data


class SubscriptionListSerializer(serializers.ModelSerializer):
    """Lists authors the user is subscribed to and their recipes."""
    recipes = RecipeLightSerializer(many=True)
    is_subscribed = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count']

    def get_is_subscribed(self, author) -> bool:
        user = self.context.get('user')
        return (
            user
            and Subscription.objects.filter(author=author,
                                            user=user).exists()
        )

    def get_recipes_count(self, author) -> int:
        return Recipe.objects.filter(author=author).count()

    def get_is_favorited(self, recipe) -> bool:
        user = self.context.get('user')
        return (
            user
            and FavoriteRecipe.objects.filter(
                who_favorited__id=user.id, favorited_recipe=recipe).exists()
        )
