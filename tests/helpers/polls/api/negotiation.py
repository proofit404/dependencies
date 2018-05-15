from rest_framework.negotiation import BaseContentNegotiation

from .exceptions import NegotiationError


class DenyNegotiation(BaseContentNegotiation):

    def select_renderer(self, request, renderers, format_suffix):

        raise NegotiationError
