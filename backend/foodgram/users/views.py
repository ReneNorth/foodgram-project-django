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
from api.serializers import RecipeRetreiveDelListSerializer
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
            serializer_class=RecipeRetreiveDelListSerializer,
            permission_classes=[IsAuthenticated, ],
            pagination_class=CustomPagination)
    def get_subscriptions(self, request):
        log.info(dir(request))
        log.info(f'request.user: {request.user}')
        recipes = Recipe.objects.filter(
            author__subscribed__user=request.user).order_by('-pub_date')
        log.info(recipes)
        # serializer = RecipeRetreiveDelListSerializer(
        #     Recipe.objects.filter(author=request.user), many=True)
        return Response(self.get_serializer(recipes, many=True).data,
                        status=status.HTTP_200_OK)


# class CustomUserViewSet(UserViewSet):
#     pagination_class = LimitPageNumberPagination

    # @action(detail=True, permission_classes=[IsAuthenticated])
    # def subscribe(self, request, id=None):
    #     user = request.user
    #     author = get_object_or_404(User, id=id)

    #     if user == author:
    #         return Response({
    #             'errors': 'Вы не можете подписываться на самого себя'
    #         }, status=status.HTTP_400_BAD_REQUEST)
    #     if Follow.objects.filter(user=user, author=author).exists():
    #         return Response({
    #             'errors': 'Вы уже подписаны на данного пользователя'
    #         }, status=status.HTTP_400_BAD_REQUEST)

    #     follow = Follow.objects.create(user=user, author=author)
    #     serializer = FollowSerializer(
    #         follow, context={'request': request}
    #     )
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)

    # @subscribe.mapping.delete
    # def del_subscribe(self, request, id=None):
    #     user = request.user
    #     author = get_object_or_404(User, id=id)
    #     if user == author:
    #         return Response({
    #             'errors': 'Вы не можете отписываться от самого себя'
    #         }, status=status.HTTP_400_BAD_REQUEST)
    #     follow = Follow.objects.filter(user=user, author=author)
    #     if follow.exists():
    #         follow.delete()
    #         return Response(status=status.HTTP_204_NO_CONTENT)

    #     return Response({
    #         'errors': 'Вы уже отписались'
    #     }, status=status.HTTP_400_BAD_REQUEST)

    # @action(detail=False, permission_classes=[IsAuthenticated])
    # def subscriptions(self, request):
    #     user = request.user
    #     queryset = Follow.objects.filter(user=user)
    #     pages = self.paginate_queryset(queryset)
    #     serializer = FollowSerializer(
    #         pages,
    #         many=True,
    #         context={'request': request}
    #     )
    #     return self.get_paginated_response(serializer.data)
