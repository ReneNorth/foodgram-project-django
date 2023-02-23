from django.urls import path, include, re_path
from rest_framework import routers
from .views import (RecipeViewSet,
                    UserViewSet,
                    CustomUserSerilizer,
                    IngredientsReadOnlyViewSet,
                    FavoritedViewSet
                    )


router1 = routers.SimpleRouter()
router1.register(r'recipes', RecipeViewSet)
router1.register(r'ingredients', IngredientsReadOnlyViewSet)
router1.register(r'favorited', FavoritedViewSet)
# router1.register(r'test_users', TestUserSerilizer, basename='test_users')


urlpatterns = [
    path('users/', UserViewSet.as_view({'get': 'list'})),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router1.urls))
]
