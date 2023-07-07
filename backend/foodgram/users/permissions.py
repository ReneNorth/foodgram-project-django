from rest_framework.permissions import SAFE_METHODS, BasePermission


class RecipePermission(BasePermission):
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if (
                request.method in ['DELETE', 'PATCH', ]
                and request.user.is_user
                and request.user != obj.author
        ):
            return False
        return True
