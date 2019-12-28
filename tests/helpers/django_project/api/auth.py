from django.contrib.auth.models import User
from rest_framework.authentication import BaseAuthentication


class _AuthenticateAll(BaseAuthentication):
    def authenticate(self, request):
        return User.objects.first(), None


class _AuthenticateAdmin(BaseAuthentication):
    def authenticate(self, request):
        return User.objects.get(username="admin"), None
