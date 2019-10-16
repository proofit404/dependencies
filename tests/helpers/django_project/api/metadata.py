from rest_framework.metadata import BaseMetadata

from django_project.api.exceptions import MetadataError


class DenyMetadata(BaseMetadata):
    def determine_metadata(self, request, view):

        raise MetadataError
