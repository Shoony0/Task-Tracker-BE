from rest_framework import viewsets

from accounts.models import Role
from .models import Task
from .serializers import TaskSerializer
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsAdminOrTaskCreator, IsReadOnlyOrAdminOrTaskCreator
from django.db.models import Q

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


    def get_queryset(self):
        request_user_role = self.request.user.roles.values_list("name", flat=True)
        if Role.ADMIN in request_user_role: 
            return super().get_queryset()
        
        if Role.TASK_CREATOR in request_user_role and Role.READ_ONLY in request_user_role:
            return Task.objects.filter(Q(creator=self.request.user) | Q(owner=self.request.user))
        
        if Role.READ_ONLY in request_user_role:
            return Task.objects.filter(owner=self.request.user)
        
        if Role.TASK_CREATOR in request_user_role:
            return Task.objects.filter(creator=self.request.user)
    
        return super().get_queryset()

    def get_permissions(self):
        # second condition, read_ony user can only update the task status
        if (self.request.method == "GET") or (self.request.method == "PATCH" and len(self.request.data) == 1 and 'status' in self.request.data):
            return [IsAuthenticated(), IsReadOnlyOrAdminOrTaskCreator()]
        return [IsAuthenticated(), IsAdminOrTaskCreator()]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
