from __future__ import absolute_import

from dependencies import this
from dependencies.exceptions import DependencyError
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

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


def model_view_set(injector):
    """Create DRF model view set from injector class."""

    handler = create_handler(ModelViewSet)
    apply_api_view_methods(handler, injector)
    apply_generic_api_view_methods(handler, injector)
    apply_model_view_set_methods(handler, injector)
    return injector.let(view_set_class=handler)


def apply_api_view_methods(handler, injector):

    for attribute in [
        "authentication_classes",
        "renderer_classes",
        "parser_classes",
        "throttle_classes",
        "permission_classes",
        "content_negotiation_class",
        "versioning_class",
        "metadata_class",
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


def apply_model_view_set_methods(handler, injector):

    for method, argname in [
        ("create", "serializer"),
        ("update", "serializer"),
        ("destroy", "instance"),
    ]:
        if method in injector:

            def locals_hack(method=method, argname=argname):

                def __method(self, argument):
                    ns = injector.let(
                        **{
                            "view": self,
                            "request": this.view.request,
                            "args": this.view.args,
                            "kwargs": this.view.kwargs,
                            "user": this.request.user,
                            "pk": this.kwargs["pk"],  # TODO: partial(int, this...
                            argname: argument,
                        }
                    )
                    return getattr(ns, method)()

                return __method

        else:

            def locals_hack(method=method, ns=injector.__name__):

                def __method(self, argument):
                    raise DependencyError(
                        "Add {method!r} to the {ns!r} injector".format(
                            method=method, ns=ns
                        )
                    )

                return __method

        setattr(handler, "perform_" + method, locals_hack())
