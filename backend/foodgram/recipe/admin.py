from django.contrib import admin
from .models import Recipe, FavoriteRecipe, RecipeIngredient, RecipeTag


@admin.register(Recipe, FavoriteRecipe, RecipeIngredient, RecipeTag)
class Admin(admin.ModelAdmin):
    pass
