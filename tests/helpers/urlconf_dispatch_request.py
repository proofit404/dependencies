from dependencies import Injector
from dependencies.contrib.django import view
from django.conf.urls import url


class View(object):

    def __init__(self, request, args, kwargs):

        self.request = request
        self.args = args
        self.kwargs = kwargs

    def get(self):

        assert self.request.path == '/comments/1/test/'
        assert self.args == ('1', 'test')
        assert self.kwargs == {}
        return '<h1>OK</h1>'


@view
class Container(Injector):

    view = View


urlpatterns = [
    # ?P<slug>
    url(r'^comments/(\d+)/(\w+)/$', Container.as_view()),
]
