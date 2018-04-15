from dependencies import Injector, this
from dependencies.contrib.django import view

from .commands import DispatchRequest, InjectKwargs, InjectSelf, InjectUser


class Methods(Injector):

    get = this.command.do
    post = this.command.do
    put = this.command.do
    patch = this.command.do
    delete = this.command.do
    head = this.command.do
    options = this.command.do
    trace = this.command.do


@view
class DispatchView(Methods):

    command = DispatchRequest


@view
class EmptyView(Injector):

    pass


@view
class UserView(Methods):

    command = InjectUser


@view
class KwargsView(Methods):

    command = InjectKwargs
    pk = this.kwargs["pk"]  # TODO: partial(int, this...
    slug = this.kwargs["slug"]


@view
class SelfView(Methods):

    command = InjectSelf
