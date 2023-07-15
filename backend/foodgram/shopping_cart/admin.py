from django.contrib import admin
from shopping_cart.models import InShoppingCart


@admin.register(InShoppingCart)
class InShoppingCartAdmin(admin.ModelAdmin):
    pass
