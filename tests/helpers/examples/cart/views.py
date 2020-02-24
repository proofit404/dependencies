# -*- coding: utf-8 -*-
from dependencies import Injector
from dependencies.contrib.django import view
from dependencies.contrib.rest_framework import api_view
from dependencies.contrib.rest_framework import model_view_set


@view
class ShowCartWithDiscount(Injector):
    pass


@api_view
class CartAPIView(Injector):
    pass


@model_view_set
class UserViewSet(Injector):
    pass
