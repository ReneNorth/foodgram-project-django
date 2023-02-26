from rest_framework import serializers, validators
from recipe.models import Recipe, RecipeIngredient, FavoriteRecipe
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


class RecipeIngredientSerializer(serializers.ModelSerializer):
    # print(123)
    # print(dir(RecipeIngredient))
    # print(RecipeIngredient.objects.filter(id=3)[0].amount)
    
    class Meta:
        model = RecipeIngredient
        fields = ['id', 'ingredient', 'amount']
        # fields = '__all__'
        # extra_kwargs = {
        #     'amount': {'read_only': True},
        # }


class RecipeSerializer(serializers.ModelSerializer):
    """ """
    author = CustomUserSerilizer()
    is_favorited = serializers.SerializerMethodField()
    recipes = RecipeIngredientSerializer(read_only=True, many=True)

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
                  'text', 'cooking_time', 'is_favorited',
                #   'ingredients',
                  'recipes',
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