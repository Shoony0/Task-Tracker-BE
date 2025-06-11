from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.roles.filter(name='admin').exists()

class IsTaskCreator(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.roles.filter(name='task_creator').exists()

class IsReadOnlyUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.roles.filter(name='read_only').exists()


class IsReadOnlyOrAdminOrTaskCreator(BasePermission):
    def has_permission(self, request, view):
        return (
            IsReadOnlyUser().has_permission(request, view) or
            IsAdmin().has_permission(request, view) or
            IsTaskCreator().has_permission(request, view)
        )


class IsAdminOrTaskCreator(BasePermission):
    def has_permission(self, request, view):
        return (
            IsAdmin().has_permission(request, view) or
            IsTaskCreator().has_permission(request, view)
        )

