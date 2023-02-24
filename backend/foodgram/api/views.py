from rest_framework import filters, status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
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
    
    # def get_serializer_class(self):
    #     if self.action == 'list':
    #         return serializers.ListaGruppi
    #     if self.action == 'retrieve':
    #         return serializers.DettaglioGruppi
    #     return serializers.Default
    

    # @action(detail=True, methods=['POST', 'DELETE', ], url_path='favorite')
    # def favorite_recipe(self, request, pk) -> Response:
    #     """Заполнить"""
        
    #     if request.method == 'POST':
    #         user = get_object_or_404(User, id=request.user.id)
    #         recipe = get_object_or_404(Recipe, pk=pk)
            
    #         serializer = FavoriteSerializer(data=request.data,
    #                                         context={'who_favorited': user,
    #                                                  'favorited_recipe': recipe})
    #         print(serializer)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data, status=status.HTTP_200_OK)
    #         print('not valid')
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerilizer


class IngredientsReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


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

    @action(methods=['post'], detail=False)
    def create(self, request, pk=None) -> Response:
        # """Метод добавляет рецепт в избранные. ID юзера и рецепта передаются
        # сериализатору через контекст"""
        user = get_object_or_404(User, id=request.user.id)
        recipe = get_object_or_404(Recipe, pk=pk)
        serializer = self.get_serializer(data=request.data,
                                         context={'who_favorited': user,
                                                  'favorited_recipe': recipe})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(methods=['delete'], detail=False)
    def destroy(self, request, pk=None):
        print(pk)
        favorited = FavoriteRecipe.objects.filter(who_favorited_id=request.user.id,
                                                  favorited_recipe_id=pk)
        print(favorited, 'favorited')
        if favorited:
        # favorited = get_object_or_404(FavoriteRecipe,
                                    #   who_favorited_id=request.user.id,
                                    #   favorited_recipe_id=pk)
            self.perform_destroy(favorited)
            return Response('object deleted', status=status.HTTP_204_NO_CONTENT)
        return Response('object not found', status=status.HTTP_404_NOT_FOUND)
                               
