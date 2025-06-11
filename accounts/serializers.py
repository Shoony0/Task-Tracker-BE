from rest_framework import serializers
from django.contrib.auth.hashers import make_password


from .models import User, Role

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']

class UserSerializer(serializers.ModelSerializer):
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
        # Rewrite 'email' input to 'username' to keep compatibility
        if "email" in data:
            data['username'] = data['email']

        if "password" in data:
            data['password'] = make_password(data['password'])
            
        return super().to_internal_value(data)
