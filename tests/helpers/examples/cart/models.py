from django.db import models


class Item(models.Model):
    class Meta:
        app_label = "django_project"


class User(models.Model):
    class Meta:
        app_label = "django_project"
