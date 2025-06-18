from rest_framework import viewsets

from accounts.models import Role
from .models import Task
from .serializers import TaskSerializer
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsAdminOrTaskCreator, IsReadOnlyOrAdminOrTaskCreator
from django.db.models import Q

class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Task resources.

    Supports full CRUD operations with role-based access control and queryset filtering.

    Permissions:
        - Admin: Full access to all tasks.
        - Task Creator: Full access to tasks created by themselves.
        - Read-Only User: Can read tasks and partially update task status.
        - Read-Only + Task Creator: Can read and update owned or created tasks.
    
    Endpoints:
        - GET /tasks/ : List tasks (role-based filtering applied).
        - GET /tasks/{id}/ : Retrieve task details.
        - POST /tasks/ : Create new task (assigns creator automatically).
        - PATCH /tasks/{id}/ : Update task partially.
        - DELETE /tasks/{id}/ : Delete task.

    QuerySet Filtering Logic (get_queryset):
        - Admin:
            - Full access to all tasks.
        - Task Creator + Read-Only:
            - Access to tasks where user is creator or owner.
        - Read-Only:
            - Access to tasks where user is owner.
        - Task Creator:
            - Access to tasks where user is creator.
        - Default fallback:
            - Admin-level access (superuser or fallback safety).

    Permission Logic (get_permissions):
        - GET: Allowed for Admin, Task Creator, and Read-Only.
        - PATCH (status only): Allowed for Read-Only users if only updating "status" field.
        - POST / DELETE / PATCH (full): Allowed only for Admin or Task Creator.
    
    Methods:
        - perform_create: Automatically sets creator as the logged-in user during task creation.
        - partial_update: Uses default DRF partial update behavior.

    Example POST request (create task):
    {
        "description": "Write unit tests",
        "due_date": "2025-06-15",
        "status": "Pending",
        "project_id": 3,
        "owner_id": 5
    }

    Example PATCH request (read-only user updating status only):
    {
        "status": "Completed"
    }
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Task.objects.none() 
        
        request_user_role = self.request.user.roles.values_list("name", flat=True)
        # Full access to all tasks.
        if Role.ADMIN in request_user_role: 
            return super().get_queryset()
        
      
        # Task Creator and Read-Only Access to tasks where user is creator or owner.
        if Role.TASK_CREATOR in request_user_role and Role.READ_ONLY in request_user_role:
            return Task.objects.filter(Q(creator=self.request.user) | Q(owner=self.request.user))
        
        # READ_ONLY - Access to tasks where user is owner.
        if Role.READ_ONLY in request_user_role:
            return Task.objects.filter(owner=self.request.user)
        
        # Full access to tasks created by themselves.
        if Role.TASK_CREATOR in request_user_role:
            return Task.objects.filter(creator=self.request.user)
    
        return super().get_queryset()

    def get_permissions(self):
        # Read-Only User: Can read tasks and partially update task "status".
        if (self.request.method == "GET") or (self.request.method == "PATCH" and len(self.request.data) == 1 and 'status' in self.request.data):
            return [IsAuthenticated(), IsReadOnlyOrAdminOrTaskCreator()]
        return [IsAuthenticated(), IsAdminOrTaskCreator()]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
