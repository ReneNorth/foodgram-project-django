from django.urls import path, include
from rest_framework import routers


router1 = routers.SimpleRouter()


urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]