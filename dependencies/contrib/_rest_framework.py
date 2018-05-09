from __future__ import absolute_import

from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView

from ._django import apply_http_methods, create_handler


def api_view(injector):
    """Create DRF class-based API view from injector class."""

    handler = create_handler(APIView)
    apply_http_methods(handler, injector)
    apply_api_view_methods(handler, injector)
    return injector.let(as_view=handler.as_view)


def generic_api_view(injector):
    """Create DRF generic class-based API view from injector class."""

    handler = create_handler(GenericAPIView)
    apply_http_methods(handler, injector)
    apply_api_view_methods(handler, injector)
    apply_generic_api_view_methods(handler, injector)
    return injector.let(as_view=handler.as_view)


def apply_api_view_methods(handler, injector):

    for attribute in [
        "authentication_classes",
        "renderer_classes",
        "parser_classes",
        "permission_classes",
    ]:
        if attribute in injector:
            setattr(handler, attribute, getattr(injector, attribute))


def apply_generic_api_view_methods(handler, injector):

    for attribute in [
        "queryset",
        "serializer_class",
        "lookup_field",
        "lookup_url_kwarg",
        "filter_backends",
        "filter_class",
        "pagination_class",
    ]:
        if attribute in injector:
            setattr(handler, attribute, getattr(injector, attribute))


# TODO:
#
# APIView.throttle_classes
# APIView.content_negotiation_class
# APIView.metadata_class
# APIView.versioning_class
