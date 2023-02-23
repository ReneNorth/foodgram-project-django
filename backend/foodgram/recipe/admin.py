from django.contrib import admin
from .models import Recipe, FavoriteRecipe


@admin.register(Recipe, FavoriteRecipe)
class Admin(admin.ModelAdmin):
    pass