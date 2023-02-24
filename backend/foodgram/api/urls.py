from django.urls import path, include, re_path
from rest_framework import routers
from .views import (RecipeViewSet,
                    UserViewSet,
                    CustomUserSerilizer,
                    IngredientsReadOnlyViewSet,
                    FavoritedViewSet,
                    FavoritedCreateDeleteViewSet,
                    )


router1 = routers.SimpleRouter()
router1.register(r'ingredients', IngredientsReadOnlyViewSet)
# router1.register(r'recipes', RecipeViewSet)

urlpatterns = [
    path('users/', UserViewSet.as_view({'GET': 'list'})),
    path('recipes/<int:pk>/favorite/',
         FavoritedCreateDeleteViewSet.as_view({'post': 'create',
                                               'delete': 'destroy'})),
    path('', include(router1.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
