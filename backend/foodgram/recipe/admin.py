from django.contrib import admin

from .models import FavoriteRecipe, Recipe, RecipeIngredient, RecipeTag


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    readonly_fields = ('get_c',)
    list_display = ['name', 'author', 'get_c']
    list_filter = ['name', 'author', 'tags']

    def get_c(self, recipe) -> int:
        return FavoriteRecipe.objects.filter(favorited_recipe=recipe).count()


@admin.register(FavoriteRecipe)
class FavorireRecipeAdmin(admin.ModelAdmin):
    pass


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    pass


@admin.register(RecipeTag)
class RecipeTagAdmin(admin.ModelAdmin):
    pass
