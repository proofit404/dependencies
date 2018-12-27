from dependencies import Injector, this
from dependencies.contrib.flask import method_view

from .commands import DispatchRequest


class Methods(Injector):

    get = this.command.do
    post = this.command.do
    put = this.command.do
    patch = this.command.do
    delete = this.command.do
    head = this.command.do
    options = this.command.do
    trace = this.command.do


@method_view
class DispatchView(Methods):

    command = DispatchRequest
