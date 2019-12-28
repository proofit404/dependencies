from django.contrib.admin.models import ADDITION
from django.contrib.admin.models import CHANGE
from django.contrib.admin.models import DELETION
from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import User
from rest_framework.renderers import DocumentationRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


class _UserOperations(object):
    def __init__(self, view, request):
        self.view = view
        self.request = request

    def do(self):
        assert self.request.data == {"last": True}
        assert isinstance(self.request.accepted_renderer, DocumentationRenderer)
        return Response({"details": "ok"})

    def login(self):
        raise Exception("Should not got there")  # pragma: no cover

    def respond(self):
        return Response()

    def retrieve(self):
        instance = self.view.get_object()
        serializer = self.view.get_serializer(instance)
        return Response(serializer.data)

    def collection(self):
        queryset = self.view.filter_queryset(self.view.get_queryset())
        page = self.view.paginate_queryset(queryset)
        serializer = self.view.get_serializer(page, many=True)
        return self.view.get_paginated_response(serializer.data)


class _UserCreateOperations(object):
    def __init__(self, view, request, args, kwargs, user, validated_data, action):
        self.view = view
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.user = user
        self.validated_data = validated_data
        self.action = action

    def create(self):
        assert isinstance(self.view, ModelViewSet)
        assert isinstance(self.request, Request)
        assert self.args == ()
        assert self.kwargs == {}
        assert isinstance(self.validated_data, dict)
        assert self.action == "create"
        LogEntry.objects.create(user=self.user, action_flag=ADDITION)
        user = User.objects.create(
            username=self.validated_data["username"],
            first_name=self.validated_data["first_name"],
            last_name=self.validated_data["last_name"],
        )
        return user


class _UserUpdateOperations(object):
    def __init__(
        self, view, request, args, kwargs, user, pk, validated_data, instance, action
    ):
        self.view = view
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.user = user
        self.pk = pk
        self.validated_data = validated_data
        self.instance = instance
        self.action = action

    def update(self):
        assert isinstance(self.view, ModelViewSet)
        assert isinstance(self.request, Request)
        assert self.args == ()
        assert self.kwargs == {"pk": "2"}
        assert self.pk == "2"
        assert isinstance(self.validated_data, dict)
        assert isinstance(self.instance, User)
        assert self.action in {"update", "partial_update"}
        LogEntry.objects.create(user=self.user, action_flag=CHANGE)
        if "username" in self.validated_data:
            self.instance.username = self.validated_data["username"]
        if "first_name" in self.validated_data:
            self.instance.first_name = self.validated_data["first_name"]
        if "last_name" in self.validated_data:
            self.instance.last_name = self.validated_data["last_name"]
        self.instance.save()
        return self.instance


class _UserDestroyOperations(object):
    def __init__(self, view, request, args, kwargs, user, pk, instance, action):
        self.view = view
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.user = user
        self.pk = pk
        self.instance = instance
        self.action = action

    def destroy(self):
        assert isinstance(self.view, ModelViewSet)
        assert isinstance(self.request, Request)
        assert self.args == ()
        assert self.kwargs == {"pk": "2"}
        assert self.pk == "2"
        assert isinstance(self.instance, User)
        assert self.action == "destroy"
        self.instance.delete()
        LogEntry.objects.create(user=self.user, action_flag=DELETION)
