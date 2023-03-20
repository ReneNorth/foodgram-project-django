from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import mixins, status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
# from django_filters.rest_framework import DjangoFilterBackend
from ingredients.models import Ingredient
from recipe.models import FavoriteRecipe, Recipe, RecipeIngredient
from tags.models import Tag
from subscription.models import Subscription
from users.permissions import (RecipePermission, )

from .serializers import (CustomUserSerilizer, IngredientSerializer,
                          FavoriteSerializer, RecipeRetreiveDelListSerializer,
                          RecipeCreatePatchSerializer, TagSerializer,
                          SubscriptionRecipeSerializer,
                          )

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerilizer


class SubscriptionRecipeListViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionRecipeSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        print(User.objects.filter(author__)
        # print(Subscription.objects.prefetch_related('author__post'))
        # print(Subscription.objects.filter(
        #     user__id=self.request.user.id))
        
        return Subscription.objects.filter(
            user__id=self.request.user.id).values
        
        # return Subscription.objects.filter(
            # user__id=self.request.user.id).prefetch_related('author')


class SubscriptionCreateDestroyViewSet(viewsets.ModelViewSet):
    """Under dev."""
    pass
    # serializer_class = SubscriptionRecipeSerializer
    # permission_classes = [IsAuthenticated, ]

    # def get_queryset(self):
    #     return Subscription.objects.filter(
    #         user__id=self.kwargs['user_id'])


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeRetreiveDelListSerializer
    permission_classes = [RecipePermission, ]
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['tags', ]

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list', 'delete'):
            return RecipeRetreiveDelListSerializer
        return RecipeCreatePatchSerializer

    def create(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=request.user.id)
        serializer = self.get_serializer(data=request.data,
                                         context={'user': user, })
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
    permission_classes = (RecipePermission, )
    
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

    # TODO проверить не лишний ли декторатор
    @action(methods=['delete'], detail=False)
    def destroy(self, request, pk=None) -> Response:
        favorited = get_object_or_404(FavoriteRecipe,
                                      who_favorited_id=request.user.id,
                                      favorited_recipe_id=pk)
        self.perform_destroy(favorited)
        return Response('object deleted', status=status.HTTP_204_NO_CONTENT)
