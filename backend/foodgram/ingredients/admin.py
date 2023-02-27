from django.contrib import admin

from .models import Ingredient


@admin.register(Ingredient)
class Admin(admin.ModelAdmin):
    pass