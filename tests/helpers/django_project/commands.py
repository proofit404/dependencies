from django.contrib.auth.models import AnonymousUser
from django.forms import Form
from django.http import HttpResponse
from django.views.generic import View


class DispatchRequest(object):
    def __init__(self, request, args, kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs

    def do(self):
        assert self.request.path in {
            "/test_dispatch_request/1/test/",
            "/test_empty_request/1/test/",
        }
        assert self.args == ("1", "test")
        assert self.kwargs == {}
        return HttpResponse("<h1>OK</h1>")


class InjectUser(object):
    def __init__(self, user):
        self.user = user

    def do(self):
        assert isinstance(self.user, AnonymousUser)
        return HttpResponse("<h1>OK</h1>")


class InjectKwargs(object):
    def __init__(self, pk, slug):
        self.pk = pk
        self.slug = slug

    def do(self):
        assert self.pk == "1"
        assert self.slug == "test"
        return HttpResponse("<h1>OK</h1>")


class InjectSelf(object):
    def __init__(self, view):
        self.view = view

    def do(self):
        assert isinstance(self.view, View)
        return HttpResponse("<h1>OK</h1>")


class ProcessQuestion(object):
    def __init__(self, view, form, request, args, kwargs, user, pk):
        self.view = view
        self.form = form
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.user = user
        self.pk = pk

    def handle_form(self):
        assert isinstance(self.view, View)
        assert isinstance(self.form, Form)
        assert self.request.path == "/test_form_view/1/"
        assert self.args == ()
        assert self.kwargs == {"pk": "1"}
        assert self.pk == "1"
        assert isinstance(self.user, AnonymousUser)
        return HttpResponse("<h1>OK</h1>")

    def handle_error(self):
        assert isinstance(self.view, View)
        assert isinstance(self.form, Form)
        assert self.request.path == "/test_form_view/1/"
        assert self.args == ()
        assert self.kwargs == {"pk": "1"}
        assert self.pk == "1"
        assert isinstance(self.user, AnonymousUser)
        return HttpResponse("<h1>ERROR</h1>")
