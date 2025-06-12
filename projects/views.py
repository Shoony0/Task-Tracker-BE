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
        request_user_role = self.request.user.roles.values_list("name", flat=True)
        if Role.ADMIN in request_user_role: 
            return super().get_queryset()
        
        return self.request.user.projects.all()

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated(), IsReadOnlyOrAdminOrTaskCreator()]
        return [IsAuthenticated(), IsAdmin()]
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)



    @action(detail=True, methods=['get'])
    def tasks(self, request, pk):
        project = Project.objects.get(id=pk)
        tasks = project.task_set.all()
        tasks_serializer = TaskSerializer(tasks, many=True)
        return Response(tasks_serializer.data)
