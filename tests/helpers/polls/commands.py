from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse


class DispatchRequest(object):

    def __init__(self, request, args, kwargs):

        self.request = request
        self.args = args
        self.kwargs = kwargs

    def do(self):

        assert self.request.path == "/test_dispatch_request/1/test/"
        assert self.args == ("1", "test")
        assert self.kwargs == {}
        return HttpResponse("<h1>OK</h1>")


class InjectUser(object):

    def __init__(self, user):

        self.user = user

    def do(self):

        assert isinstance(self.user, AnonymousUser)
        return HttpResponse("<h1>OK</h1>")


class PassKwargs(object):

    def __init__(self, pk, slug):

        self.pk = pk
        self.slug = slug

    def do(self):

        assert self.pk == "1"
        assert self.slug == "test"
        return HttpResponse("<h1>OK</h1>")
