from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

@api_view(['GET'])
@permission_classes([AllowAny])
def health(request):
    """
    Health check endpoint.

    Returns a 200 OK response with a message indicating that the Django server
    is up and running. This endpoint requires no authentication and can be used
    for load balancer health checks, uptime monitoring, or readiness probes.

    Returns:
        Response: A JSON response with a simple status message.
    """
    return Response({
        "message": "Django Server up and running."
    }, 200)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer