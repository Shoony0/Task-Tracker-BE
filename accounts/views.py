from rest_framework import viewsets

from accounts.permissions import IsAdmin, IsReadOnlyOrAdminOrTaskCreator
from .models import User, Role
from .serializers import UserSerializer, RoleSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema

@swagger_auto_schema(tags=["Tasks"])
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing User objects.

    This ViewSet provides CRUD operations on User instances with permission-based access control.
    
    Permissions:
        - GET (list/retrieve): Requires authentication and one of the roles:
            - ReadOnly
            - Admin
            - TaskCreator
        - POST, PUT, PATCH, DELETE: Requires authentication and Admin role.

    Endpoints:
        - GET /users/ : List all users.
        - POST /users/ : Create a new user.
        - GET /users/{id}/ : Retrieve a specific user.
        - PUT /users/{id}/ : Update an existing user.
        - PATCH /users/{id}/ : Partially update an existing user.
        - DELETE /users/{id}/ : Delete a user.
        - GET /users/me/ : Retrieve the profile of the current authenticated user.

    Custom Actions:
        - me (GET /users/me/): 
            Returns the details of the authenticated user making the request.

    Methods:
        - get_permissions: Dynamically assigns permissions based on request method.

    """
    
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Returns the list of permissions that this view requires.
        
        - GET requests require IsAuthenticated and IsReadOnlyOrAdminOrTaskCreator.
        - Other requests require IsAuthenticated and IsAdmin.
        """
        if self.request.method == 'GET':
            return [IsAuthenticated(), IsReadOnlyOrAdminOrTaskCreator()]
        return [IsAuthenticated(), IsAdmin()]

    @action(detail=False, methods=['GET'])
    def me(self, request):
        """
        Returns the currently authenticated user's details.
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class RoleViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing Role objects.

    This ViewSet provides CRUD operations on Role instances with permission-based access control.

    Permissions:
        - GET (list/retrieve): Requires authentication and one of the roles:
            - ReadOnly
            - Admin
            - TaskCreator
        - POST, PUT, PATCH, DELETE: Requires authentication and Admin role.

    Endpoints:
        - GET /roles/ : List all roles.
        - POST /roles/ : Create a new role.
        - GET /roles/{id}/ : Retrieve a specific role.
        - PUT /roles/{id}/ : Update an existing role.
        - PATCH /roles/{id}/ : Partially update an existing role.
        - DELETE /roles/{id}/ : Delete a role.

    Methods:
        - get_permissions: Dynamically assigns permissions based on request method.
    """
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

    def get_permissions(self):
        """
        Returns the list of permissions that this view requires.
        
        - GET requests require IsAuthenticated and IsReadOnlyOrAdminOrTaskCreator.
        - Other requests require IsAuthenticated and IsAdmin.
        """
        if self.request.method == 'GET':
            return [IsAuthenticated(), IsReadOnlyOrAdminOrTaskCreator()]
        return [IsAuthenticated(), IsAdmin()]
