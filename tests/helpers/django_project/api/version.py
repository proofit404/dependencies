from rest_framework.versioning import BaseVersioning

from django_project.api.exceptions import VersionError


class DenyVersion(BaseVersioning):
    def determine_version(self, request, *args, **kwargs):

        raise VersionError
