from __future__ import absolute_import

from rest_framework.generics import GenericAPIView
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import ViewSet

from _dependencies.contrib.django import apply_http_methods
from _dependencies.contrib.django import build_view_property
from _dependencies.contrib.django import create_handler
from _dependencies.exceptions import DependencyError
from _dependencies.this import this
from _dependencies.value import Value


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


# FIXME:
#
# [ ] create_api_view
#
# [ ] destroy_api_view
#
# [ ] update_api_view


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


def add_custom_attributes_from_throttle_classes(attributes_list):
    for throttle_class in api_settings.DEFAULT_THROTTLE_CLASSES:
        if throttle_class.scope_attr not in attributes_list:
            attributes_list.append(throttle_class.scope_attr)
    return attributes_list


def apply_api_view_attributes(handler, injector):

    attributes_list = [
        "authentication_classes",
        "renderer_classes",
        "parser_classes",
        "throttle_classes",
        "throttle_scope",
        "permission_classes",
        "content_negotiation_class",
        "versioning_class",
        "metadata_class",
    ]
    attributes_list = add_custom_attributes_from_throttle_classes(attributes_list)
    for attribute in attributes_list:
        if attribute in injector:
            view_property = build_view_property(
                injector, attribute, action=this.view.action
            )
            setattr(handler, attribute, view_property)


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
            view_property = build_view_property(
                injector, attribute, action=this.view.action
            )
            setattr(handler, attribute, view_property)


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
            view_action = build_view_action(injector, action, detail, validated_data)
            setattr(handler, action, view_action)


def apply_model_view_set_methods(handler, injector):
    def create_arguments(ns, serializer):

        ns["validated_data"] = serializer.validated_data

    def update_arguments(ns, serializer):

        ns["validated_data"] = serializer.validated_data
        ns["instance"] = serializer.instance

    def delete_arguments(ns, instance):

        ns["instance"] = instance

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

    for method, set_args, callback in [
        ("create", create_arguments, set_instance),
        ("update", update_arguments, set_instance),
        ("destroy", delete_arguments, ignore),
    ]:
        if method in injector:
            viewset_method = build_view_set_method(injector, method, set_args, callback)
        else:
            viewset_method = build_view_set_error(injector, method)
        setattr(handler, "perform_" + method, viewset_method)


@Value
def get_validated_data(view, request):

    serializer = view.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return serializer.validated_data


def build_view_action(injector, action, detail, validated_data):
    def __action(self, request, *args, **kwargs):
        __tracebackhide__ = True
        scope = {
            "view": self,
            "request": this.view.request,
            "args": this.view.args,
            "kwargs": this.view.kwargs,
            "user": this.request.user,
            "action": action,
        }
        if detail:
            scope["pk"] = this.kwargs["pk"]
        if validated_data is not None:
            scope["validated_data"] = validated_data
        ns = injector.let(**scope)
        return getattr(ns, action)()

    return __action


def build_view_set_method(injector, method, set_args, callback):
    def __method(self, argument):
        __tracebackhide__ = True
        scope = {
            "view": self,
            "request": this.view.request,
            "args": this.view.args,
            "kwargs": this.view.kwargs,
            "user": this.request.user,
            "pk": this.kwargs["pk"],
            "action": this.view.action,
        }
        set_args(scope, argument)
        ns = injector.let(**scope)
        callback(argument, getattr(ns, method)())

    return __method


def build_view_set_error(injector, method):
    def __method(self, argument):
        raise DependencyError(
            "Add {!r} to the {!r} injector".format(method, injector.__name__)
        )

    return __method
