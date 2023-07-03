from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.is_user)


class CreateListUsersPermission(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.is_admin
                or request.user.is_superuser
                or request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        return (request.user.is_admin
                or request.user.is_superuser
                or request.user.is_staff)


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_superuser


class RecipeTestPermission(BasePermission):
    """Доступ на чтение всем.
    Доступ к изменению объекта только админу или администратору."""

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or (request.user.is_authenticated
                    and request.user.role == 'admin')
                )

    def has_object_permission(self, request, view, obj):
        return (request.method == 'GET'
                or request.user.is_authenticated
                and (request.user.is_superuser
                     or request.user.role == 'admin')
                )


class RecipePermission(BasePermission):
    """Доступ на чтение всем.
    Доступ к созданию всем кроме не аутентифицированных пользователей.
    Доступ к удалению и редактированию админам, модераторам,
    суперпользователям и авторам контента."""

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
