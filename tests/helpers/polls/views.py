from dependencies import Injector, this
from dependencies.contrib.django import view

from .commands import DispatchRequest, InjectUser, PassKwargs


@view
class DispatchView(Injector):

    view = DispatchRequest
    get = this.view.do
    post = this.view.do
    put = this.view.do
    patch = this.view.do
    delete = this.view.do
    head = this.view.do
    options = this.view.do
    trace = this.view.do


@view
class EmptyView(Injector):

    pass


@view
class UserView(Injector):

    view = InjectUser
    get = this.view.do


@view
class KwargsView(Injector):

    view = PassKwargs
    get = this.view.do
    pk = this.kwargs["pk"]  # TODO: partial(int, this...
    slug = this.kwargs["slug"]
