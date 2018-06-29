from rest_framework.metadata import BaseMetadata

from .exceptions import MetadataError


class DenyMetadata(BaseMetadata):

    def determine_metadata(self, request, view):

        raise MetadataError
