from django.contrib import admin

from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class Admin(admin.ModelAdmin):
    list_display = ['email', 'username', ]
    search_fields = ['email', 'username', ]
    list_filter = ['email', 'username', ]
