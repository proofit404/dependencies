from __future__ import absolute_import

from dependencies import this
from django.http import HttpResponse
from django.views.generic import View


def view(injector):
    """FIXME: Write docstring."""

    # FIXME: Assert injector has view attribute.

    class Handler(View):

        def handle(self, request, args, kwargs):

            return injector.let(
                request=request, args=args, kwargs=kwargs, user=this.request.user
            ).view

        def get(self, request, *args, **kwargs):

            result = self.handle(request, args, kwargs).get()
            # FIXME: All http responses.
            return HttpResponse(result)

    # FIXME: All http methods.
    return injector.let(as_view=Handler.as_view)
