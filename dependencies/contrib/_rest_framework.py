from rest_framework.views import APIView

from ._django import apply_http_methods, create_handler


def api_view(injector):
    """Create DRF class-based API view from injector class."""

    handler = create_handler(APIView)
    apply_http_methods(handler, injector)
    return handler
