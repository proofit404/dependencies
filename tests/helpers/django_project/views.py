from django.contrib.auth.models import AnonymousUser

from dependencies import Injector
from dependencies import this
from dependencies import value
from dependencies.contrib.django import form_view
from dependencies.contrib.django import template_view
from dependencies.contrib.django import view
from django_project.commands import _DispatchRequest
from django_project.commands import _InjectKwargs
from django_project.commands import _InjectSelf
from django_project.commands import _InjectUser
from django_project.commands import _ProcessQuestion
from django_project.forms import _QuestionForm
from django_project.responses import _TestTemplateResponse


class _Methods(Injector):
    get = this.command.do
    post = this.command.do
    put = this.command.do
    patch = this.command.do
    delete = this.command.do
    head = this.command.do
    options = this.command.do
    trace = this.command.do


# View.


@view
class _DispatchView(_Methods):
    """Intentionally left blank."""

    command = _DispatchRequest


@view
class _EmptyView(Injector):
    pass


@view
class _UserView(_Methods):
    command = _InjectUser


@view
class _KwargsView(_Methods):
    command = _InjectKwargs
    slug = this.kwargs["slug"]


@view
class _SelfView(_Methods):
    command = _InjectSelf


# Template view.


@template_view
class _QuestionTemplateView(Injector):
    """Intentionally left blank."""

    template_name = "question.html"
    template_engine = "default"
    response_class = _TestTemplateResponse
    content_type = "text/html"
    extra_context = {"extra_var": "extra-var"}


@template_view
class _DynamicQuestionTemplateView(Injector):
    template_name = "question.html"
    template_engine = "default"
    response_class = _TestTemplateResponse
    content_type = "text/html"

    @value
    # Old versions of Django does not access this attribute while
    # processing template view.  So not all Tox environment will
    # report this function called.
    def extra_context(user):  # pragma: no cover
        assert isinstance(user, AnonymousUser)
        return {"extra_var": "extra-var"}


# Form view.


@form_view
class _QuestionFormView(Injector):
    """Intentionally left blank."""

    form_class = _QuestionForm
    template_name = "question.html"
    success_url = "/thanks/"
    form_valid = this.command.handle_form
    form_invalid = this.command.handle_error
    command = _ProcessQuestion
    template_engine = "default"
    response_class = _TestTemplateResponse
    content_type = "text/html"
    initial = {"is_testing": True}
    prefix = "test"
    extra_context = {"extra_var": "extra-var"}


@form_view
class _EmptyFormView(Injector):
    form_class = _QuestionForm
    template_name = "question.html"
    success_url = "/thanks/"
