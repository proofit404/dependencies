from rest_framework.versioning import BaseVersioning

from django_project.api.exceptions import _VersionError


class _DenyVersion(BaseVersioning):
    def determine_version(self, request, *args, **kwargs):
        raise _VersionError
