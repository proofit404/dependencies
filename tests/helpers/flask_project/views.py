from dependencies import Injector
from dependencies import this
from dependencies.contrib.flask import method_view
from flask_project.commands import _DispatchRequest


class _Methods(Injector):
    get = this.command.do
    post = this.command.do
    put = this.command.do
    patch = this.command.do
    delete = this.command.do
    head = this.command.do
    options = this.command.do
    trace = this.command.do


@method_view
class _DispatchView(_Methods):
    command = _DispatchRequest
