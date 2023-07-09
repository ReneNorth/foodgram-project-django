from django.urls import include, path
from rest_framework import routers

from api.views import (FavoritedCreateDeleteViewSet,
                       IngredientsReadOnlyViewSet,
                       InShoppingCartCreateDeleteViewSet,
                       SubscriptionListCreateDestroyViewSet,
                       TagsReadOnlyViewSet, RecipeViewSet)
from users.views import CustomizedUserViewSet

router1 = routers.DefaultRouter()
router1.register('ingredients', IngredientsReadOnlyViewSet)
router1.register('recipes', RecipeViewSet)
router1.register('tags', TagsReadOnlyViewSet)
router1.register('users', CustomizedUserViewSet)

urlpatterns = [
    path('users/<int:author_id>/subscribe/',
         SubscriptionListCreateDestroyViewSet.as_view({'get': 'list',
                                                       'post': 'create',
                                                       'delete': 'destroy'})),
    path('recipes/<int:pk>/favorite/',
         FavoritedCreateDeleteViewSet.as_view({'post': 'create',
                                               'delete': 'destroy'})),
    path('recipes/<int:pk>/shopping_cart/',
         InShoppingCartCreateDeleteViewSet.as_view({'post': 'create',
                                                    'delete': 'destroy'})),
    path('', include(router1.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
