from django.contrib.auth import get_user_model
import logging
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from api.pagination import CustomPagination
from django.http import HttpResponse

from ingredients.models import Ingredient
from recipe.models import FavoriteRecipe, Recipe, RecipeIngredient
from shopping_cart.models import InShoppingCart
from subscription.models import Subscription
from tags.models import Tag
from users.permissions import RecipePermission
from api.permissions import IsAuthorOrReadOnly

from .filters import RecipeFilter
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          InShoppingCartSerializer,
                          RecipeSerializer,
                          SubscriptionCreateDeleteSerializer,
                          SubscriptionListSerializer, TagSerializer)

User = get_user_model()

logging.basicConfig(format='%(message)s')
log = logging.getLogger(__name__)


def txt_to_repr(final_list: dict) -> str:
    txt_to_repr = ''
    for name, amount in final_list.items():
        unit = amount['measurement_unit']
        amount = amount['amount']
        txt_to_repr += f'{name} ({unit}) — {amount}\n'
    return txt_to_repr


class SubscriptionListCreateDestroyViewSet(
        mixins.DestroyModelMixin,
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, ]
    pagination_class = CustomPagination

    def get_queryset(self):
        return User.objects.filter(subscribed__user__id=self.request.user.id)

    def get_serializer_class(self) -> (SubscriptionListSerializer |
                                       SubscriptionCreateDeleteSerializer):
        if self.action == "list":
            return SubscriptionListSerializer
        return SubscriptionCreateDeleteSerializer

    def create(self, request, author_id=None) -> Response:
        user = get_object_or_404(User, id=request.user.id)
        author = get_object_or_404(User, id=author_id)
        serializer = self.get_sericalizer(
            data=request.data,
            context={"user": user, "author": author, "request": request},
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, author_id=None) -> Response:
        user = get_object_or_404(User, id=request.user.id)
        author = get_object_or_404(User, id=author_id)
        subscription = get_object_or_404(
            Subscription, user=user, author=author)
        self.perform_destroy(subscription)
        return Response(status=status.HTTP_204_NO_CONTENT)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all().order_by('-pub_date')
    serializer_class = RecipeSerializer
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend, )
    filterset_class = RecipeFilter
    permission_classes = [IsAuthorOrReadOnly, ]

    def get_serializer_context(self):
        return {'user': self.request.user}

    def create(self, request, *args, **kwargs):
        """
        Creates a new recipe based on the provided data.

        Args:
            request (Request): The HTTP request object.
            args: Variable length argument list.
            kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The response containing the serialized
            data of the created recipe.
        """
        serializer = self.get_serializer(
            data=request.data,
            context={
                'user': request.user,
            },
        )
        log.info('in viewset')
        log.info(request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        """
        Performs additional actions after creating a recipe.

        Args:
            serializer (Serializer): The serializer
            instance used to create the recipe.
        """
        serializer.save(author=self.request.user)

    def partial_update(self, request, *args, **kwargs) -> Response:
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request) -> HttpResponse:
        final_list = {}
        ingredients = RecipeIngredient.objects.filter(
            recipe__is_in_cart__user=request.user).values_list(
            'ingredient__name', 'ingredient__measurement_unit',
            'amount')
        for item in ingredients:
            name = item[0]
            if name not in final_list:
                final_list[name] = {
                    'measurement_unit': item[1],
                    'amount': item[2]
                }
            else:
                final_list[name]['amount'] += item[2]
        filename = "список_покупок.txt"
        response = HttpResponse(txt_to_repr(final_list),
                                content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response


class IngredientsReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None


class TagsReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class FavoritedCreateDeleteViewSet(
    mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    queryset = FavoriteRecipe.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = (RecipePermission,)

    # TODO Refactoring
    @action(methods=["post"], detail=False)
    def create(self, request, pk=None) -> Response:
        """
        The method adds a recipe to favorites. The user ID and recipe
        are passed to the serializer through the context.
        """
        user = get_object_or_404(User, id=request.user.id)
        recipe = get_object_or_404(Recipe, pk=pk)
        serializer = self.get_serializer(
            data=request.data,
            context={"who_favorited": user, "favorited_recipe": recipe},
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # TODO проверить не лишний ли декторатор
    @action(methods=["delete"], detail=False)
    def destroy(self, request, pk=None) -> Response:
        favorited = get_object_or_404(
            FavoriteRecipe,
            who_favorited_id=request.user.id,
            favorited_recipe_id=pk
        )
        self.perform_destroy(favorited)
        return Response("object deleted", status=status.HTTP_204_NO_CONTENT)


class InShoppingCartCreateDeleteViewSet(
    mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    queryset = InShoppingCart.objects.all()
    serializer_class = InShoppingCartSerializer
    permission_classes = (RecipePermission,)

    # TODO Refactoring
    @action(methods=["post"], detail=False)
    def create(self, request, pk=None) -> Response:
        """
        The method adds a recipe to favorites. The user ID and recipe
        are passed to the serializer through the context.
        """
        user = get_object_or_404(User, id=request.user.id)
        recipe = get_object_or_404(Recipe, pk=pk)
        serializer = self.get_serializer(
            data=request.data, context={"user": user, "recipe_in_cart": recipe}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["delete"], detail=False)
    def destroy(self, request, pk=None) -> Response:
        recipe_in_cart = get_object_or_404(
            InShoppingCart, user=request.user.id, recipe_in_cart_id=pk
        )
        self.perform_destroy(recipe_in_cart)
        return Response("object deleted", status=status.HTTP_204_NO_CONTENT)
