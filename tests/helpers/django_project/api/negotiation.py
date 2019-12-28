from rest_framework.negotiation import BaseContentNegotiation

from django_project.api.exceptions import _NegotiationError


class _DenyNegotiation(BaseContentNegotiation):
    def select_renderer(self, request, renderers, format_suffix):
        raise _NegotiationError
