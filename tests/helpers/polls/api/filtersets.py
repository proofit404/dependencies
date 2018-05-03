from django.contrib.auth.models import User
from django_filters.rest_framework import FilterSet


class UserFilter(FilterSet):

    class Meta(object):

        model = User
        fields = ["username"]
