from rest_framework import serializers, validators
from recipe.models import Recipe, RecipeIngredient, FavoriteRecipe, RecipeTag
from tags.models import Tag
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
                  'last_name']


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit']


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class RecipeIngredient(serializers.ModelSerializer):
    # всё таки сделать также как тэги? в чём отличите? почему 
    # такой подход не сработал сначала?
    name = serializers.SerializerMethodField()
    measurement_unit = serializers.SerializerMethodField()
    class Meta:
        model = RecipeIngredient
        fields = [
                  'ingredient',
                  'name',
                  'measurement_unit',
                  'amount',
                  ]
    def get_name(self, obj):
        return Ingredient.objects.get(id=obj.ingredient.id).name
    
    def get_measurement_unit(self, obj):
        return Ingredient.objects.get(id=obj.ingredient.id).measurement_unit
        


class RecipeSerializer(serializers.ModelSerializer):
    """ """
    author = CustomUserSerilizer()
    is_favorited = serializers.SerializerMethodField()
    ingredients = RecipeIngredient(read_only=True, many=True)
    tags = TagSerializer(many=True)
    # ingredients_in_recipe2 = serializers.SerializerMethodField()

    def get_is_favorited(self, recipe):
        user = self.context.get("request").user
        # TODO оптимизировать запрос
        if FavoriteRecipe.objects.filter(who_favorited=user,
                                         favorited_recipe=recipe):
            return True
        return False
    
    # def get_ingredients_in_recipe2(self, obj):
    #     return Recipe.ingredients.all()
         

    class Meta:
        model = Recipe
        fields = ['id', 'author', 'name', 'image',
                  'text', 'cooking_time', 'is_favorited',
                  'ingredients',
                  'tags',
                #   'ingredients_in_recipe2',
                #   'recipes',
                  ]

        extra_kwargs = {
            'is_favorited': {'read_only': True},
            # 'ingredients': {'read_only': True},
        }


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