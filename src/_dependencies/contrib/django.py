from __future__ import absolute_import

from django.views.generic import FormView
from django.views.generic import TemplateView
from django.views.generic import View

from _dependencies.exceptions import DependencyError
from _dependencies.this import this


def view(injector):
    """Create Django class-based view from injector class."""

    handler = create_handler(View, injector)
    apply_http_methods(handler, injector)
    return injector.let(as_view=handler.as_view)


def template_view(injector):
    """Create Django template class-based view from injector class."""

    handler = create_handler(TemplateView, injector)
    apply_template_methods(handler, injector)
    return injector.let(as_view=handler.as_view)


def form_view(injector):
    """Create Django form processing class-based view from injector class."""

    handler = create_handler(FormView, injector)
    apply_template_methods(handler, injector)
    apply_form_methods(handler, injector)
    return injector.let(as_view=handler.as_view)


def create_handler(from_class, injector):
    class Handler(from_class):
        __doc__ = injector.__doc__

    Handler.__name__ = injector.__name__
    Handler.__module__ = injector.__module__

    return Handler


def apply_http_methods(handler, injector):

    for method in ["get", "post", "put", "patch", "delete", "head", "options", "trace"]:
        if method in injector:
            setattr(handler, method, build_view_method(injector, method))


def apply_template_methods(handler, injector):

    for attribute in [
        "template_name",
        "template_engine",
        "response_class",
        "content_type",
        "extra_context",
    ]:
        if attribute in injector:
            setattr(handler, attribute, build_view_property(injector, attribute))


def apply_form_methods(handler, injector):

    for attribute in [
        "form_class",
        "success_url",
        "initial",
        "prefix",
    ]:
        if attribute in injector:
            setattr(handler, attribute, getattr(injector, attribute))

    for method in ["form_valid", "form_invalid"]:
        if method in injector:
            form_method = build_form_view_method(injector, method)
        else:
            form_method = build_form_view_error(injector, method)
        setattr(handler, method, form_method)


def build_view_method(injector, method):
    def __view(self, request, *args, **kwargs):
        __tracebackhide__ = True
        ns = injector.let(
            view=self,
            request=request,
            args=args,
            kwargs=kwargs,
            user=this.request.user,
            pk=this.kwargs["pk"],
        )
        return getattr(ns, method)()

    return __view


def build_view_property(injector, attribute, **extra):
    @property
    def __attribute(self):
        __tracebackhide__ = True
        ns = injector.let(
            view=self,
            request=this.view.request,
            args=this.view.args,
            kwargs=this.view.kwargs,
            user=this.request.user,
            pk=this.kwargs["pk"],
            **extra
        )
        return getattr(ns, attribute)

    return __attribute


def build_form_view_method(injector, method):
    def __method(self, form):
        __tracebackhide__ = True
        ns = injector.let(
            view=self,
            form=form,
            request=this.view.request,
            args=this.view.args,
            kwargs=this.view.kwargs,
            user=this.request.user,
            pk=this.kwargs["pk"],
        )
        return getattr(ns, method)()

    return __method


def build_form_view_error(injector, method):
    def __method(self, form):
        raise DependencyError(
            "Add {!r} to the {!r} injector".format(method, injector.__name__)
        )

    return __method
