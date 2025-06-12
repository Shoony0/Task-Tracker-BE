from rest_framework import serializers

class SSOTokenSerializer(serializers.Serializer):
    """
    Serializer for handling SSO (Single Sign-On) token input.

    Fields:
        - token: (required) SSO token string. Maximum length 32 characters.

    Example request:
    {
        "token": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6"
    }
    """
    token = serializers.CharField(max_length=32)