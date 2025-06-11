from rest_framework import serializers


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
        fields = ['id', 'username','email', 'first_name', 'last_name', 'roles', 'role_ids']

    def to_internal_value(self, data):
        # Rewrite 'email' input to 'username' to keep compatibility
        if "email" in data:
            data['username'] = data['email']
            
        return super().to_internal_value(data)
