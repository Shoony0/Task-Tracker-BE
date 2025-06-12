from rest_framework import serializers
from .models import Task
from projects.serializers import ProjectSerializer
from accounts.serializers import UserSerializer
from accounts.models import User
from projects.models import Project

class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Task model.

    Handles serialization and deserialization of Task instances, including:
    - Linking task to a project.
    - Assigning owner and creator to the task.
    - Handling both read and write operations with nested serializers and ID-based relations.

    Fields:
        - id (read-only): Task ID.
        - description: Task description.
        - due_date: Due date of the task.
        - status: Current task status (e.g., Pending, Completed).
        - project (read-only): Nested Project object.
        - project_id (write-only): Assign project by Project ID.
        - owner (read-only): Nested User object representing task owner.
        - owner_id (write-only, optional): Assign owner by User ID.
        - creator (read-only): Nested User object representing task creator.
        - creator_id (write-only, optional): Assign creator by User ID.

    Example request (create/update):
    {
        "description": "Complete unit tests",
        "due_date": "2025-06-15",
        "status": "Pending",
        "project_id": 2,
        "owner_id": 5,
        "creator_id": 3
    }

    Example response:
    {
        "id": 101,
        "description": "Complete unit tests",
        "due_date": "2025-06-15",
        "status": "Pending",
        "project": {
            "id": 2,
            "name": "Backend Refactor",
            ...
        },
        "owner": {
            "id": 5,
            "username": "john.doe",
            ...
        },
        "creator": {
            "id": 3,
            "username": "jane.smith",
            ...
        }
    }
    """
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
