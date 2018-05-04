from rest_framework.renderers import DocumentationRenderer
from rest_framework.response import Response


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

    def retrieve(self):

        instance = self.view.get_object()
        serializer = self.view.get_serializer(instance)
        return Response(serializer.data)

    def list(self):

        queryset = self.view.filter_queryset(self.view.get_queryset())
        page = self.view.paginate_queryset(queryset)
        serializer = self.view.get_serializer(page, many=True)
        return self.view.get_paginated_response(serializer.data)
