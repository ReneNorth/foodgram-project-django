from django.contrib import admin

from shopping_cart.models import InShoppingCart


@admin.register(InShoppingCart)
class Admin(admin.ModelAdmin):
    pass
