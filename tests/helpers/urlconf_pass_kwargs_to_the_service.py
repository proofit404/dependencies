from dependencies import Injector, this
from dependencies.contrib.django import view
from django.conf.urls import url


class View(object):

    def __init__(self, service):

        self.service = service

    def get(self):

        return self.service.list()


class Service(object):

    def __init__(self, pk, slug):

        self.pk = pk
        self.slug = slug

    def list(self):

        assert self.pk == '1'
        assert self.slug == 'test'
        return '<h1>OK</h1>'


@view
class Container(Injector):

    view = View
    service = Service
    pk = this.kwargs['pk']  # TODO: partial(int, this...
    slug = this.kwargs['slug']


urlpatterns = [
    url(r'^comments/(?P<pk>\d+)/(?P<slug>\w+)/$', Container.as_view()),
]
