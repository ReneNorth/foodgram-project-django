from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import User
from .permissions import CreateListUsersPermission
from .serializers import CustomUserSerializer


class UserViewSet(viewsets.ModelViewSet):
    # permission_classes = [CreateListUsersPermission, IsAuthenticated]
    permission_classes = [AllowAny, ]
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
        return Response(CustomUserSerializer(
            user,
            context={'request': request}).data, status=status.HTTP_200_OK)

