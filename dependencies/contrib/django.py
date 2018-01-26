"""
dependencies.contrib.django
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module implements injectable Django view.

:copyright: (c) 2016-2017 by Artem Malyshev.
:license: LGPL-3, see LICENSE for more details.
"""

from __future__ import absolute_import

from django.http import HttpResponse
from django.views.generic import View


def view(injector):
    """FIXME: Write docstring."""

    class Handler(View):

        def get(self, request, *args, **kwargs):

            ns = injector.let(request=request, args=args, kwargs=kwargs)
            result = ns.view.get()
            # FIXME: All http responses.
            return HttpResponse(result)

        # FIXME: All http methods.

    return injector.let(as_view=Handler.as_view)
