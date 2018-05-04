from dependencies.contrib.rest_framework import api_view, generic_api_view
from django.contrib.auth.models import User
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN
from rest_framework.test import APIClient

client = APIClient()


def test_dispatch_request():
    """
    Dispatch request to the `Injector` subclass attributes.

    DRF APIView render, parser, permissions and other attributes
    should be respected.
    """

    response = client.get("/api/action/", {"last": True}, format="json")
    assert response.status_code == HTTP_200_OK
    assert response.content.decode().lstrip().startswith("<!DOCTYPE html>")

    response = client.get("/api/login/")
    assert response.status_code == HTTP_403_FORBIDDEN


def test_dispatch_request_generic_view_retrieve(db):
    """
    Retrieve user details through view defined with injector subclass.
    """

    User.objects.create(pk=1, username="johndoe", first_name="John", last_name="Doe")

    response = client.get("/api/users/johndoe/", format="json")
    assert response.status_code == HTTP_200_OK
    assert (
        response.json()
        == {"id": 1, "username": "johndoe", "first_name": "John", "last_name": "Doe"}
    )


def test_dispatch_request_generic_view_list(db):
    """
    List user details through view defined with injector subclass.
    """

    User.objects.create(pk=1, username="johndoe", first_name="John", last_name="Doe")
    User.objects.create(pk=2, username="foo", first_name="bar", last_name="baz")

    response = client.get("/api/users/?username=johndoe&limit=1", format="json")
    assert response.status_code == HTTP_200_OK
    assert (
        response.json()
        == {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": 1,
                    "username": "johndoe",
                    "first_name": "John",
                    "last_name": "Doe",
                }
            ],
        }
    )


def test_docstrings():
    """Access `api_view` and `generic_api_view` docstrings."""

    assert api_view.__doc__ == "Create DRF class-based API view from injector class."
    assert (
        generic_api_view.__doc__
        == "Create DRF generic class-based API view from injector class."
    )
