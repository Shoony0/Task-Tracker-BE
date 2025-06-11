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
