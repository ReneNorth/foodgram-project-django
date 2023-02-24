from django.contrib import admin
from .models import Recipe, FavoriteRecipe, RecipeIngredient


@admin.register(Recipe, FavoriteRecipe, RecipeIngredient)
class Admin(admin.ModelAdmin):
    pass