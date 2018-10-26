from django.contrib.admin.models import ADDITION, CHANGE, DELETION, LogEntry
from django.contrib.auth.models import User
from django.db.models import Model
from rest_framework.renderers import DocumentationRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet


class UserOperations(object):

    def __init__(self, view, request):

        self.view = view
        self.request = request

    def do(self):

        assert self.request.data == {"last": True}
        assert isinstance(self.request.accepted_renderer, DocumentationRenderer)
        return Response({"details": "ok"})

    def login(self):

        raise Exception("Should not got there")

    def respond(self):

        return Response()

    def retrieve(self):

        instance = self.view.get_object()
        serializer = self.view.get_serializer(instance)
        return Response(serializer.data)

    def list(self):

        queryset = self.view.filter_queryset(self.view.get_queryset())
        page = self.view.paginate_queryset(queryset)
        serializer = self.view.get_serializer(page, many=True)
        return self.view.get_paginated_response(serializer.data)


class UserCreateOperations(object):

    def __init__(self, view, request, args, kwargs, user, serializer):

        self.view = view
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.user = user
        self.serializer = serializer

    def create(self):

        assert isinstance(self.view, ModelViewSet)
        assert isinstance(self.request, Request)
        assert self.args == ()
        assert self.kwargs == {}
        assert isinstance(self.serializer, ModelSerializer)

        LogEntry.objects.create(user=self.user, action_flag=ADDITION)

        user = User.objects.create(
            username=self.serializer.validated_data["username"],
            first_name=self.serializer.validated_data["first_name"],
            last_name=self.serializer.validated_data["last_name"],
        )

        return user


class UserUpdateOperations(object):

    def __init__(self, view, request, args, kwargs, user, pk, serializer):

        self.view = view
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.user = user
        self.pk = pk
        self.serializer = serializer

    def update(self):

        assert isinstance(self.view, ModelViewSet)
        assert isinstance(self.request, Request)
        assert self.args == ()
        assert self.kwargs == {"pk": "2"}
        assert self.pk == "2"
        assert isinstance(self.serializer, ModelSerializer)

        LogEntry.objects.create(user=self.user, action_flag=CHANGE)

        user = User.objects.get(**self.kwargs)
        if "username" in self.serializer.validated_data:
            user.username = self.serializer.validated_data["username"]
        if "first_name" in self.serializer.validated_data:
            user.first_name = self.serializer.validated_data["first_name"]
        if "last_name" in self.serializer.validated_data:
            user.last_name = self.serializer.validated_data["last_name"]
        user.save()

        return user


class UserDestroyOperations(object):

    def __init__(self, view, request, args, kwargs, user, pk, instance):

        self.view = view
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.user = user
        self.pk = pk
        self.instance = instance

    def destroy(self):

        assert isinstance(self.view, ModelViewSet)
        assert isinstance(self.request, Request)
        assert self.args == ()
        assert self.kwargs == {"pk": "2"}
        assert self.pk == "2"
        assert isinstance(self.instance, Model)

        self.instance.delete()
        LogEntry.objects.create(user=self.user, action_flag=DELETION)
