from django.contrib import admin

from subscription.models import Subscription


@admin.register(Subscription)
class Admin(admin.ModelAdmin):
    pass
