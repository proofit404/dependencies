from __future__ import absolute_import

from flask.views import MethodView


def method_view(injector):
    """Create Flask method based dispatching view from injector class."""

    handler = create_handler(MethodView)
    apply_http_methods(handler, injector)
    return injector.let(as_view=handler.as_view)


def create_handler(from_class):
    class Handler(from_class):
        pass

    return Handler


def apply_http_methods(handler, injector):

    for method in ["get", "post", "head", "options", "delete", "put", "trace", "patch"]:
        if method in injector:

            def locals_hack(method=method):
                def __view(self, *args, **kwargs):
                    return getattr(injector, method)()

                return __view

            setattr(handler, method, locals_hack())
