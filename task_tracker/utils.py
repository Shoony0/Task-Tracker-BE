from rest_framework.views import exception_handler
from rest_framework.exceptions import Throttled
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, Throttled):
        custom_message = "Too many requests. Please try again later."
        return Response({"detail": custom_message}, status=429)

    return response
