from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    """
    Allows access only to users with the 'admin' role.

    Returns:
        True if the user is authenticated and has 'admin' role assigned.
        False otherwise.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.roles.filter(name='admin').exists()

class IsTaskCreator(BasePermission):
    """
    Allows access only to users with the 'task_creator' role.

    Returns:
        True if the user is authenticated and has 'task_creator' role assigned.
        False otherwise.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.roles.filter(name='task_creator').exists()

class IsReadOnlyUser(BasePermission):
    """
    Allows access only to users with the 'read_only' role.

    Returns:
        True if the user is authenticated and has 'read_only' role assigned.
        False otherwise.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.roles.filter(name='read_only').exists()


class IsReadOnlyOrAdminOrTaskCreator(BasePermission):
    """
    Allows access if user has any of the following roles:
    - 'read_only'
    - 'admin'
    - 'task_creator'

    Useful for views where multiple roles are allowed.

    Returns:
        True if user has at least one of the above roles.
        False otherwise.
    """
    def has_permission(self, request, view):
        return (
            IsReadOnlyUser().has_permission(request, view) or
            IsAdmin().has_permission(request, view) or
            IsTaskCreator().has_permission(request, view)
        )


class IsAdminOrTaskCreator(BasePermission):
    """
    Allows access if user has either 'admin' or 'task_creator' role.

    Useful for views where write operations are allowed only for creators and admins.

    Returns:
        True if user has either role.
        False otherwise.
    """
    def has_permission(self, request, view):
        return (
            IsAdmin().has_permission(request, view) or
            IsTaskCreator().has_permission(request, view)
        )

