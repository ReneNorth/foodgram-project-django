from django.contrib import admin

from .models import FavoriteRecipe, Recipe, RecipeIngredient, RecipeTag


@admin.register(Recipe, FavoriteRecipe, RecipeIngredient, RecipeTag)
class Admin(admin.ModelAdmin):
    pass
