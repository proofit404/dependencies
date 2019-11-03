from rest_framework.negotiation import BaseContentNegotiation

from django_project.api.exceptions import NegotiationError


class DenyNegotiation(BaseContentNegotiation):
    def select_renderer(self, request, renderers, format_suffix):

        raise NegotiationError
