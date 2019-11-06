from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import DocumentationRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.status import HTTP_201_CREATED
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.viewsets import GenericViewSet
from rest_framework.viewsets import ViewSet

from dependencies import Injector
from dependencies import operation
from dependencies import this
from dependencies import value
from dependencies.contrib.rest_framework import api_view
from dependencies.contrib.rest_framework import generic_api_view
from dependencies.contrib.rest_framework import generic_view_set
from dependencies.contrib.rest_framework import model_view_set
from dependencies.contrib.rest_framework import view_set
from django_project.api.auth import AuthenticateAdmin
from django_project.api.auth import AuthenticateAll
from django_project.api.commands import UserCreateOperations
from django_project.api.commands import UserDestroyOperations
from django_project.api.commands import UserOperations
from django_project.api.commands import UserUpdateOperations
from django_project.api.filtersets import use_filterset_name
from django_project.api.filtersets import UserFilter
from django_project.api.metadata import DenyMetadata
from django_project.api.negotiation import DenyNegotiation
from django_project.api.serializers import UserSerializer
from django_project.api.throttle import ThrottleEveryOne
from django_project.api.version import DenyVersion


@api_view
class UserAction(Injector):
    """Intentionally left blank."""

    post = this.command.do
    command = UserOperations

    renderer_classes = (DocumentationRenderer,)
    parser_classes = (JSONParser,)


@api_view
class UserLogin(Injector):

    get = this.command.login
    command = UserOperations

    permission_classes = (IsAuthenticated,)


@api_view
class LoginAll(Injector):

    get = this.command.respond
    command = UserOperations

    authentication_classes = (AuthenticateAll,)
    permission_classes = (IsAuthenticated,)


@api_view
class ThrottleAll(Injector):

    get = this.command.login
    command = UserOperations

    throttle_classes = (ThrottleEveryOne,)


@api_view
class DefaultThrottleScope(Injector):
    get = this.command.respond
    command = UserOperations

    throttle_scope = "throttle_scope"


@api_view
class CustomThrottleScope(Injector):
    get = this.command.respond
    command = UserOperations

    custom_throttle_scope = "custom_scope"


@api_view
class BadNegotiation(Injector):

    get = this.command.respond
    command = UserOperations

    content_negotiation_class = DenyNegotiation


@api_view
class BadVersion(Injector):

    get = this.command.respond
    command = UserOperations

    versioning_class = DenyVersion


@api_view
class BadMetadata(Injector):

    get = this.command.respond
    command = UserOperations

    metadata_class = DenyMetadata


@generic_api_view
class UserRetrieveView(Injector):
    """Intentionally left blank."""

    get = this.command.retrieve
    command = UserOperations

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "username"
    lookup_url_kwarg = "nick"


@generic_api_view
class UserListView(Injector):

    get = this.command.collection
    command = UserOperations

    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend,)
    if use_filterset_name:
        filterset_class = UserFilter
    else:
        filter_class = UserFilter
    pagination_class = LimitOffsetPagination


@generic_api_view
class UserListFilterFieldsView(Injector):

    get = this.command.collection
    command = UserOperations

    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend,)
    if use_filterset_name:
        filterset_fields = ["username"]
    else:
        filter_fields = ["username"]
    pagination_class = LimitOffsetPagination


# ViewSet.


@view_set
class InjectedViewSet(Injector):
    """Intentionally left blank."""

    @operation
    def list(view, request, args, kwargs, user, action):

        assert isinstance(view, ViewSet)
        assert isinstance(request, Request)
        assert args == ()
        assert kwargs == {}
        assert action == "list"

        return Response(status=HTTP_200_OK, data={"list": "ok"})

    @operation
    def retrieve(view, request, args, kwargs, user, pk, action):

        assert isinstance(view, ViewSet)
        assert isinstance(request, Request)
        assert args == ()
        assert kwargs == {"pk": "1"}
        assert pk == "1"
        assert action == "retrieve"

        return Response(status=HTTP_200_OK, data={"retrieve": "ok"})

    @operation
    def create(view, request, args, kwargs, user, action):

        assert isinstance(view, ViewSet)
        assert isinstance(request, Request)
        assert args == ()
        assert kwargs == {}
        assert action == "create"

        return Response(status=HTTP_201_CREATED, data={"create": "ok"})

    @operation
    def update(view, request, args, kwargs, user, pk, action):

        assert isinstance(view, ViewSet)
        assert isinstance(request, Request)
        assert args == ()
        assert kwargs == {"pk": "1"}
        assert pk == "1"
        assert action == "update"

        return Response(status=HTTP_200_OK, data={"update": "ok"})

    @operation
    def partial_update(view, request, args, kwargs, user, pk, action):

        assert isinstance(view, ViewSet)
        assert isinstance(request, Request)
        assert args == ()
        assert kwargs == {"pk": "1"}
        assert pk == "1"
        assert action == "partial_update"

        return Response(status=HTTP_200_OK, data={"partial_update": "ok"})

    @operation
    def destroy(view, request, args, kwargs, user, pk, action):

        assert isinstance(view, ViewSet)
        assert isinstance(request, Request)
        assert args == ()
        assert kwargs == {"pk": "1"}
        assert pk == "1"
        assert action == "destroy"

        return Response(status=HTTP_204_NO_CONTENT)


# GenericViewSet.


@generic_view_set
class InjectedGenericViewSet(Injector):

    serializer_class = UserSerializer

    @operation
    def list(view, request, args, kwargs, user, action):

        assert isinstance(view, GenericViewSet)
        assert isinstance(request, Request)
        assert args == ()
        assert kwargs == {}
        assert action == "list"

        return Response(status=HTTP_200_OK, data={"list": "ok"})

    @operation
    def retrieve(view, request, args, kwargs, user, pk, action):

        assert isinstance(view, GenericViewSet)
        assert isinstance(request, Request)
        assert args == ()
        assert kwargs == {"pk": "1"}
        assert pk == "1"
        assert action == "retrieve"

        return Response(status=HTTP_200_OK, data={"retrieve": "ok"})

    @operation
    def create(view, request, args, kwargs, user, action, validated_data):

        assert isinstance(view, GenericViewSet)
        assert isinstance(request, Request)
        assert args == ()
        assert kwargs == {}
        assert action == "create"
        assert validated_data == {
            "username": "johndoe",
            "first_name": "John",
            "last_name": "Doe",
        }

        return Response(status=HTTP_201_CREATED, data={"create": "ok"})

    @operation
    def update(view, request, args, kwargs, user, pk, action, validated_data):

        assert isinstance(view, GenericViewSet)
        assert isinstance(request, Request)
        assert args == ()
        assert kwargs == {"pk": "1"}
        assert pk == "1"
        assert action == "update"
        assert validated_data == {
            "username": "johndoe",
            "first_name": "John",
            "last_name": "Doe",
        }

        return Response(status=HTTP_200_OK, data={"update": "ok"})

    @operation
    def partial_update(view, request, args, kwargs, user, pk, action, validated_data):

        assert isinstance(view, GenericViewSet)
        assert isinstance(request, Request)
        assert args == ()
        assert kwargs == {"pk": "1"}
        assert pk == "1"
        assert action == "partial_update"
        assert validated_data == {"username": "jimworm"}

        return Response(status=HTTP_200_OK, data={"partial_update": "ok"})

    @operation
    def destroy(view, request, args, kwargs, user, pk, action):

        assert isinstance(view, GenericViewSet)
        assert isinstance(request, Request)
        assert args == ()
        assert kwargs == {"pk": "1"}
        assert pk == "1"
        assert action == "destroy"

        return Response(status=HTTP_204_NO_CONTENT)


@model_view_set
class UserViewSet(Injector):
    """Intentionally left blank."""

    authentication_classes = (AuthenticateAdmin,)

    queryset = User.objects.filter(username="johndoe")
    serializer_class = UserSerializer

    create = this.create_command.create
    update = this.update_command.update
    destroy = this.destroy_command.destroy

    create_command = UserCreateOperations
    update_command = UserUpdateOperations
    destroy_command = UserDestroyOperations


@model_view_set
class DynamicUserViewSet(Injector):

    authentication_classes = (AuthenticateAdmin,)

    @value
    def queryset(user, action):

        assert action in {"list", "retrieve", "update", "partial_update", "destroy"}
        assert user.username == "admin"
        return User.objects.filter(username="johndoe")

    serializer_class = UserSerializer

    create = this.create_command.create
    update = this.update_command.update
    destroy = this.destroy_command.destroy

    create_command = UserCreateOperations
    update_command = UserUpdateOperations
    destroy_command = UserDestroyOperations


@model_view_set
class EmptyViewSet(Injector):

    queryset = User.objects.all()
    serializer_class = UserSerializer
