from django.template.response import TemplateResponse

from dependencies import Injector
from dependencies import this
from dependencies.contrib.django import form_view
from dependencies.contrib.django import view
from django_project.commands import DispatchRequest
from django_project.commands import InjectKwargs
from django_project.commands import InjectSelf
from django_project.commands import InjectUser
from django_project.commands import ProcessQuestion
from django_project.forms import QuestionForm


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
    """Intentionally left blank."""

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
    slug = this.kwargs["slug"]


@view
class SelfView(Methods):

    command = InjectSelf


class TestTemplateResponse(TemplateResponse):

    pass


@form_view
class QuestionFormView(Injector):
    """Intentionally left blank."""

    form_class = QuestionForm
    template_name = "question.html"
    success_url = "/thanks/"
    form_valid = this.command.handle_form
    form_invalid = this.command.handle_error
    command = ProcessQuestion

    template_engine = "default"
    response_class = TestTemplateResponse
    content_type = "text/html"
    initial = {"is_testing": True}
    prefix = "test"
    extra_context = {"extra_var": "extra-var"}
