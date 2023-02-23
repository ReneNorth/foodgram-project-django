from rest_framework import viewsets
from .serializers import (RecipeSerializer,
                          CustomUserSerilizer,
                          IngredientSerializer,
                          FavoriteSerializer,
                          )
from recipe.models import Recipe, FavoriteRecipe
from ingredients.models import Ingredient
from django.contrib.auth import get_user_model

User = get_user_model()


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerilizer


class IngredientsReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class FavoritedViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FavoriteRecipe.objects.all()
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        return FavoriteRecipe.objects.filter(
            who_favorited=self.request.user
        )
