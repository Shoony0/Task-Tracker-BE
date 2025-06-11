import urllib.parse
from django.http import HttpResponseRedirect
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth import get_user_model
User = get_user_model()

from sso.utils import generate_random_string 
from django.http import HttpResponseRedirect
import requests
from google.oauth2 import id_token
import google.auth.transport.requests
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from .serializers import SSOTokenSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi



@permission_classes([AllowAny])
def google_login(request):
    auth_url = f"{settings.GOOGLE_AUTHORITY}/v2/auth"
    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "response_type": "code",
        "access_type": "offline",
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "scope": " ".join(settings.GOOGLE_SCOPES),
        "include_granted_scopes": "true",  
        "state": "560008",  # state_parameter_passthrough_value
    }
    login_url = f"{auth_url}?{urllib.parse.urlencode(params)}"
    return HttpResponseRedirect(login_url)

@permission_classes([AllowAny])
def google_callback(request):
    code = request.GET.get('code', None)
    print('request.GET')
    print(request.GET)
    if not code:
        return JsonResponse({"error": "No code provided"}, status=400)
    
    client_id = settings.GOOGLE_CLIENT_ID
    # Exchange code for access token
    token_url = f"{settings.GOOGLE_AUTHORITY}/token"

    data = {
        "client_id": client_id,
        "scope": " ".join(settings.GOOGLE_SCOPES),
        "code": code,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
    }

    response = requests.post(token_url, data=data)
    print("Done")
    # Log the response for debugging
    print(f"Token response status: {response.status_code}")
    print(f"Token response body: {response.text}")

    if response.status_code != 200:
        return JsonResponse({"error": "Failed to fetch token"}, status=response.status_code)

    token_data = response.json()
    token = token_data.get("id_token")

    try:
        id_info = id_token.verify_oauth2_token(token, google.auth.transport.requests.Request(), client_id)
    except ValueError:
        return JsonResponse({"error": "Failed to fetch user info"}, status=id_info.status_code)
    
    print(f"{id_info = }")
    # Extract user information from the token
    email = id_info.get("email")
    # first_name = id_info.get("given_name", "")
    # last_name = id_info.get("family_name", "")

    response_token=generate_random_string()
    user = User.objects.filter(email=email)
    if user.exists():
        # Generate a token (e.g., JWT or session)
        refresh = RefreshToken.for_user(user.first())
        cache_data = {
            "access": str(refresh.access_token), 
            "refresh": str(refresh)
        }
    else:
        cache_data =  {
            "status": "error",
            "message": "User is not exists with 'Task Tracker' System. please contact to admin e.g. admin@tracker.com"
        }
    cache.set(response_token, cache_data, timeout=5) # 5 sec

    return HttpResponseRedirect(f"http://localhost:3000/sso/?status=success&token={response_token}")

@swagger_auto_schema(
    method='post',
    request_body=SSOTokenSerializer,
    responses={
        200: openapi.Response(description="Token data found"),
        404: openapi.Response(description="Token not found or expired"),
        400: "Bad Request"
    }
)
@api_view(["POST"])
@permission_classes([AllowAny])
def sso_token_data(request):
    serializer = SSOTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    token = serializer.validated_data["token"]
    token_data = cache.get(token, {})
    cache.delete(token)

    return Response(token_data, status=status.HTTP_200_OK)