from django.urls import path, include
from rest_framework import routers
from .views import RecipeViewSet


router1 = routers.SimpleRouter()
router1.register(r'recipes', RecipeViewSet)


urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router1.urls))
]
