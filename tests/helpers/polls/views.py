from dependencies import Injector, this
from dependencies.contrib.django import view

from .commands import DispatchRequest, InjectKwargs, InjectSelf, InjectUser


@view
class DispatchView(Injector):

    command = DispatchRequest
    get = this.command.do
    post = this.command.do
    put = this.command.do
    patch = this.command.do
    delete = this.command.do
    head = this.command.do
    options = this.command.do
    trace = this.command.do


@view
class EmptyView(Injector):

    pass


@view
class UserView(Injector):

    command = InjectUser
    get = this.command.do


@view
class KwargsView(Injector):

    command = InjectKwargs
    get = this.command.do
    pk = this.kwargs["pk"]  # TODO: partial(int, this...
    slug = this.kwargs["slug"]


@view
class SelfView(Injector):

    command = InjectSelf
    get = this.command.do
