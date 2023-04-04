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
from shopping_cart.models import InShoppingCart
from users.permissions import (RecipePermission, )
from rest_framework.pagination import LimitOffsetPagination

from .serializers import (IngredientSerializer,
                          FavoriteSerializer, RecipeRetreiveDelListSerializer,
                          RecipeCreatePatchSerializer, TagSerializer,
                          SubscriptionListSerializer,
                          SubscriptionCreateDeleteSerializer,
                          InShoppingCartSerializer,
                          )

User = get_user_model()


class SubscriptionListCreateDestroyViewSet(mixins.DestroyModelMixin,
                                           mixins.ListModelMixin,
                                           mixins.CreateModelMixin,
                                           viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return User.objects.filter(subscribed__user__id=self.request.user.id)

    def get_serializer_class(self):
        if self.action == 'list':
            return SubscriptionListSerializer
        return SubscriptionCreateDeleteSerializer

    def create(self, request, author_id=None) -> Response:
        """"""
        user = get_object_or_404(User, id=request.user.id)
        author = get_object_or_404(User, id=author_id)
        serializer = self.get_serializer(data=request.data,
                                         context={'user': user,
                                                  'author': author,
                                                  'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, author_id=None) -> Response:
        user = get_object_or_404(User, id=request.user.id)
        author = get_object_or_404(User, id=author_id)
        subscription = get_object_or_404(Subscription,
                                         user=user,
                                         author=author)
        self.perform_destroy(subscription)
        return Response(status=status.HTTP_204_NO_CONTENT)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeRetreiveDelListSerializer
    pagination_class = LimitOffsetPagination
    # permission_classes = [RecipePermission, ]
    permission_classes = [AllowAny, ]
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


    # def destroy(self, request, author_id=None) -> Response:
    #     user = get_object_or_404(User, id=request.user.id)
    #     author = get_object_or_404(User, id=author_id)
    #     subscription = get_object_or_404(Subscription,
    #                                      user=user,
    #                                      author=author)
    #     self.perform_destroy(subscription)
    #     return Response('object deleted', status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IngredientsReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None


class TagsReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


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


class InShoppingCartCreateDeleteViewSet(mixins.CreateModelMixin,
                                        mixins.DestroyModelMixin,
                                        viewsets.GenericViewSet):
    queryset = InShoppingCart.objects.all()
    serializer_class = InShoppingCartSerializer
    permission_classes = (RecipePermission, )
    
    # TODO Refactoring
    @action(methods=['post'], detail=False)
    def create(self, request, pk=None) -> Response:
        """Метод добавляет рецепт в избранные. ID юзера и рецепта передаются
        сериализатору через контекст"""
        user = get_object_or_404(User, id=request.user.id)
        recipe = get_object_or_404(Recipe, pk=pk)
        serializer = self.get_serializer(data=request.data,
                                         context={'user': user,
                                                  'recipe_in_cart': recipe})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # TODO проверить не лишний ли декторатор
    @action(methods=['delete'], detail=False)
    def destroy(self, request, pk=None) -> Response:
        recipe_in_cart = get_object_or_404(InShoppingCart,
                                      user=request.user.id,
                                      recipe_in_cart_id=pk)
        self.perform_destroy(recipe_in_cart)
        return Response('object deleted', status=status.HTTP_204_NO_CONTENT)