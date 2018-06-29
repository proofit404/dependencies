from dependencies import Injector, this
from dependencies.contrib.rest_framework import (
    api_view,
    generic_api_view,
    model_view_set,
)
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import DocumentationRenderer

from .auth import AuthenticateAdmin, AuthenticateAll
from .commands import UserOperations, UserSetOperations
from .filtersets import UserFilter
from .metadata import DenyMetadata
from .negotiation import DenyNegotiation
from .serializers import UserSerializer
from .throttle import ThrottleEveryOne
from .version import DenyVersion


@api_view
class UserAction(Injector):

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

    get = this.command.retrieve
    command = UserOperations

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "username"
    lookup_url_kwarg = "nick"


@generic_api_view
class UserListView(Injector):

    get = this.command.list
    command = UserOperations

    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = UserFilter
    pagination_class = LimitOffsetPagination


@model_view_set
class UserViewSet(Injector):

    authentication_classes = (AuthenticateAdmin,)

    queryset = User.objects.filter(username="johndoe")
    serializer_class = UserSerializer

    create = this.command.create
    update = this.command.update
    destroy = this.command.destroy

    command = UserSetOperations
