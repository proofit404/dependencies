from __future__ import absolute_import

from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView

from ._django import apply_http_methods, create_handler


def api_view(injector):
    """Create DRF class-based API view from injector class."""

    handler = create_handler(APIView)
    apply_http_methods(handler, injector)
    return handler


def generic_api_view(injector):
    """FIXME"""

    handler = create_handler(GenericAPIView)
    apply_http_methods(handler, injector)
    return handler


# TODO:
#
# APIView.renderer_classes
# APIView.parser_classes
# APIView.authentication_classes
# APIView.throttle_classes
# APIView.permission_classes
# APIView.content_negotiation_class
# APIView.metadata_class
# APIView.versioning_class
#
# GenericAPIView.queryset
# GenericAPIView.serializer_class
# GenericAPIView.lookup_field
# GenericAPIView.lookup_url_kwarg
# GenericAPIView.filter_backends
# GenericAPIView.pagination_class
