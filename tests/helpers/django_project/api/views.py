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
from django_project.api.auth import _AuthenticateAdmin
from django_project.api.auth import _AuthenticateAll
from django_project.api.commands import _UserCreateOperations
from django_project.api.commands import _UserDestroyOperations
from django_project.api.commands import _UserOperations
from django_project.api.commands import _UserUpdateOperations
from django_project.api.filtersets import _UserFilter
from django_project.api.filtersets import use_filterset_name
from django_project.api.metadata import _DenyMetadata
from django_project.api.negotiation import _DenyNegotiation
from django_project.api.serializers import _UserSerializer
from django_project.api.throttle import _ThrottleEveryOne
from django_project.api.version import _DenyVersion


@api_view
class _UserAction(Injector):
    """Intentionally left blank."""

    post = this.command.do
    command = _UserOperations
    renderer_classes = (DocumentationRenderer,)
    parser_classes = (JSONParser,)


@api_view
class _UserLogin(Injector):
    get = this.command.login
    command = _UserOperations
    permission_classes = (IsAuthenticated,)


@api_view
class _LoginAll(Injector):
    get = this.command.respond
    command = _UserOperations
    authentication_classes = (_AuthenticateAll,)
    permission_classes = (IsAuthenticated,)


@api_view
class _ThrottleAll(Injector):
    get = this.command.login
    command = _UserOperations
    throttle_classes = (_ThrottleEveryOne,)


@api_view
class _DefaultThrottleScope(Injector):
    get = this.command.respond
    command = _UserOperations
    throttle_scope = "throttle_scope"


@api_view
class _CustomThrottleScope(Injector):
    get = this.command.respond
    command = _UserOperations
    custom_throttle_scope = "custom_scope"


@api_view
class _BadNegotiation(Injector):
    get = this.command.respond
    command = _UserOperations
    content_negotiation_class = _DenyNegotiation


@api_view
class _BadVersion(Injector):
    get = this.command.respond
    command = _UserOperations
    versioning_class = _DenyVersion


@api_view
class _BadMetadata(Injector):
    get = this.command.respond
    command = _UserOperations
    metadata_class = _DenyMetadata


@generic_api_view
class _UserRetrieveView(Injector):
    """Intentionally left blank."""

    get = this.command.retrieve
    command = _UserOperations
    queryset = User.objects.all()
    serializer_class = _UserSerializer
    lookup_field = "username"
    lookup_url_kwarg = "nick"


@generic_api_view
class _UserListView(Injector):
    get = this.command.collection
    command = _UserOperations
    queryset = User.objects.all()
    serializer_class = _UserSerializer
    filter_backends = (DjangoFilterBackend,)
    if use_filterset_name:
        filterset_class = _UserFilter
    else:
        filter_class = _UserFilter
    pagination_class = LimitOffsetPagination


@generic_api_view
class _UserListFilterFieldsView(Injector):
    get = this.command.collection
    command = _UserOperations
    queryset = User.objects.all()
    serializer_class = _UserSerializer
    filter_backends = (DjangoFilterBackend,)
    if use_filterset_name:
        filterset_fields = ["username"]
    else:
        filter_fields = ["username"]
    pagination_class = LimitOffsetPagination


# ViewSet.


@view_set
class _InjectedViewSet(Injector):
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
class _InjectedGenericViewSet(Injector):
    serializer_class = _UserSerializer

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
class _UserViewSet(Injector):
    """Intentionally left blank."""

    authentication_classes = (_AuthenticateAdmin,)
    queryset = User.objects.filter(username="johndoe")
    serializer_class = _UserSerializer
    create = this.create_command.create
    update = this.update_command.update
    destroy = this.destroy_command.destroy
    create_command = _UserCreateOperations
    update_command = _UserUpdateOperations
    destroy_command = _UserDestroyOperations


@model_view_set
class _DynamicUserViewSet(Injector):
    authentication_classes = (_AuthenticateAdmin,)

    @value
    def queryset(user, action):
        assert action in {"list", "retrieve", "update", "partial_update", "destroy"}
        assert user.username == "admin"
        return User.objects.filter(username="johndoe")

    serializer_class = _UserSerializer
    create = this.create_command.create
    update = this.update_command.update
    destroy = this.destroy_command.destroy
    create_command = _UserCreateOperations
    update_command = _UserUpdateOperations
    destroy_command = _UserDestroyOperations


@model_view_set
class _EmptyViewSet(Injector):
    queryset = User.objects.all()
    serializer_class = _UserSerializer
