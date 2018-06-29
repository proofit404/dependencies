from django.contrib.admin.models import ADDITION, CHANGE, DELETION, LogEntry
from django.db.models import Model
from rest_framework.renderers import DocumentationRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import GenericViewSet


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


class UserSetOperations(object):

    def __init__(
        self, view, request, args, kwargs, user, serializer=None, instance=None
    ):

        self.view = view
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.user = user
        self.serializer = serializer
        self.instance = instance

    def create(self):

        assert isinstance(self.view, GenericViewSet)
        assert isinstance(self.request, Request)
        assert self.args == ()
        assert self.kwargs == {}
        assert isinstance(self.serializer, ModelSerializer)
        assert self.instance is None

        self.serializer.save()
        LogEntry.objects.create(user=self.user, action_flag=ADDITION)

    def update(self):

        assert isinstance(self.view, GenericViewSet)
        assert isinstance(self.request, Request)
        assert self.args == ()
        assert self.kwargs == {"pk": "2"}
        assert isinstance(self.serializer, ModelSerializer)
        assert self.instance is None

        self.serializer.save()
        LogEntry.objects.create(user=self.user, action_flag=CHANGE)

    def destroy(self):

        assert isinstance(self.view, GenericViewSet)
        assert isinstance(self.request, Request)
        assert self.args == ()
        assert self.kwargs == {"pk": "2"}
        assert self.serializer is None
        assert isinstance(self.instance, Model)

        self.instance.delete()
        LogEntry.objects.create(user=self.user, action_flag=DELETION)
