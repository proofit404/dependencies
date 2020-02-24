# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):

        model = User
        fields = ("id", "username", "first_name", "last_name")
