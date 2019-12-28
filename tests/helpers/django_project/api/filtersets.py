from django.contrib.auth.models import User
from django_filters import VERSION
from django_filters.rest_framework import FilterSet


use_filterset_name = VERSION >= (2, 0)


class _UserFilter(FilterSet):
    class Meta(object):
        model = User
        fields = ["username"]
