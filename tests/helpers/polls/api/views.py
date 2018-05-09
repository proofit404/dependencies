from dependencies import Injector, this
from dependencies.contrib.rest_framework import api_view, generic_api_view
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import DocumentationRenderer

from .auth import AuthenticateAll
from .commands import UserOperations
from .filtersets import UserFilter
from .serializers import UserSerializer


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


@generic_api_view
class UserRetrieveView(Injector):

    get = this.command.retrieve
    command = UserOperations

    queryset = User.objects.all()
    serializer_cls = UserSerializer
    lookup_field = "username"
    lookup_url_kwarg = "nick"


@generic_api_view
class UserListView(Injector):

    get = this.command.list
    command = UserOperations

    queryset = User.objects.all()
    serializer_cls = UserSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_cls = UserFilter
    pagination_cls = LimitOffsetPagination
