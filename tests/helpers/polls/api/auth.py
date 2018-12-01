from django.contrib.auth.models import User
from rest_framework.authentication import BaseAuthentication


class AuthenticateAll(BaseAuthentication):
    def authenticate(self, request):

        return User.objects.first(), None


class AuthenticateAdmin(BaseAuthentication):
    def authenticate(self, request):

        return User.objects.get(username="admin"), None
