from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response


class QuestionsStat(object):

    def __init__(self, request):

        assert request.query_params["last"] == "True"
        assert isinstance(request.accepted_renderer, JSONRenderer)

    def do(self):

        return Response({"details": "ok"})


class UserOperations(object):

    def __init__(self, view):

        self.view = view

    def retrieve(self):

        instance = self.view.get_object()
        serializer = self.view.get_serializer(instance)
        return Response(serializer.data)

    def list(self):

        queryset = self.view.filter_queryset(self.view.get_queryset())
        page = self.view.paginate_queryset(queryset)
        serializer = self.view.get_serializer(page, many=True)
        return self.view.get_paginated_response(serializer.data)
