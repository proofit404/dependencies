from __future__ import absolute_import

from collections import OrderedDict

from dependencies import this
from django.views.generic import View


def view(injector):
    """Create Django class-based view from injector class."""

    handler = create_handler(View)
    apply_http_methods(handler, injector)
    finalize_http_methods(handler)
    return injector.let(as_view=handler.as_view)


def create_handler(from_class):

    class Handler(from_class):
        http_method_names = OrderedDict.fromkeys(["head", "options"])

    return Handler


def apply_http_methods(handler, injector):

    for method in ["get", "post", "put", "patch", "delete", "head", "options", "trace"]:
        if method in injector:

            def __view(self, request, *args, **kwargs):
                ns = injector.let(
                    view=self,
                    request=request,
                    args=args,
                    kwargs=kwargs,
                    user=this.request.user,
                )
                return getattr(ns, __view.method)()

            __view.method = method
            handler.http_method_names[method] = None
            setattr(handler, method, __view)


def finalize_http_methods(handler):

    handler.http_method_names = list(handler.http_method_names.keys())
