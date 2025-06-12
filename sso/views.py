import os
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
    """
    Initiates Google OAuth2 login flow.

    Redirects the user to Google's OAuth2 authorization endpoint with required query parameters.

    Permissions:
        - AllowAny: No authentication required to access this endpoint.

    Query Parameters sent to Google:
        - client_id: Google OAuth client ID from settings.
        - response_type: "code" (authorization code grant type).
        - access_type: "offline" (requests refresh token).
        - redirect_uri: Callback URL after successful authorization.
        - scope: Space-separated list of OAuth scopes.
        - include_granted_scopes: Always true (reuse previously granted scopes).
        - state: CSRF protection value or static identifier ("560008" in this case).

    Flow:
        1. User accesses this endpoint.
        2. User is redirected to Google login page.
        3. Upon successful authentication, Google redirects back to `redirect_uri` with authorization code.

    Example usage:
        GET /google-login/

    Returns:
        HttpResponseRedirect: Redirects the user to Google's OAuth2 authorization URL.
    """
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
    """
    Google OAuth2 callback handler.

    This view handles the callback from Google after user authentication.
    It exchanges the authorization code for an ID token, verifies it, and generates access tokens if user exists.

    Permissions:
        - AllowAny: No authentication required (public callback endpoint).

    Flow:
        1. Receives authorization code from Google's redirect.
        2. Exchanges authorization code for tokens.
        3. Verifies ID token.
        4. Checks if user exists in Task Tracker system.
        5. If user exists:
            - Generates JWT tokens.
            - Caches the tokens temporarily (10 seconds).
        6. If user does not exist:
            - Caches error message.
        7. Redirects to frontend with temporary token for SSO completion.

    Query Params (Google Redirect):
        - code: OAuth2 authorization code.

    Query Params (Frontend Redirect):
        - status: "success"
        - token: Temporary SSO token (used to pull cached data).

    Cache:
        - Key: random generated token.
        - Value: JWT tokens or error message.
        - Timeout: 10 seconds.

    Example redirect (success):
        GET {FRONTEND_URI}/sso/?status=success&token=abc123xyz456

    Error handling:
        - Missing code: returns 400.
        - Token exchange failure: returns appropriate HTTP error.
        - ID token verification failure: returns appropriate HTTP error.
        - User not found: returns error message in cached data.

    Returns:
        - HttpResponseRedirect: Redirects to frontend SSO handler with temporary token.
    """
    code = request.GET.get('code', None)
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

    if response.status_code != 200:
        return JsonResponse({"error": "Failed to fetch token"}, status=response.status_code)

    token_data = response.json()
    token = token_data.get("id_token")

    # getting user details 
    try:
        id_info = id_token.verify_oauth2_token(token, google.auth.transport.requests.Request(), client_id)
    except ValueError:
        return JsonResponse({"error": "Failed to fetch user info"}, status=id_info.status_code)
    
    # Extract user information from the token
    email = id_info.get("email")

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
    # caching unique token for 10 sec
    cache.set(response_token, cache_data, timeout=10) # 10 sec

    return HttpResponseRedirect(f"{os.getenv('FRONTEND_URI')}/sso/?status=success&token={response_token}")

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
    """
    SSO token data retriever.

    This endpoint is used by the frontend to exchange the temporary SSO token (received after Google login)
    for the actual authentication tokens (access & refresh tokens) or error message.

    Permissions:
        - AllowAny: No authentication required (public callback endpoint).

    Flow:
        1. Frontend receives temporary token from Google SSO redirect.
        2. Frontend sends POST request to this endpoint with that token.
        3. Backend retrieves token data from cache and deletes it.
        4. Returns token data or error message.

    Request:
        Method: POST
        Body:
            {
                "token": "<temporary_sso_token>"
            }

    Response (success - user exists):
        {
            "access": "<access_token>",
            "refresh": "<refresh_token>"
        }

    Response (failure - user not found):
        {
            "status": "error",
            "message": "User does not exist in Task Tracker system. Please contact admin (admin@tracker.com)."
        }

    Permissions:
        - No authentication required (intended to be called immediately after SSO redirect).

    Notes:
        - The temporary token is deleted from cache after first use to ensure one-time usage.
        - Token timeout is managed during SSO login flow (typically 10 seconds).

    Raises:
        - ValidationError: If token field is missing or invalid.
    """
    serializer = SSOTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    token = serializer.validated_data["token"]
    token_data = cache.get(token, {})
    # The temporary token is deleted from cache after first use to ensure one-time usage.
    # other wise if user  didn't use after 10 sec it will expire
    cache.delete(token)

    return Response(token_data, status=status.HTTP_200_OK)