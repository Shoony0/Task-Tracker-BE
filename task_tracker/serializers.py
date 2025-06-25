
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["short_name"] = f'{user.first_name[0]} {user.last_name[0]}'
        token["roles"] = [ role.name for role in user.roles.all()] if user.roles.exists() else []
        return token


