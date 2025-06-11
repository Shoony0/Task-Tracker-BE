from rest_framework import viewsets

from accounts.permissions import IsAdmin, IsReadOnlyOrAdminOrTaskCreator
from .models import User, Role
from .serializers import UserSerializer, RoleSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated(), IsReadOnlyOrAdminOrTaskCreator()]
        return [IsAuthenticated(), IsAdmin()]

    @action(detail=False, methods=['GET'])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated(), IsReadOnlyOrAdminOrTaskCreator()]
        return [IsAuthenticated(), IsAdmin()]
