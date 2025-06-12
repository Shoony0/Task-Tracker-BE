from rest_framework import serializers
from django.contrib.auth.hashers import make_password


from .models import User, Role

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.

    Handles serialization and deserialization of User instances, including:
    - Reading assigned roles using nested RoleSerializer.
    - Writing role assignments via role IDs (write-only field).
    - Allowing password hashing automatically when creating/updating user.
    - Mapping 'email' to 'username' to simplify API client integration.

    Fields:
        - id (read-only): User ID.
        - username: Used as system username (auto-mapped from email on input).
        - email: User's email.
        - first_name: First name of the user.
        - last_name: Last name of the user.
        - roles (read-only): Nested list of Role objects assigned to the user.
        - role_ids (write-only): List of role IDs used to assign roles.
        - password (write-only): User password; automatically hashed.

    Notes:
        - When 'email' is provided in the request, it is mapped to 'username' for internal processing.
        - The password is automatically hashed before being saved to the database.

    Example request (create/update):
    {
        "email": "john.doe@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "role_ids": [1, 2],
        "password": "securePassword123"
    }

    Example response:
    {
        "id": 1,
        "username": "john.doe@example.com",
        "email": "john.doe@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "roles": [
            {
                "id": 1,
                "name": "Admin"
            },
            {
                "id": 2,
                "name": "Task Creator"
            }
        ]
    }
    """
    roles = RoleSerializer(many=True, read_only=True)
    role_ids = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(), many=True, write_only=True, source='roles'
    )

    class Meta:
        model = User
        fields = ['id', 'username','email', 'first_name', 'last_name', 'roles', 'role_ids', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def to_internal_value(self, data):
        """
        Override deserialization logic to handle:
        - Mapping 'email' field to 'username' internally.
        - Hashing passwords before saving.
        """
        if "email" in data:
            data['username'] = data['email']

        if "password" in data:
            data['password'] = make_password(data['password'])
            
        return super().to_internal_value(data)
