from rest_framework import viewsets

from accounts.models import Role
from .models import Project
from .serializers import ProjectSerializer
from tasks.serializers import TaskSerializer
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsAdmin, IsReadOnlyOrAdminOrTaskCreator
from rest_framework.decorators import action
from rest_framework.response import Response


class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing Project objects.

    This ViewSet provides CRUD operations on Project instances with role-based access control,
    dynamic queryset filtering based on the user's role, and additional project-specific actions.

    Permissions:
        - GET (list/retrieve):
            - Requires authentication (`IsAuthenticated`)
            - Requires one of the roles: `IsReadOnlyOrAdminOrTaskCreator`
        - POST, PUT, PATCH, DELETE:
            - Requires authentication (`IsAuthenticated`)
            - Requires `IsAdmin` role.

    Queryset Filtering:
        - If the requesting user has 'admin' role, return all projects.
        - Otherwise, return only projects where the user is assigned.

    Endpoints:
        - GET /projects/ : List projects.
        - POST /projects/ : Create a new project.
        - GET /projects/{id}/ : Retrieve a specific project.
        - PUT /projects/{id}/ : Update a project.
        - PATCH /projects/{id}/ : Partially update a project.
        - DELETE /projects/{id}/ : Delete a project.
        - GET /projects/{id}/tasks/ : Retrieve all tasks assigned to a specific project.

    Methods:
        - get_queryset(): Dynamically filters queryset based on user role.
        - get_permissions(): Dynamically assigns permissions based on request method.
        - perform_create(): Automatically assigns the current user as the project owner during creation.
        - tasks(): Custom action to fetch tasks for a given project.

    Example (Custom Action - Get tasks for a project):
        Request:
            GET /projects/5/tasks/
        Response:
            [
                {
                    "id": 101,
                    "name": "Task 1",
                    "description": "...",
                    ...
                },
                ...
            ]
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


    def get_queryset(self):
        """
        Role-based filtering logic for project listing.
        Admin users see all projects.
        Non-admin users see only projects where they are assigned.
        """
        if getattr(self, 'swagger_fake_view', False):
            return Project.objects.none() 
    
        request_user_role = self.request.user.roles.values_list("name", flat=True)
        if Role.ADMIN in request_user_role:  # admin has full access to all projects
            return super().get_queryset()
        
        # Non-admin users can only access projects assigned to them
        return self.request.user.projects.all()

    def get_permissions(self):
        """
        Dynamically assign permissions based on request type.
        """
        # Allow read-only access to Admin, TaskCreator, and ReadOnly users
        if self.request.method == "GET":
            return [IsAuthenticated(), IsReadOnlyOrAdminOrTaskCreator()]
        # Write operations restricted to Admin only
        return [IsAuthenticated(), IsAdmin()]
    
    def perform_create(self, serializer):
        # Auto-assign the current user as project owner on creation.
        serializer.save(owner=self.request.user)



    @action(detail=True, methods=['get'])
    def tasks(self, request, pk):
        """
        Custom action to list tasks under a specific project.
        URL: /projects/{id}/tasks/
        """
        # Fetch project by ID
        project = Project.objects.get(id=pk)
        # Fetch all tasks associated with this project
        tasks = project.task_set.all()
        tasks_serializer = TaskSerializer(tasks, many=True)
        return Response(tasks_serializer.data)
