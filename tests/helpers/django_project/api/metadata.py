from rest_framework.metadata import BaseMetadata

from django_project.api.exceptions import _MetadataError


class _DenyMetadata(BaseMetadata):
    def determine_metadata(self, request, view):
        raise _MetadataError
