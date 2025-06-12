from rest_framework import serializers
from .models import Project
from accounts.serializers import UserSerializer
from accounts.models import User

class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializer for the Project model.

    Handles serialization and deserialization of Project instances, including:
    - Assigning multiple users to a project (users/user_ids).
    - Assigning an owner to a project (owner/owner_id).
    - Returning associated tasks via task_set.

    Fields:
        - id (read-only): Project ID.
        - name: Name of the project.
        - description: Project description.
        - start_date: Project start date.
        - end_date: Project end date.
        - owner (read-only): Project owner as nested User object.
        - owner_id (write-only): Assigns owner by User ID.
        - users (read-only): List of assigned users as nested User objects.
        - user_ids (write-only): Assigns users by list of User IDs.
        - task_set (read-only): List of Task IDs associated with this project.

    Example request (create/update):
    {
        "name": "New Project",
        "description": "This is a test project",
        "start_date": "2024-06-10",
        "end_date": "2024-09-10",
        "owner_id": 1,
        "user_ids": [2, 3, 4]
    }

    Example response:
    {
        "id": 10,
        "name": "New Project",
        "description": "This is a test project",
        "start_date": "2024-06-10",
        "end_date": "2024-09-10",
        "owner": {
            "id": 1,
            "username": "john.doe",
            "email": "john@example.com",
            ...
        },
        "users": [
            {
                "id": 2,
                "username": "jane.doe",
                "email": "jane@example.com"
            },
            {
                "id": 3,
                "username": "bob.smith",
                "email": "bob@example.com"
            }
        ],
        "task_set": [100, 101, 102]
    }
    """
    users = UserSerializer(many=True, read_only=True)
    user_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True, write_only=True, source='users'
    )
    owner = UserSerializer(read_only=True)
    owner_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, source='owner'
    )

    task_set = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True
    )

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'start_date', 'end_date', 'owner', 'owner_id', 'users', 'user_ids', 'task_set']
