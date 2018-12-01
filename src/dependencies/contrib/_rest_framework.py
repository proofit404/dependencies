from __future__ import absolute_import

from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from dependencies import this
from dependencies.contrib._django import apply_http_methods, create_handler
from dependencies.exceptions import DependencyError


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

            def locals_hack(attribute=attribute):
                @property
                def __attribute(self):
                    ns = injector.let(
                        **{
                            "view": self,
                            "request": this.view.request,
                            "args": this.view.args,
                            "kwargs": this.view.kwargs,
                            "user": this.request.user,
                            "pk": this.kwargs["pk"],  # TODO: partial(int, this...
                        }
                    )
                    return getattr(ns, attribute)

                return __attribute

            setattr(handler, attribute, locals_hack())


def apply_generic_api_view_methods(handler, injector):

    # FIXME: Router issue.
    #
    # REST Framework tries to access ViewSet.queryset.model if we add
    # this ViewSet to the router without basename.
    #
    # Property itself can not be monkey patched.  I think queryset
    # should be wrapped in custom property subclass with model
    # attribute defined.  If dependency injection error occurs, we
    # should say explicitly about basename attribute.

    for attribute in [
        "queryset",
        "serializer_class",
        "lookup_field",
        "lookup_url_kwarg",
        "filter_backends",
        "filterset_class",
        "filter_class",  # Legacy name for django-filter 1.x
        "pagination_class",
    ]:
        if attribute in injector:

            def locals_hack(attribute=attribute):
                @property
                def __attribute(self):
                    ns = injector.let(
                        **{
                            "view": self,
                            "request": this.view.request,
                            "args": this.view.args,
                            "kwargs": this.view.kwargs,
                            "user": this.request.user,
                            "pk": this.kwargs["pk"],  # TODO: partial(int, this...
                        }
                    )
                    return getattr(ns, attribute)

                return __attribute

            setattr(handler, attribute, locals_hack())


def apply_model_view_set_methods(handler, injector):
    def create_arguments(ns, serializer):

        ns["validated_data"] = serializer.validated_data
        return ns

    def update_arguments(ns, serializer):

        ns["validated_data"] = serializer.validated_data
        ns["instance"] = serializer.instance
        return ns

    def delete_arguments(ns, instance):

        ns["instance"] = instance
        return ns

    def set_instance(serializer, instance):

        # TODO:
        #
        # * Assert instance is not None. Suggest an edit to fix it.
        #
        # * Compare serializer.meta.model against instance type.

        serializer.instance = instance

    def ignore(instance, nothing):

        # TODO:
        #
        # * Assert nothing is None.

        pass

    for method, set_args, cb in [
        ("create", create_arguments, set_instance),
        ("update", update_arguments, set_instance),
        ("destroy", delete_arguments, ignore),
    ]:
        if method in injector:

            def locals_hack(method=method, set_args=set_args, cb=cb):
                def __method(self, argument):
                    ns = injector.let(
                        **set_args(
                            {
                                "view": self,
                                "request": this.view.request,
                                "args": this.view.args,
                                "kwargs": this.view.kwargs,
                                "user": this.request.user,
                                "pk": this.kwargs["pk"],  # TODO: partial(int, this...
                            },
                            argument,
                        )
                    )
                    cb(argument, getattr(ns, method)())

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
