from dependencies import Injector
from dependencies.contrib.django import view
from django.conf.urls import url
from django.contrib.auth.models import AnonymousUser


class View(object):

    def __init__(self, user):

        self.user = user

    def get(self):

        assert isinstance(self.user, AnonymousUser)
        return '<h1>OK</h1>'


@view
class Container(Injector):

    view = View


urlpatterns = [
    url(r'^comments/(?P<pk>\d+)/(?P<slug>\w+)/$', Container.as_view()),
]
