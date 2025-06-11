from rest_framework import serializers
from .models import Task
from projects.serializers import ProjectSerializer
from accounts.serializers import UserSerializer
from accounts.models import User
from projects.models import Project

class TaskSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)
    project_id = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(), write_only=True, source='project'
    )

    owner = UserSerializer(read_only=True)
    owner_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, source='owner', allow_null=True, required=False
    )

    creator = UserSerializer(read_only=True)
    creator_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, source='creator', allow_null=True, required=False
    )

    class Meta:
        model = Task
        fields = ['id', 'description', 'due_date', 'status', 'project', 'project_id', 'owner', 'owner_id', 'creator', 'creator_id']
