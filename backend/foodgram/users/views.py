import logging

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import filters, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.pagination import CustomPagination
from api.serializers import SubscriptionListSerializer
from users.serializers import CustomUserSerializer

User = get_user_model()

logger = logging.getLogger(__name__)
log = logging.getLogger(__name__)


class CustomizedUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username', )

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
        subscriptions = User.objects.filter(subscribed__user=request.user)
        log.info(subscriptions)
        pagination = self.paginate_queryset(subscriptions)
        if pagination is None:
            log.warning('Pagination in subscriptions is disabled')

        serializer = self.get_serializer(pagination, many=True)

        return self.get_paginated_response(serializer.data)
