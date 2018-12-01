from rest_framework.versioning import BaseVersioning

from .exceptions import VersionError


class DenyVersion(BaseVersioning):
    def determine_version(self, request, *args, **kwargs):

        raise VersionError
