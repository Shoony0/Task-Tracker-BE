from django.urls import path
from .views import google_login, google_callback, sso_token_data


urlpatterns = [
    path("auth/google/login/", google_login, name="google_login"), # http://localhost:8000/api/auth/google/login/
    path("auth/google/callback/", google_callback, name="google_callback"),
    path("sso/token/data/", sso_token_data, name="sso_token_data"),
]