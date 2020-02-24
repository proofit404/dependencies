# -*- coding: utf-8 -*-
from django import forms


class CartForm(forms.Form):
    product = forms.CharField(label="Product", max_length=100)
