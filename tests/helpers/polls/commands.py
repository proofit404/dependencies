from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse


class DispatchRequest(object):

    def __init__(self, request, args, kwargs):

        self.request = request
        self.args = args
        self.kwargs = kwargs

    def get(self):

        assert self.request.path == "/test_dispatch_request/1/test/"
        assert self.args == ("1", "test")
        assert self.kwargs == {}
        return HttpResponse("<h1>OK</h1>")


class InjectUser(object):

    def __init__(self, user):

        self.user = user

    def get(self):

        assert isinstance(self.user, AnonymousUser)
        return HttpResponse("<h1>OK</h1>")


class PassKwargs(object):

    def __init__(self, service):

        self.service = service

    def get(self):

        return self.service.list()


class Service(object):

    def __init__(self, pk, slug):

        self.pk = pk
        self.slug = slug

    def list(self):

        assert self.pk == "1"
        assert self.slug == "test"
        return HttpResponse("<h1>OK</h1>")
