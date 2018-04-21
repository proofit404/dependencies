from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response


class QuestionsStat(object):

    def __init__(self, request):

        assert request.query_params["last"] == "True"
        assert isinstance(request.accepted_renderer, JSONRenderer)

    def do(self):

        return Response({"details": "ok"})
