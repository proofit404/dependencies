from __future__ import absolute_import

from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet, ViewSet

from dependencies import this, value
from dependencies.contrib._django import apply_http_methods, create_handler
from dependencies.exceptions import DependencyError


def api_view(injector):
    """Create DRF class-based API view from injector class."""

    handler = create_handler(APIView, injector)
    apply_http_methods(handler, injector)
    apply_api_view_attributes(handler, injector)
    return injector.let(as_view=handler.as_view)


def generic_api_view(injector):
    """Create DRF generic class-based API view from injector class."""

    handler = create_handler(GenericAPIView, injector)
    apply_http_methods(handler, injector)
    apply_api_view_attributes(handler, injector)
    apply_generic_api_view_attributes(handler, injector)
    return injector.let(as_view=handler.as_view)


def list_api_view(injector):
    """Create DRF view for listing a queryset from injector class."""

    # FIXME:
    #
    # [ ] Test me.
    #
    # [ ] Doc me.
    handler = create_handler(ListAPIView, injector)
    apply_api_view_attributes(handler, injector)
    apply_generic_api_view_attributes(handler, injector)
    return injector.let(as_view=handler.as_view)


def retrieve_api_view(injector):
    """Create DRF view for retrieving a model instance from injector class."""

    # FIXME:
    #
    # [ ] Write separate test module for each public function.
    #
    # [ ] Test me.
    #
    # [ ] Doc me.
    handler = create_handler(RetrieveAPIView, injector)
    apply_api_view_attributes(handler, injector)
    apply_generic_api_view_attributes(handler, injector)
    return injector.let(as_view=handler.as_view)


def view_set(injector):
    """Create DRF view set from injector class."""

    # FIXME:
    #
    # [ ] Test me.
    #
    # [ ] Doc me.
    handler = create_handler(ViewSet, injector)
    apply_api_view_attributes(handler, injector)
    apply_view_set_methods(handler, injector)
    return injector.let(as_viewset=lambda: handler)


def generic_view_set(injector):
    """Create DRF generic view set from injector class."""

    # FIXME:
    #
    # [ ] Test me.
    #
    # [ ] Doc me.
    handler = create_handler(GenericViewSet, injector)
    apply_api_view_attributes(handler, injector)
    apply_generic_api_view_attributes(handler, injector)
    apply_view_set_methods(handler, injector)
    return injector.let(as_viewset=lambda: handler)


def model_view_set(injector):
    """Create DRF model view set from injector class."""

    handler = create_handler(ModelViewSet, injector)
    apply_api_view_attributes(handler, injector)
    apply_generic_api_view_attributes(handler, injector)
    apply_model_view_set_methods(handler, injector)
    return injector.let(as_viewset=lambda: handler)


def apply_api_view_attributes(handler, injector):

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
                    __tracebackhide__ = True
                    ns = injector.let(
                        view=self,
                        request=this.view.request,
                        args=this.view.args,
                        kwargs=this.view.kwargs,
                        user=this.request.user,
                        pk=this.kwargs["pk"],
                    )
                    return getattr(ns, attribute)

                return __attribute

            setattr(handler, attribute, locals_hack())


def apply_generic_api_view_attributes(handler, injector):

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
        "filterset_fields",
        "filter_class",  # Legacy name for django-filter 1.x
        "filter_fields",  # Legacy name for django-filter 1.x
        "pagination_class",
    ]:
        if attribute in injector:

            def locals_hack(attribute=attribute):
                @property
                def __attribute(self):
                    __tracebackhide__ = True
                    ns = injector.let(
                        view=self,
                        request=this.view.request,
                        args=this.view.args,
                        kwargs=this.view.kwargs,
                        user=this.request.user,
                        pk=this.kwargs["pk"],
                        action=this.view.action,
                    )
                    return getattr(ns, attribute)

                return __attribute

            setattr(handler, attribute, locals_hack())


def apply_view_set_methods(handler, injector):

    for action, detail, validated_data in [
        ("list", False, None),
        ("create", False, get_validated_data),
        ("retrieve", True, None),
        ("update", True, get_validated_data),
        ("partial_update", True, get_validated_data),
        ("destroy", True, None),
    ]:
        if action in injector:

            def locals_hack(
                action=action, detail=detail, validated_data=validated_data
            ):
                def __action(self, request, *args, **kwargs):
                    __tracebackhide__ = True
                    scope = build_injection_scope(self, detail, True, validated_data)
                    ns = injector.let(**scope)
                    return getattr(ns, action)()

                return __action

            setattr(handler, action, locals_hack())


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
                    __tracebackhide__ = True
                    ns = injector.let(
                        **set_args(
                            {
                                "view": self,
                                "request": this.view.request,
                                "args": this.view.args,
                                "kwargs": this.view.kwargs,
                                "user": this.request.user,
                                "pk": this.kwargs["pk"],
                                "action": this.view.action,
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


@value
def get_validated_data(view, request):

    serializer = view.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return serializer.validated_data


def build_injection_scope(
    view, detail=False, view_set=False, validated_data=None, instance=None
):
    scope = {
        "view": view,
        "request": this.view.request,
        "args": this.view.args,
        "kwargs": this.view.kwargs,
        "user": this.request.user,
    }
    if detail:
        scope["pk"] = this.kwargs["pk"]
    if view_set:
        scope["action"] = this.view.action
    if validated_data is not None:
        scope["validated_data"] = validated_data
    if instance is not None:
        scope["instance"] = instance
    return scope
