from django.shortcuts import render
from rest_framework import viewsets
from .serializers import (RecipeSerializer,
                          CustomUserSerilizer,
                          )
from recipe.models import Recipe
from django.contrib.auth import get_user_model

User = get_user_model()


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerilizer
    
class CustomUserViewSet():
    pass
    
    

