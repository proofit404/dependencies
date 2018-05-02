from dependencies.contrib.rest_framework import api_view, generic_api_view
from rest_framework.status import HTTP_200_OK
from rest_framework.test import APIClient

client = APIClient()


def test_dispatch_request():
    """
    Dispatch request to the `Injector` subclass attributes.

    DRF APIView render, parser, permissions and other attributes
    should be respected.
    """

    response = client.get("/api/questions-stat/", {"last": True}, format="json")
    assert response.status_code == HTTP_200_OK
    assert response.json() == {"details": "ok"}


def test_dispatch_request_generic_view():
    """
    Dispatch request to the dynamically created generic view subclass.
    """

    response = client.get("/api/questions-generic-stat/", format="json")
    assert response.status_code == HTTP_200_OK
    assert response.json() == {"details": "ok"}


def test_docstrings():
    """Access `api_view` and `generic_api_view` docstrings."""

    assert api_view.__doc__ == "Create DRF class-based API view from injector class."
    assert (
        generic_api_view.__doc__
        == "Create DRF generic class-based API view from injector class."
    )
