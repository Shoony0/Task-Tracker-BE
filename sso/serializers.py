from rest_framework import serializers

class SSOTokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=32)