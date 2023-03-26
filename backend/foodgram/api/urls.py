from django.urls import include, path, re_path
from rest_framework import routers

from .views import (CustomUserSerilizer,
                    FavoritedCreateDeleteViewSet,
                    # FavoritedViewSet,
                    IngredientsReadOnlyViewSet,
                    RecipeViewSet, UserViewSet, TagsReadOnlyViewSet,
                    SubscriptionListCreateDestroyViewSet
                    )

router1 = routers.SimpleRouter()
router1.register(r'ingredients', IngredientsReadOnlyViewSet)
router1.register(r'recipes', RecipeViewSet)
router1.register(r'tags', TagsReadOnlyViewSet)
urlpatterns = [
    path('users/', UserViewSet.as_view({'get': 'list'})),
    path('users/<int:author_id>/subscribe/',
         SubscriptionListCreateDestroyViewSet.as_view({'post': 'create',
                                                       'get': 'list',
                                                       'delete': 'destroy'})),
    path('recipes/<int:pk>/favorite/',
         FavoritedCreateDeleteViewSet.as_view({'post': 'create',
                                               'delete': 'destroy'})),
    path('', include(router1.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
