from dependencies import Injector, this
from dependencies.contrib.django import view

from .commands import DispatchRequest, InjectUser, PassKwargs, Service


@view
class DispatchView(Injector):

    view = DispatchRequest


@view
class UserView(Injector):

    view = InjectUser


@view
class KwargsView(Injector):

    view = PassKwargs
    service = Service
    pk = this.kwargs["pk"]  # TODO: partial(int, this...
    slug = this.kwargs["slug"]
