from django.contrib.auth import get_user_model
import logging
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from api.pagination import CustomPagination

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
                          RecipeCreatePatchSerializer,
                          RecipeRetreiveDelListSerializer,
                          SubscriptionCreateDeleteSerializer,
                          SubscriptionListSerializer, TagSerializer)

User = get_user_model()

logging.basicConfig(format='%(message)s')
log = logging.getLogger(__name__)


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
    serializer_class = RecipeCreatePatchSerializer
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend, )
    filterset_class = RecipeFilter
    permission_classes = [IsAuthorOrReadOnly, ]

    def get_serializer_class(self) -> (RecipeRetreiveDelListSerializer |
                                       RecipeCreatePatchSerializer):
        """
        Returns the appropriate serializer class based on the action.

        Returns:
            Serializer: The serializer class for the current action.
        """
        if self.action in ('retrieve', 'list', 'destroy'):
            return RecipeRetreiveDelListSerializer
        return RecipeCreatePatchSerializer

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
                "user": request.user,
            },
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            log.info(f'serializier returned data: {serializer.data}')
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
        log.info(self)
        log.info('test message', request)
        instance = self.get_object()
        log.info(f'request data in recipe viewset {request.data}')
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            log.info(f'serializer data in recipe viewset {serializer.data}')
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        final_list = {}
        ingredients = RecipeIngredient.objects.filter(
            recipe__cart__user=request.user).values_list(
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
        # pdfmetrics.registerFont(
        #     TTFont('Slimamif', 'Slimamif.ttf', 'UTF-8'))
        # response = HttpResponse(content_type='application/pdf')
        # response['Content-Disposition'] = ('attachment; '
        #                                    'filename="shopping_list.pdf"')
        # page = canvas.Canvas(response)
        # page.setFont('Slimamif', size=24)
        # page.drawString(200, 800, 'Список ингредиентов')
        # page.setFont('Slimamif', size=16)
        # height = 750
        # for i, (name, data) in enumerate(final_list.items(), 1):
        #     page.drawString(75, height, (f'<{i}> {name} - {data["amount"]}, '
        #                                  f'{data["measurement_unit"]}'))
        #     height -= 25
        # page.showPage()
        # page.save()
        # return response
        return True


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
