from django.urls import include, path
from rest_framework import routers

from .views import (
                    FavoritedCreateDeleteViewSet,
                    IngredientsReadOnlyViewSet,
                    RecipeViewSet, TagsReadOnlyViewSet,
                    SubscriptionListCreateDestroyViewSet,
                    InShoppingCartCreateDeleteViewSet
                    
                    )


router1 = routers.SimpleRouter()
router1.register(r'ingredients', IngredientsReadOnlyViewSet)
router1.register(r'recipes', RecipeViewSet)
router1.register(r'tags', TagsReadOnlyViewSet)
router1.register('users/subscriptions',
                 SubscriptionListCreateDestroyViewSet,
                 'subscriptions')
urlpatterns = [
    path('users/<int:author_id>/subscribe/',
         SubscriptionListCreateDestroyViewSet.as_view({'post': 'create',
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
