from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ingredients.models import Ingredient
from recipe.models import FavoriteRecipe, Recipe
from tags.models import Tag

from .serializers import (CustomUserSerilizer, IngredientSerializer,
                          FavoriteSerializer, RecipeRetreiveDelListSerializer,
                          RecipeCreatePatchSerializer, TagSerializer,
                          )

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerilizer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeRetreiveDelListSerializer

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list', 'delete'):
            return RecipeRetreiveDelListSerializer
        return RecipeCreatePatchSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class IngredientsReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class TagsReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class FavoritedViewSet(viewsets.ReadOnlyModelViewSet):
    """Test viewset"""
    queryset = FavoriteRecipe.objects.all()
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        return FavoriteRecipe.objects.filter(
            who_favorited=self.request.user
        )


class FavoritedCreateDeleteViewSet(mixins.CreateModelMixin,
                                   mixins.DestroyModelMixin,
                                   viewsets.GenericViewSet):
    queryset = FavoriteRecipe.objects.all()
    serializer_class = FavoriteSerializer
    # TODO Refactoring 
    @action(methods=['post'], detail=False)
    def create(self, request, pk=None) -> Response:
        """Метод добавляет рецепт в избранные. ID юзера и рецепта передаются
        сериализатору через контекст"""
        user = get_object_or_404(User, id=request.user.id)
        recipe = get_object_or_404(Recipe, pk=pk)
        serializer = self.get_serializer(data=request.data,
                                         context={'who_favorited': user,
                                                  'favorited_recipe': recipe})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # проверить не лишний ли декторатор
    @action(methods=['delete'], detail=False)
    def destroy(self, request, pk=None):
        favorited = get_object_or_404(FavoriteRecipe,
                                      who_favorited_id=request.user.id,
                                      favorited_recipe_id=pk)
        self.perform_destroy(favorited)
        return Response('object deleted', status=status.HTTP_204_NO_CONTENT)

