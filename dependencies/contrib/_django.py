from __future__ import absolute_import

from dependencies import this
from django.views.generic import View


def view(injector):
    """FIXME: Write docstring."""

    # FIXME: Assert injector has view attribute.

    class Handler(View):

        if "get" in injector:

            def get(self, request, *args, **kwargs):

                return injector.let(
                    view=self,
                    request=request,
                    args=args,
                    kwargs=kwargs,
                    user=this.request.user,
                ).get()

        if "post" in injector:

            def post(self, request, *args, **kwargs):

                return injector.let(
                    view=self,
                    request=request,
                    args=args,
                    kwargs=kwargs,
                    user=this.request.user,
                ).post()

        if "put" in injector:

            def put(self, request, *args, **kwargs):

                return injector.let(
                    view=self,
                    request=request,
                    args=args,
                    kwargs=kwargs,
                    user=this.request.user,
                ).put()

        if "patch" in injector:

            def patch(self, request, *args, **kwargs):

                return injector.let(
                    view=self,
                    request=request,
                    args=args,
                    kwargs=kwargs,
                    user=this.request.user,
                ).patch()

        if "delete" in injector:

            def delete(self, request, *args, **kwargs):

                return injector.let(
                    view=self,
                    request=request,
                    args=args,
                    kwargs=kwargs,
                    user=this.request.user,
                ).delete()

        if "head" in injector:

            def head(self, request, *args, **kwargs):

                return injector.let(
                    view=self,
                    request=request,
                    args=args,
                    kwargs=kwargs,
                    user=this.request.user,
                ).head()

        if "options" in injector:

            def options(self, request, *args, **kwargs):

                return injector.let(
                    view=self,
                    request=request,
                    args=args,
                    kwargs=kwargs,
                    user=this.request.user,
                ).options()

        if "trace" in injector:

            def trace(self, request, *args, **kwargs):

                return injector.let(
                    view=self,
                    request=request,
                    args=args,
                    kwargs=kwargs,
                    user=this.request.user,
                ).trace()

    return injector.let(as_view=Handler.as_view)
