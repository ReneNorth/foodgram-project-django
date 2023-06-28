from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import filters, status, viewsets
from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from recipe.models import Recipe
from subscription.models import Subscription

# from .models import User
from users.permissions import CreateListUsersPermission
from users.serializers import CustomUserSerializer
from api.serializers import RecipeRetreiveDelListSerializer, SubscriptionListSerializer

from api.pagination import CustomPagination
import logging

User = get_user_model()

logger = logging.getLogger(__name__)
log = logging.getLogger(__name__)


class CustomizedUserViewSet(UserViewSet):
    # permission_classes = [CreateListUsersPermission, IsAuthenticated]
    permission_classes = [AllowAny, IsAuthenticated, ]
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username', )
    # lookup_field = 'username'

    @action(detail=False,
            methods=['GET', ],
            permission_classes=[IsAuthenticated, ],
            url_path='me',)
    def get_me(self, request):
        user = get_object_or_404(User, pk=request.user.pk)
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False,
            url_path='subscriptions',
            serializer_class=SubscriptionListSerializer,
            permission_classes=[IsAuthenticated, ],
            pagination_class=CustomPagination)
    def get_subscriptions(self, request):
        """
        Returns queryset with the recipes of
        all authors the user is subscribed to.
        """
        log.info(type(self))
        log.info(self)

        # subscriptions = Subscription.objects.filter(user=request.user)
        subscriptions = User.objects.filter(subscribed__user=request.user)
        log.info(subscriptions)
        pagination = self.paginate_queryset(subscriptions)
        if pagination is None:
            log.warning('Pagination in subscriptions is disabled')
        # pagination = CustomPagination.paginate_queryset(self, queryset=recipes,
        #                                                 request=request)
        serializer = self.get_serializer(pagination, many=True)
        log.info(serializer.data)

        return self.get_paginated_response(serializer.data)

# failed attempt
    @action(detail=False,
            url_path='subscriptions-test',
            serializer_class=RecipeRetreiveDelListSerializer,
            permission_classes=[IsAuthenticated, ],
            pagination_class=CustomPagination)
    def get_subscriptions_test(self, request):
        """
        Returns queryset with the recipes of
        all authors the user is subscribed to.
        """
        log.info(type(self))
        log.info(self)
        recipes = Recipe.objects.filter(
            author__subscribed__user=request.user).order_by('-pub_date')
        log.info(recipes)
        pagination = self.paginate_queryset(recipes)
        if pagination is None:
            log.warning('Pagination in subscriptions is disabled')
        # pagination = CustomPagination.paginate_queryset(self, queryset=recipes,
        #                                                 request=request)
        serializer = self.get_serializer(pagination, many=True)
        log.info(serializer.data)

        return self.get_paginated_response(serializer.data)
